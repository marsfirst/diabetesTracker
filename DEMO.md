# Diabetes Tracker - Demo Instructions

## Quick Start (5 minutes)

### Step 1: Prepare Your Computer
Make sure you have Python 3.10+ installed:
```cmd
python --version
```

If you get "Python not found", download from [python.org](https://python.org/downloads) and check "Add Python to PATH" during installation.

### Step 2: Open Command Prompt
Press `Windows + R`, type `cmd`, and press Enter.

### Step 3: Navigate and Setup
```cmd
cd %USERPROFILE%\diabetes_simple_json
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

You should see `(venv)` at the start of the command prompt.

### Step 4: Start the Server
```cmd
python app.py
```

You should see:
```
============================================================
🩺 DIABETES TRACKER - Starting up
============================================================
📍 Server running at: http://127.0.0.1:5000
🌐 Open your browser and navigate to:
   http://127.0.0.1:5000/static/index.html
============================================================
```

### Step 5: Open in Browser
Open any web browser and go to:
```
http://127.0.0.1:5000/static/index.html
```

---

## Demo Walkthrough

### 1. Home Page (Main Dashboard)
**URL:** `http://127.0.0.1:5000/static/index.html`

**What you'll see:**
- Large heading: "🩺 Diabetes Tracker - Simple and Friendly"
- 6 action cards in a grid
- Medical disclaimer at top
- Large, easy-to-read buttons

**What to do:**
- Point out the medical disclaimer
- Explain the 6 main features
- Note the large fonts (18-24px)
- High contrast colors

---

### 2. Log Blood Sugar Demo
**Click:** "Log Sugar" button

**What you'll see:**
- Date field (auto-filled with today)
- Time field (auto-filled with current time)
- Number input for glucose (mg/dL)
- Dropdown for context (fasting, pre-meal, post-meal, bedtime)
- Dropdown for meal type
- Text area for notes
- Large blue submit button

**Demo Entry:**
```
Date: 2025-11-28 (auto-filled)
Time: 14:00 (auto-filled)
Glucose: 220
Context: post-meal
Meal: lunch
Note: feeling tired
```

**After Submit:**
- You'll see a recommendation box with:
  - "Your blood sugar is elevated. A gentle walk or light activity may help..."
  - Friendly, encouraging tone
  - No medical jargon

**Why this works:**
- Auto-filled date/time reduces errors
- Simple dropdowns (no typing required)
- Personalized feedback after submission
- Large, easy-to-click submit button

---

### 3. Log Food Demo
**Click:** "Log Food" button (back to home first, or just navigate)

**What you'll see:**
- Date and time fields
- Large text area for food description
- Big submit button

**Demo Entry:**
```
Date: 2025-11-28
Time: 12:00
Food: Grilled chicken with broccoli, 1 glass of water
```

**Why this works:**
- Simple, free-form text entry
- No complex food database needed
- Easy to describe what was actually eaten

---

### 4. View History
**Click:** "View History" button

**What you'll see:**
- Two tables: "Blood Sugar Readings" and "Food Log"
- Newest entries appear first
- Glucose levels are color-coded:
  - 🟢 Green (70-180) = normal range
  - 🟡 Orange (< 70) = low
  - 🔴 Red (> 180) = high

**Sample Data** (seeded automatically):
```
Reading 1: 95 mg/dL (fasting) - GREEN
Reading 2: 142 mg/dL (pre-meal) - GREEN
Reading 3: 185 mg/dL (post-meal) - RED
Reading 4: 65 mg/dL (fasting) - ORANGE
Reading 5: 115 mg/dL (pre-meal) - GREEN
Reading 6: 220 mg/dL (post-meal) - RED
```

**Why this works:**
- Large, simple tables
- Color coding makes patterns obvious
- No overwhelming data
- Newest first (natural reading order)

---

### 5. Cache Demo (Computer Organization & Architecture)

**Click:** "Open Cache Demo" button

**What you'll see:**
- Heading: "🔄 LRU Cache Demo"
- "What is an LRU Cache?" explanation
- Cache statistics (capacity, size, hits, misses)
- List of cached items
- Input to load items into cache
- Refresh button
- Debug console at bottom

**Demo Steps:**

1. **Note initial stats:**
   - Capacity: 5 (can hold 5 items max)
   - Size: 0 (currently empty)
   - Hits: 0
   - Misses: 0

2. **Load reading #1 into cache:**
   - Type "1" in the input
   - Click "Load to Cache"
   - Watch the size increase to 1
   - Reading appears in items list

3. **Load readings #2, #3, #4, #5:**
   - Repeat the process
   - Watch as cache fills up
   - Size reaches 5

4. **Load reading #6:**
   - Cache is full!
   - Reading #1 gets evicted (least recently used)
   - Reading #6 takes its place
   - Size stays at 5

5. **Access reading #1 again:**
   - It's not in cache anymore
   - This increments MISSES
   - It loads from database
   - Gets re-added to cache
   - Most recent item

6. **Access reading #2:**
   - It's still in cache
   - This increments HITS
   - Item moves to end (most recent)

**Key Learning Points:**
- LRU evicts oldest, least-used items
- Helps understand memory hierarchy (CPU cache, web cache)
- Trade-off: speed vs. memory capacity
- Importance of locality of reference

**Debug Console Output:**
```
[14:05:23] Welcome to the LRU Cache Demo!
[14:05:23] Enter a reading ID (1-6) to load it into the cache.
[14:05:23] The cache can hold 5 items at a time.
[14:05:25] Loading reading 1 into cache...
[14:05:25] ✓ Reading 1 loaded into cache
[14:05:25] Stats: 1/5 slots, 0 hits, 0 misses
```

---

### 6. Scheduler Demo (Computer Organization & Architecture)

**Click:** "Open Scheduler Demo" button

**What you'll see:**
- Heading: "⏱️ Priority Scheduler Demo"
- "What is a Priority Scheduler?" explanation
- Form to submit new tasks
- Current queue (list of pending tasks)
- Run Scheduler button
- Execution history

**Demo Steps:**

1. **Submit Task 1:**
   - Task Name: "Doctor reminder"
   - Priority: 1 (highest)
   - Ticks: 2
   - Click "Submit Task"
   - Task appears in queue

2. **Submit Task 2:**
   - Task Name: "Follow-up check"
   - Priority: 5 (medium)
   - Ticks: 1
   - Click "Submit Task"
   - Task appears in queue (after Task 1, since priority 1 < 5)

3. **Submit Task 3:**
   - Task Name: "General note"
   - Priority: 9 (low)
   - Ticks: 1
   - Click "Submit Task"
   - Task appears in queue (last, since priority is highest number)

4. **Queue shows (in order):**
   ```
   1. Doctor reminder (Priority 1, Ticks 2)
   2. Follow-up check (Priority 5, Ticks 1)
   3. General note (Priority 9, Ticks 1)
   ```

5. **Run for 1 tick:**
   - Set "Run for how many ticks?" to 1
   - Click "Run Ticks"
   - "Doctor reminder" executes
   - History shows: "Doctor reminder | Priority: 1 | Executed at: 14:05:45"
   - Task remains in queue (Ticks decremented to 1)

6. **Run for 3 ticks:**
   - Set to 3
   - Click "Run Ticks"
   - Executes:
     - Doctor reminder (ticks: 1→0, removed after)
     - Follow-up check (ticks: 1→0, removed after)
     - General note (ticks: 1→0, removed after)
   - Queue is now empty
   - History shows all 3 executions with timestamps

**Key Learning Points:**
- Priority-based scheduling (lower number = higher priority)
- FIFO with priority (jobs don't execute in order they arrive, but by importance)
- Real-world analogy: OS task scheduler, hospital triage
- Min-heap implementation makes this efficient
- Ticks represent time slices

**Use Case Examples:**
- Priority 1: Critical system task
- Priority 5: Regular maintenance
- Priority 10: Optional background work

---

### 7. API Testing (Bonus)

You can test the backend endpoints directly. Examples:

**Test ping:**
```
GET http://127.0.0.1:5000/api/ping
```
Response:
```json
{"status": "ok", "time": "2025-11-28T14:05:45Z"}
```

**Test login:**
```
POST http://127.0.0.1:5000/api/login
Body: {"email": "user@example.com", "pin": "1234"}
```
Response:
```json
{"ok": true, "user": {"id": 1, "email": "user@example.com"}}
```

**List readings:**
```
GET http://127.0.0.1:5000/api/readings?user_id=1&limit=10
```
Response:
```json
{
  "ok": true,
  "readings": [
    {"id": 1, "glucose": 95.0, "context": "fasting", ...},
    ...
  ]
}
```

---

## Teaching Notes

### For High School / Early College
- Focus on the **user interface** and **accessibility**
- Explain why large fonts matter for older adults
- Discuss color contrast and readability
- Show the friendly tone (no jargon)

### For Computer Organization & Architecture (CS306)
- **Cache Demo**: Show LRU eviction policy, cache hits/misses
- **Scheduler Demo**: Explain priority-based scheduling, min-heap ordering
- **Backend**: Discuss REST API design, JSON serialization
- **Data Structures**: LRUCache uses OrderedDict, Scheduler uses heapq

### For Web Development
- Show Flask routing (`@app.route`)
- Static file serving
- RESTful API design
- Vanilla JavaScript fetch calls
- HTML/CSS/JavaScript separation

### For UX/Accessibility
- Large fonts (18-24px minimum)
- High contrast colors (WCAG AAA)
- Simple navigation (3 main buttons)
- Clear labels (no icons without text)
- Medical disclaimer (legal/ethical requirement)

---

## Troubleshooting During Demo

### Problem: Port 5000 already in use
**Solution:**
```cmd
# Edit app.py, change port from 5000 to 5001
# Then restart
python app.py
# Visit http://127.0.0.1:5001/static/index.html
```

### Problem: Cache/Scheduler demo shows empty
**Solution:**
- Refresh the page (Ctrl + F5)
- Check browser console for errors (F12)
- Verify backend is running

### Problem: Readings not showing in history
**Solution:**
1. Reload the page
2. Check that data was actually submitted (look at terminal output)
3. Verify `data/readings.json` exists in project folder

### Problem: Can't activate virtual environment
**Solution:**
```cmd
# Try PowerShell instead of cmd
powershell
cd your\project\path
.\venv\Scripts\Activate.ps1
```

---

## After the Demo

### For Students
1. **Study the code**: Read through app.py (it's all comments!)
2. **Try modifications**:
   - Change the glucose level thresholds for recommendations
   - Add a new field to readings (e.g., mood, exercise)
   - Create a new demo page (e.g., calorie counter)
3. **Extend the database**: Convert from JSON to SQLite
4. **Build the frontend**: Create a mobile app using React Native

### For Instructors
1. **Use as teaching tool**: Show code structure, REST APIs, data structures
2. **Assign homework**: "Add feature X to the app"
3. **Group projects**: "Build a medical tracker app for [specific disease]"
4. **Real-world context**: Discuss why accessibility matters in healthcare

---

## Stopping the Server

At any time, press **Ctrl + C** in the terminal to stop the Flask server:

```cmd
^C
KeyboardInterrupt
* Debugger is active!
* Debugger PIN: 123-456-789
```

The server will shut down gracefully. All data is saved to `data/` folder.

---

## Reset Data

To start fresh with sample data only:

1. Stop the server (Ctrl + C)
2. Delete the data folder:
   ```cmd
   rmdir /s /q data
   ```
3. Restart the server:
   ```cmd
   python app.py
   ```

The app will recreate `data/` with fresh sample data.

---

## Questions During Demo?

**What if someone asks about...**

**"Is this a real medical device?"**
- No, it's for education only. Always consult a doctor.

**"Can we store this in the cloud?"**
- Yes, move the data/ folder to cloud storage, or use a real database.

**"How do we add multi-user support?"**
- Implement real login/authentication, use database with user IDs.

**"Can we integrate with fitness trackers?"**
- Yes, use their APIs. Would make a great capstone project!

**"How do we handle HIPAA compliance?"**
- Use HTTPS, encrypt data, proper access controls. This demo doesn't have all that—it's educational only.

---

Enjoy the demo! 🎉
