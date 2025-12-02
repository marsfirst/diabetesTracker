"""
Diabetes Tracker - Simple Flask App with JSON Storage
A friendly, accessible diabetes tracking application for older adults.
Uses JSON files for data storage (no database required).
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import json
import os
from pathlib import Path

app = Flask(__name__)

# Configuration
DATA_DIR = Path('data')
READINGS_FILE = DATA_DIR / 'readings.json'
FOODS_FILE = DATA_DIR / 'foods.json'
CACHE_FILE = DATA_DIR / 'cache.json'
SCHEDULER_FILE = DATA_DIR / 'scheduler.json'

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# ============================================================================
# HELPER FUNCTIONS - JSON Operations
# ============================================================================

def load_json(file_path):
    """Load JSON data from file. Return empty list if file doesn't exist."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_json(file_path, data):
    """Save data to JSON file."""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving {file_path}: {e}")
        return False

def init_db():
    """Initialize database with sample data if empty."""
    if not os.path.exists(READINGS_FILE) or len(load_json(READINGS_FILE)) == 0:
        sample_readings = [
            {"id": 1, "user_id": 1, "date": "2025-11-25", "time": "08:00", "glucose": 95.0, "context": "fasting", "meal": "water", "note": "morning check", "created_at": "2025-11-25T08:00:00Z"},
            {"id": 2, "user_id": 1, "date": "2025-11-25", "time": "12:30", "glucose": 142.0, "context": "pre-meal", "meal": "lunch", "note": "before eating", "created_at": "2025-11-25T12:30:00Z"},
            {"id": 3, "user_id": 1, "date": "2025-11-25", "time": "15:00", "glucose": 185.0, "context": "post-meal", "meal": "snack", "note": "high reading", "created_at": "2025-11-25T15:00:00Z"},
            {"id": 4, "user_id": 1, "date": "2025-11-26", "time": "06:30", "glucose": 65.0, "context": "fasting", "meal": "water", "note": "low reading", "created_at": "2025-11-26T06:30:00Z"},
            {"id": 5, "user_id": 1, "date": "2025-11-26", "time": "11:00", "glucose": 115.0, "context": "pre-meal", "meal": "breakfast", "note": "normal", "created_at": "2025-11-26T11:00:00Z"},
            {"id": 6, "user_id": 1, "date": "2025-11-27", "time": "14:00", "glucose": 220.0, "context": "post-meal", "meal": "dinner", "note": "elevated", "created_at": "2025-11-27T14:00:00Z"},
        ]
        save_json(READINGS_FILE, sample_readings)
    
    if not os.path.exists(FOODS_FILE) or len(load_json(FOODS_FILE)) == 0:
        sample_foods = [
            {"id": 1, "date": "2025-11-25", "time": "08:30", "food": "Oatmeal with berries"},
            {"id": 2, "date": "2025-11-25", "time": "12:30", "food": "Grilled chicken and vegetables"},
            {"id": 3, "date": "2025-11-25", "time": "18:00", "food": "Fish with steamed broccoli"},
        ]
        save_json(FOODS_FILE, sample_foods)

# ============================================================================
# RECOMMENDATIONS ENGINE
# ============================================================================

def get_recommendation(glucose_level):
    """
    Return a friendly recommendation based on glucose level.
    Also suggests when to check with a doctor.
    """
    level = float(glucose_level)
    
    if level > 250:
        return "Your blood sugar is quite high. Consider: drinking water, taking a short 10-minute walk, and checking with your healthcare provider if this happens often."
    elif level > 180:
        return "Your blood sugar is elevated. A gentle walk or light activity may help. Contact your healthcare provider if levels stay high."
    elif level < 70:
        return "Your blood sugar is low. Eat a fast-acting carb: juice, glucose tablets, or a few crackers. Test again in 15 minutes."
    elif level < 100:
        return "Your blood sugar is a bit low. Consider a light snack if you're hungry."
    else:
        return "Your blood sugar is in a healthy range. Keep monitoring regularly!"

# ============================================================================
# LRU CACHE IMPLEMENTATION (for COA demo)
# ============================================================================

