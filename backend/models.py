"""
backend.models

Simple JSON-backed data helpers for readings and foods.
These functions mirror the JSON logic used by app.py but are separated
so the backend folder is useful for future refactors or tests.
"""
from pathlib import Path
import json
from datetime import datetime
import os

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
READINGS_FILE = DATA_DIR / 'readings.json'
FOODS_FILE = DATA_DIR / 'foods.json'


def _ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)


def load_json(file_path):
    """Load JSON from a file path; return empty list on errors."""
    _ensure_data_dir()
    try:
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_json(file_path, data):
    """Save Python object to JSON file. Returns True on success."""
    _ensure_data_dir()
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False


# ---------------------- Readings API ----------------------

def init_db():
    """Seed files with example data if empty."""
    _ensure_data_dir()

    readings = load_json(READINGS_FILE)
    if not readings:
        sample_readings = [
            {"id": 1, "user_id": 1, "date": "2025-11-25", "time": "08:00", "glucose": 95.0, "context": "fasting", "meal": "water", "note": "morning check", "created_at": "2025-11-25T08:00:00Z"},
            {"id": 2, "user_id": 1, "date": "2025-11-25", "time": "12:30", "glucose": 142.0, "context": "pre-meal", "meal": "lunch", "note": "before eating", "created_at": "2025-11-25T12:30:00Z"},
            {"id": 3, "user_id": 1, "date": "2025-11-25", "time": "15:00", "glucose": 185.0, "context": "post-meal", "meal": "snack", "note": "high reading", "created_at": "2025-11-25T15:00:00Z"},
            {"id": 4, "user_id": 1, "date": "2025-11-26", "time": "06:30", "glucose": 65.0, "context": "fasting", "meal": "water", "note": "low reading", "created_at": "2025-11-26T06:30:00Z"},
            {"id": 5, "user_id": 1, "date": "2025-11-26", "time": "11:00", "glucose": 115.0, "context": "pre-meal", "meal": "breakfast", "note": "normal", "created_at": "2025-11-26T11:00:00Z"},
            {"id": 6, "user_id": 1, "date": "2025-11-27", "time": "14:00", "glucose": 220.0, "context": "post-meal", "meal": "dinner", "note": "elevated", "created_at": "2025-11-27T14:00:00Z"},
        ]
        save_json(READINGS_FILE, sample_readings)

    foods = load_json(FOODS_FILE)
    if not foods:
        sample_foods = [
            {"id": 1, "date": "2025-11-25", "time": "08:30", "food": "Oatmeal with berries"},
            {"id": 2, "date": "2025-11-25", "time": "12:30", "food": "Grilled chicken and vegetables"},
            {"id": 3, "date": "2025-11-25", "time": "18:00", "food": "Fish with steamed broccoli"},
        ]
        save_json(FOODS_FILE, sample_foods)


def add_reading(user_id, glucose, context='general', meal='', note=''):
    """Add a reading and return the new record."""
    readings = load_json(READINGS_FILE)
    new_id = max([r.get('id', 0) for r in readings], default=0) + 1
    new_reading = {
        'id': new_id,
        'user_id': user_id,
        'glucose': float(glucose),
        'context': context,
        'meal': meal,
        'note': note,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    readings.append(new_reading)
    save_json(READINGS_FILE, readings)
    return new_reading


def get_readings(user_id=None, limit=50):
    """Return list of readings (newest first)."""
    readings = load_json(READINGS_FILE)
    if user_id is not None:
        readings = [r for r in readings if r.get('user_id') == user_id]
    readings = sorted(readings, key=lambda r: r.get('created_at', ''), reverse=True)
    return readings[:limit]


def get_reading(reading_id):
    readings = load_json(READINGS_FILE)
    return next((r for r in readings if r.get('id') == reading_id), None)


def update_reading(reading_id, **fields):
    readings = load_json(READINGS_FILE)
    updated = None
    for r in readings:
        if r.get('id') == reading_id:
            r.update(fields)
            updated = r
            break
    if updated:
        save_json(READINGS_FILE, readings)
    return updated


def delete_reading(reading_id):
    readings = load_json(READINGS_FILE)
    new = [r for r in readings if r.get('id') != reading_id]
    save_json(READINGS_FILE, new)
    return True


# ---------------------- Foods API ----------------------

def add_food(date, time, food_text):
    foods = load_json(FOODS_FILE)
    new_id = max([f.get('id', 0) for f in foods], default=0) + 1
    new_food = {'id': new_id, 'date': date, 'time': time, 'food': food_text}
    foods.append(new_food)
    save_json(FOODS_FILE, foods)
    return new_food


def get_foods(limit=100):
    foods = load_json(FOODS_FILE)
    foods = sorted(foods, key=lambda f: (f.get('date', ''), f.get('time', '')), reverse=True)
    return foods[:limit]


def get_food(food_id):
    foods = load_json(FOODS_FILE)
    return next((f for f in foods if f.get('id') == food_id), None)


def delete_food(food_id):
    foods = load_json(FOODS_FILE)
    new = [f for f in foods if f.get('id') != food_id]
    save_json(FOODS_FILE, new)
    return True
