# 🩺 Diabetes Tracker - Simple & Accessible

A friendly web application for tracking blood sugar levels and food intake, designed to be easy for older adults to use. Built with Python Flask and stores data in JSON files — no complicated database setup required.

## What It Does

- **Log Blood Sugar**: Simple form to record glucose readings with date, time, and context.
- **Log Food Intake**: Track meals and snacks throughout the day.
- **View History**: See all readings and food logs sorted by date (newest first).
- **Get Recommendations**: Receive gentle, friendly suggestions based on your blood sugar levels.
- **LRU Cache Demo**: See how caching works with glucose readings (Computer Organization & Architecture demo).
- **Priority Scheduler Demo**: Task scheduling with priority levels (COA demo).
- **JSON API**: Full REST API for querying and managing data.

## Medical Disclaimer

⚠️ **This application is for educational and demonstration purposes only.**
It is NOT a medical device and should NOT be used for medical diagnosis or treatment.
Always consult with a licensed healthcare provider for medical guidance about your diabetes management.

This app provides general information and friendly reminders only. Do not rely on it for medical decisions.

---

## Prerequisites

Before you begin, make sure you have:

- **Python 3.10 or higher** ([Download from python.org](https://www.python.org/downloads/))
- **pip** (usually included with Python)
- **Windows Command Prompt** or **PowerShell**

To check if Python is installed:
```cmd
python --version
```

---

## Quick Start (Windows)

Follow these exact steps in Command Prompt or PowerShell:

### Step 1: Create Project Folder
```cmd
mkdir %USERPROFILE%\diabetes_simple_json
cd %USERPROFILE%\diabetes_simple_json
```

### Step 2: Create Virtual Environment
```cmd
python -m venv venv
```

### Step 3: Activate Virtual Environment
```cmd
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 4: Install Dependencies
```cmd
pip install -r requirements.txt
```

### Step 5: Run the Server
```cmd
python app.py
```

You should see output like:
```
============================================================
🩺 DIABETES TRACKER - Starting up
============================================================
📍 Server running at: http://127.0.0.1:5000
🌐 Open your browser and navigate to:
   http://127.0.0.1:5000/static/index.html
============================================================
```

### Step 6: Open in Browser
Click or copy-paste this link into your web browser:
```
http://127.0.0.1:5000/static/index.html
```

---

## Features & Pages

### 🏠 Home (Dashboard)
- Large welcome message
- Three big buttons: "Log Sugar", "Log Food", "View History"
- Links to Cache and Scheduler demos
- Medical disclaimer at the bottom

### 📊 Log Blood Sugar (`/add-reading`)
- Date field (auto-filled with today)
- Time field (auto-filled with current time)
- Blood sugar level (number input)
- Context (fasting, pre-meal, post-meal)
- Meal type (water, breakfast, lunch, snack, etc.)
- Additional notes
- **After submitting**: See a personalized recommendation!

### 🍽️ Log Food (`/add-food`)
- Date and time fields
- Description of what you ate/drank
- Easy to use while standing or at a table

### 📈 History (`/history`)
- Two sortable tables: recent readings and food logs
- Shows date, time, glucose level, and notes
- Newest entries appear first
- Large, easy-to-read text

### 🎯 Recommendations
After logging a reading, you'll see one of these:

| Your Level | You Might See |
|-----------|--------------|
| > 250 mg/dL | "Your blood sugar is quite high. Consider drinking water, taking a short 10-minute walk..." |
| 180-250 mg/dL | "Your blood sugar is elevated. A gentle walk or light activity may help..." |
| 70-180 mg/dL | "Your blood sugar is in a healthy range..." |
| < 70 mg/dL | "Your blood sugar is low. Eat a fast-acting carb..." |

### 🔄 Cache Demo (`/cache.html`)
- Shows how computer systems use caching to speed up data access
- Educational demo of LRU (Least Recently Used) cache
- Test by loading readings into cache and watching stats update

### ⏱️ Scheduler Demo (`/scheduler.html`)
- Demonstrates priority-based task scheduling
- Submit tasks with name, priority, and tick count
- Run ticks to execute tasks
- See execution history

---

## File Structure

```
diabetes_simple_json/
│── app.py                   # Main Flask application (all backend code)
│── requirements.txt         # Python dependencies (just Flask)
│── README.md               # This file
│── data/                   # JSON data files (created at runtime)
│   ├── readings.json       # Blood sugar readings
│   ├── foods.json          # Food intake log
│   ├── cache.json          # Cache data (if used)
│   └── scheduler.json      # Scheduler data (if used)
│
└── static/                 # Frontend files (HTML/CSS/JS)
    ├── index.html          # Home page
    ├── login.html          # Login page (demo)
    ├── add_reading.html    # Log blood sugar page
    ├── add_food.html       # Log food page
    ├── history.html        # History page
    ├── cache.html          # Cache demo page
    ├── scheduler.html      # Scheduler demo page
    ├── css/
    │   └── style.css       # Styles (large fonts, high contrast)
    └── js/
        ├── main.js         # Core functions (fetch, login, load data)
        ├── cache.js        # Cache demo logic
        └── scheduler.js    # Scheduler demo logic
```

---

## JSON Data Format

### readings.json
```json
[
  {
    "id": 1,
    "user_id": 1,
    "date": "2025-11-25",
    "time": "08:00",
    "glucose": 95.0,
    "context": "fasting",
    "meal": "water",
    "note": "morning check",
    "created_at": "2025-11-25T08:00:00Z"
  }
]
```

### foods.json
```json
[
  {
    "id": 1,
    "date": "2025-11-25",
    "time": "08:30",
    "food": "Oatmeal with berries"
  }
]
```

---

## API Examples

### POST /api/readings - Add a Reading
**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/readings \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "glucose": 145.5,
    "context": "post-meal",
    "meal": "lunch",
    "note": "after salad"
  }'
```

**Response:**
```json
{
  "ok": true,
  "reading": {
    "id": 7,
    "user_id": 1,
    "glucose": 145.5,
    "context": "post-meal",
    "meal": "lunch",
    "note": "after salad",
    "created_at": "2025-11-28T14:30:00Z"
  }
}
```

### POST /api/suggestions - Get Suggestions
**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "glucose": 220.0,
    "context": "post-meal"
  }'
```

**Response:**
```json
{
  "ok": true,
  "suggestions": [
    "Consider light walking 10–20 minutes and re-check blood sugar.",
    "Stay hydrated — drink water regularly.",
    "Contact your healthcare provider if elevated readings happen often."
  ],
  "enqueued": [
    {
      "name": "Doctor reminder (auto)",
      "priority": 2,
      "ticks": 1
    }
  ]
}
```

### GET /api/cache - View Cache Stats
**Response:**
```json
{
  "ok": true,
  "capacity": 5,
  "size": 3,
  "hits": 10,
  "misses": 2,
  "items": [
    [1, {"id": 1, "glucose": 95.0, ...}],
    [3, {"id": 3, "glucose": 185.0, ...}]
  ]
}
```

---

## Resetting Data

To delete all saved readings and food logs and start fresh:

1. **Stop the server** (press `Ctrl + C` in the command prompt)
2. **Delete the data folder**: 
   ```cmd
   rmdir /s /q data
   ```
3. **Start the server again**:
   ```cmd
   python app.py
   ```

The app will automatically recreate `data/` and seed it with sample data.

---

## Stopping the Server

To stop the Flask server at any time, press **Ctrl + C** in the command prompt.

---

## Accessibility Features

This app is designed with older adults in mind:

- ✅ **Large fonts** (18-24px)
- ✅ **High contrast** colors (dark text on light background)
- ✅ **Simple navigation** (minimal menus, big buttons)
- ✅ **Clear labels** (no jargon)
- ✅ **Friendly language** (warm, encouraging tone)
- ✅ **Large input fields** (easy to tap or click)
- ✅ **Minimal scrolling** (content fits well on screen)
- ✅ **No animations** (no flickering or distracting effects)

---

## Troubleshooting

### "Python not found"
Make sure Python is installed and in your PATH. Reinstall from [python.org](https://www.python.org/downloads/) and check "Add Python to PATH".

### "Port 5000 already in use"
Another app is using port 5000. Either close that app or change the port in `app.py` line ~600:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Use 5001 instead
```

### "Virtual environment won't activate"
Make sure you're in the correct folder (`cd` to your project directory first) and try:
```cmd
venv\Scripts\activate
```

### "Module not found: Flask"
Make sure you ran `pip install -r requirements.txt` AFTER activating the virtual environment.

---

## Development Notes

### Backend (app.py)
- **LRUCache class**: Demonstrates a cache data structure with hits/misses tracking
- **PriorityScheduler class**: Implements a min-heap based task scheduler
- **JSON persistence**: All data saved to `data/` folder (created automatically)
- **CORS enabled**: API works with any frontend

### Frontend
- **Vanilla JavaScript**: No frameworks needed
- **Fetch API**: Makes async calls to backend endpoints
- **LocalStorage**: Stores user login info temporarily
- **Responsive design**: Works on phones, tablets, computers

### Computer Organization & Architecture (COA) Concepts

This project includes two COA learning demos:

1. **LRU Cache** (`/cache.html`):
   - Demonstrates memory caching with capacity limits
   - Shows hit/miss rates
   - Illustrates the importance of cache locality and replacement policies

2. **Priority Scheduler** (`/scheduler.html`):
   - Shows task scheduling with priorities
   - Uses a heap data structure
   - Demonstrates how operating systems manage processes

---

## License

This is an educational project. Use freely for learning purposes.

---

## Questions?

This project was designed to be simple and self-contained. All code is in `app.py`. Study it to understand:
- Flask routing
- JSON file I/O
- REST API design
- LRU cache implementation
- Priority queue scheduling
- HTML form handling

Good luck! 🎉