class LRUCache:
    """Simple LRU Cache implementation for caching glucose readings."""
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.cache = {}
        self.order = []
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        """Get item from cache. Return None if not found. Increment hits/misses."""
        if key in self.cache:
            self.hits += 1
            # Move to end (most recently used)
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        else:
            self.misses += 1
            return None
    
    def put(self, key, value):
        """Put item in cache. Remove LRU item if cache is full."""
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used
            lru_key = self.order.pop(0)
            del self.cache[lru_key]
        
        self.cache[key] = value
        self.order.append(key)
    
    def items(self):
        """Return list of [key, value] pairs in order."""
        return [[k, self.cache[k]] for k in self.order]
    
    def stats(self):
        """Return cache statistics."""
        return {
            "capacity": self.capacity,
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses
        }

# Global cache instance
reading_cache = LRUCache(capacity=5)

# ============================================================================
# PRIORITY SCHEDULER IMPLEMENTATION (for COA demo)
# ============================================================================

import heapq

class PriorityScheduler:
    """Simple priority-based task scheduler using heap."""
    def __init__(self):
        self.queue = []
        self.task_id = 0
        self.history = []
    
    def submit(self, name, priority, ticks):
        """Submit a task. Lower priority number = higher priority (runs first)."""
        self.task_id += 1
        task = {
            "id": self.task_id,
            "name": name,
            "priority": priority,
            "ticks": ticks,
            "created_at": datetime.utcnow().isoformat()
        }
        heapq.heappush(self.queue, (priority, self.task_id, task))
        return task
    
    def run_tick(self):
        """Run one tick: decrement ticks on next task, remove if done."""
        executed = []
        if self.queue:
            priority, task_id, task = heapq.heappop(self.queue)
            task['ticks'] -= 1
            executed.append(task)
            self.history.append({**task, "executed_at": datetime.utcnow().isoformat()})
            
            if task['ticks'] > 0:
                # Re-queue if more ticks remain
                heapq.heappush(self.queue, (priority, task_id, task))
        
        return executed
    
    def run_ticks(self, n):
        """Run n ticks."""
        executed = []
        for _ in range(n):
            executed.extend(self.run_tick())
        return executed
    
    def list_tasks(self):
        """Return current queue (not in heapq order, but readable)."""
        return [task for _, _, task in self.queue]
    
    def get_history(self):
        """Return execution history."""
        return self.history

# Global scheduler instance
scheduler = PriorityScheduler()

# ============================================================================
# FLASK ROUTES - Main Pages
# ============================================================================

@app.route('/')
def index():
    """Home page with large friendly buttons."""
    return render_template('index.html')

@app.route('/add-reading', methods=['GET', 'POST'])
def add_reading():
    """Add a blood sugar reading."""
    recommendation = None
    
    if request.method == 'POST':
        try:
            date = request.form.get('date')
            time = request.form.get('time')
            glucose = float(request.form.get('glucose'))
            context = request.form.get('context', 'fasting')
            meal = request.form.get('meal', '')
            note = request.form.get('note', '')
            
            readings = load_json(READINGS_FILE)
            new_id = max([r['id'] for r in readings], default=0) + 1
            
            new_reading = {
                'id': new_id,
                'user_id': 1,
                'date': date,
                'time': time,
                'glucose': glucose,
                'context': context,
                'meal': meal,
                'note': note,
                'created_at': datetime.utcnow().isoformat() + 'Z'
            }
            
            readings.append(new_reading)
            save_json(READINGS_FILE, readings)
            
            # Get recommendation
            recommendation = get_recommendation(glucose)
            
            # Add to cache
            reading_cache.put(new_id, new_reading)
            
            print(f"✓ Added reading: {glucose} mg/dL")
            
        except ValueError as e:
            print(f"Error: {e}")
    
    # Pre-fill with today's date and current time
    today = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%H:%M')
    
    return render_template('add_reading.html', recommendation=recommendation, today=today, now=now)

@app.route('/add-food', methods=['GET', 'POST'])
def add_food():
    """Add a food intake record."""
    if request.method == 'POST':
        try:
            date = request.form.get('date')
            time = request.form.get('time')
            food = request.form.get('food')
            
            foods = load_json(FOODS_FILE)
            new_id = max([f['id'] for f in foods], default=0) + 1
            
            new_food = {
                'id': new_id,
                'date': date,
                'time': time,
                'food': food
            }
            
            foods.append(new_food)
            save_json(FOODS_FILE, foods)
            
            print(f"✓ Added food: {food}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    today = datetime.now().strftime('%Y-%m-%d')
    now = datetime.now().strftime('%H:%M')
    
    return render_template('add_food.html', today=today, now=now)

@app.route('/history')
def history():
    """Show history of readings and food intake."""
    readings = sorted(load_json(READINGS_FILE), key=lambda x: (x['date'], x['time']), reverse=True)
    foods = sorted(load_json(FOODS_FILE), key=lambda x: (x['date'], x['time']), reverse=True)
    
    return render_template('history.html', readings=readings, foods=foods)

# ============================================================================
# JSON API ROUTES (for frontend fetch calls)
# ============================================================================

@app.route('/api/ping', methods=['GET'])
def ping():
    """Ping endpoint to test backend connectivity."""
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat() + 'Z'})

@app.route('/api/login', methods=['POST'])
def login():
    """Simple demo login."""
    data = request.get_json() or {}
    email = data.get('email', 'user@example.com')
    pin = data.get('pin', '1234')
    
    # Demo: accept any email and pin
    return jsonify({
        "ok": True,
        "user": {
            "id": 1,
            "email": email
        }
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    """Simple demo logout."""
    return jsonify({"ok": True})

@app.route('/api/readings', methods=['GET', 'POST'])
def api_readings():
    """GET: List readings. POST: Add a reading."""
    if request.method == 'GET':
        user_id = request.args.get('user_id', 1, type=int)
        limit = request.args.get('limit', 50, type=int)
        
        readings = load_json(READINGS_FILE)
        readings = [r for r in readings if r.get('user_id') == user_id]
        readings = sorted(readings, key=lambda x: x['created_at'], reverse=True)[:limit]
        
        return jsonify({
            "ok": True,
            "readings": readings
        })
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            readings = load_json(READINGS_FILE)
            new_id = max([r['id'] for r in readings], default=0) + 1
            
            new_reading = {
                'id': new_id,
                'user_id': data.get('user_id', 1),
                'glucose': float(data.get('glucose')),
                'context': data.get('context', 'fasting'),
                'meal': data.get('meal', ''),
                'note': data.get('note', ''),
                'created_at': datetime.utcnow().isoformat() + 'Z'
            }
            
            readings.append(new_reading)
            save_json(READINGS_FILE, readings)
            reading_cache.put(new_id, new_reading)
            
            return jsonify({"ok": True, "reading": new_reading}), 201
        
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 400

@app.route('/api/readings/<int:reading_id>', methods=['GET', 'PUT', 'DELETE'])
def api_reading_detail(reading_id):
    """GET: Get a reading. PUT: Update. DELETE: Delete."""
    readings = load_json(READINGS_FILE)
    reading = next((r for r in readings if r['id'] == reading_id), None)
    
    if not reading:
        return jsonify({"ok": False, "error": "Reading not found"}), 404
    
    if request.method == 'GET':
        return jsonify({"ok": True, "reading": reading})
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            reading.update(data)
            readings = [r for r in readings if r['id'] != reading_id]
            readings.append(reading)
            save_json(READINGS_FILE, readings)
            reading_cache.put(reading_id, reading)
            return jsonify({"ok": True, "reading": reading})
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 400
    
    elif request.method == 'DELETE':
        readings = [r for r in readings if r['id'] != reading_id]
        save_json(READINGS_FILE, readings)
        return jsonify({"ok": True})

@app.route('/api/suggestions', methods=['POST'])
def api_suggestions():
    """Get suggestions based on glucose level. May enqueue scheduler tasks."""
    try:
        data = request.get_json()
        glucose = float(data.get('glucose'))
        context = data.get('context', 'general')
        
        suggestions = []
        enqueued = []
        
        if glucose > 180:
            suggestions = [
                "Consider light walking 10–20 minutes and re-check blood sugar.",
                "Stay hydrated — drink water regularly.",
                "Contact your healthcare provider if elevated readings happen often."
            ]
            # Enqueue high-priority reminder
            task = scheduler.submit("Doctor reminder (auto)", priority=2, ticks=1)
            enqueued = [{"name": task['name'], "priority": task['priority'], "ticks": task['ticks']}]
        
        elif glucose < 70:
            suggestions = [
                "Your blood sugar is low. Eat a fast-acting carb (juice, crackers, glucose tablets).",
                "Re-check in 15 minutes.",
                "If this happens often, discuss with your doctor."
            ]
        
        else:
            suggestions = [
                "Your blood sugar is in a good range.",
                "Keep monitoring regularly.",
                "Continue with your healthy habits!"
            ]
        
        return jsonify({
            "ok": True,
            "suggestions": suggestions,
            "enqueued": enqueued
        })
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.route('/api/cache', methods=['GET'])
def api_cache():
    """Get cache statistics and items."""
    stats = reading_cache.stats()
    items = reading_cache.items()
    
    return jsonify({
        "ok": True,
        "capacity": stats['capacity'],
        "size": stats['size'],
        "hits": stats['hits'],
        "misses": stats['misses'],
        "items": items
    })

@app.route('/api/cache/get/<int:item_id>', methods=['GET'])
def api_cache_get(item_id):
    """Get item from cache (or load from DB if not cached)."""
    item = reading_cache.get(item_id)
    
    if not item:
        # Load from DB
        readings = load_json(READINGS_FILE)
        item = next((r for r in readings if r['id'] == item_id), None)
        if item:
            reading_cache.put(item_id, item)
    
    stats = reading_cache.stats()
    
    if item:
        return jsonify({
            "ok": True,
            "item": item,
            "stats": stats
        })
    else:
        return jsonify({"ok": False, "error": "Item not found"}), 404

@app.route('/api/cache/put', methods=['POST'])
def api_cache_put():
    """Load reading into cache."""
    try:
        data = request.get_json()
        item_id = data.get('id')
        
        readings = load_json(READINGS_FILE)
        item = next((r for r in readings if r['id'] == item_id), None)
        
        if item:
            reading_cache.put(item_id, item)
            stats = reading_cache.stats()
            return jsonify({"ok": True, "item": item, "stats": stats})
        else:
            return jsonify({"ok": False, "error": "Item not found"}), 404
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.route('/api/scheduler', methods=['GET', 'POST'])
def api_scheduler():
    """GET: List scheduler queue. POST: Submit a task."""
    if request.method == 'GET':
        queue = scheduler.list_tasks()
        history = scheduler.get_history()
        
        return jsonify({
            "ok": True,
            "queue": queue,
            "history": history
        })
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            name = data.get('name')
            priority = int(data.get('priority', 5))
            ticks = int(data.get('ticks', 1))
            
            task = scheduler.submit(name, priority, ticks)
            
            return jsonify({"ok": True, "task": task}), 201
        
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 400

@app.route('/api/scheduler/run', methods=['POST'])
def api_scheduler_run():
    """Run scheduler for n ticks."""
    try:
        ticks = request.args.get('ticks', 1, type=int)
        executed = scheduler.run_ticks(ticks)
        queue = scheduler.list_tasks()
        history = scheduler.get_history()
        
        return jsonify({
            "ok": True,
            "executed": executed,
            "queue": queue,
            "history": history
        })
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.route('/api/export', methods=['GET'])
def api_export():
    """Export readings as CSV wrapped in JSON."""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        readings = load_json(READINGS_FILE)
        readings = [r for r in readings if r.get('user_id') == user_id]
        readings = sorted(readings, key=lambda x: x['created_at'])
        
        # Build CSV
        csv_lines = ["id,user_id,glucose,context,meal,note,created_at"]
        for r in readings:
            line = f"{r['id']},{r['user_id']},{r['glucose']},{r['context']},{r['meal']},{r['note']},{r['created_at']}"
            csv_lines.append(line)
        
        csv_content = "\n".join(csv_lines)
        
        return jsonify({
            "ok": True,
            "csv": csv_content
        })
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.route('/api/import', methods=['POST'])
def api_import():
    """Import readings from JSON array."""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 1)
        import_readings = data.get('readings', [])
        
        readings = load_json(READINGS_FILE)
        max_id = max([r['id'] for r in readings], default=0)
        
        inserted = 0
        for reading in import_readings:
            max_id += 1
            new_reading = {
                'id': max_id,
                'user_id': user_id,
                'glucose': reading.get('glucose'),
                'context': reading.get('context', 'general'),
                'meal': reading.get('meal', ''),
                'note': reading.get('note', ''),
                'created_at': datetime.utcnow().isoformat() + 'Z'
            }
            readings.append(new_reading)
            inserted += 1
        
        save_json(READINGS_FILE, readings)
        
        return jsonify({"ok": True, "inserted": inserted}), 201
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

# ============================================================================
# ERROR HANDLERS & CORS
# ============================================================================

@app.after_request
def add_cors_headers(response):
    """Add CORS headers to all responses."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/<path:path>')
def catch_all(path):
    """Redirect unknown routes to static index.html"""
    return redirect(url_for('index'))

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    
    print("\n" + "="*60)
    print("🩺 DIABETES TRACKER - Starting up")
    print("="*60)
    print("📍 Server running at: http://127.0.0.1:5000")
    print("🌐 Open your browser and navigate to:")
    print("   http://127.0.0.1:5000/static/index.html")
    print("="*60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
