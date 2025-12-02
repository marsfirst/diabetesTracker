# Diabetes Tracker - Presentation Slides

## Slide 1: Title Slide
**Diabetes Tracker: Simple & Accessible**
- A friendly web application for tracking blood sugar and meals
- Designed for older adults
- Built with Python Flask + vanilla JavaScript
- No complicated setup required

---

## Slide 2: The Problem
- Many diabetes apps are too complicated for older adults
- Cluttered interfaces, tiny fonts, confusing navigation
- Patients need simple, accessible tools
- Goal: Make tracking as easy as possible

---

## Slide 3: Our Solution
**Key Features:**
- Large fonts (18-24px) for easy reading
- Simple navigation with big buttons
- One-click access to core functions
- Friendly, encouraging language
- No medical jargon

---

## Slide 4: Core Features
1. **Log Blood Sugar** - Quick recording with suggestions
2. **Log Food** - Track meals throughout the day
3. **View History** - See all readings and meals sorted
4. **Get Recommendations** - Gentle suggestions based on readings
5. **Export Data** - Download readings as CSV

---

## Slide 5: Technical Architecture
```
Frontend (Static HTML/CSS/JS)
    ↓
REST API (Flask Backend)
    ↓
JSON Storage (Simple files, no database)
```

**Key Benefits:**
- No database setup needed
- Easy to understand and modify
- Runs locally (privacy-friendly)
- Single-file backend (app.py)

---

## Slide 6: Backend Structure

### Flask App (`app.py`)
- Serves static files (HTML/CSS/JS)
- Exposes JSON REST API
- Handles data persistence via JSON files
- Implements LRU Cache demo
- Implements Priority Scheduler demo

### Data Storage
- `data/readings.json` - Blood sugar readings
- `data/foods.json` - Food intake logs
- Created automatically on first run

---

## Slide 7: API Endpoints

### Core Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/readings` | GET/POST | List or add readings |
| `/api/suggestions` | POST | Get recommendations |
| `/api/login` | POST | Simple demo login |

### Educational Endpoints
| Endpoint | Purpose |
|----------|---------|
| `/api/cache` | LRU cache demo |
| `/api/scheduler` | Task scheduler demo |

---

## Slide 8: LRU Cache Demo (COA)
**What is an LRU Cache?**
- Stores frequently accessed data in fast memory
- When full, removes least recently used item
- Makes subsequent accesses faster

**Example:**
```
Cache capacity: 5 items
- Load reading #1 → stored
- Load reading #2 → stored
- Load reading #3 → stored
- Access reading #1 → HIT (refresh position)
- Load reading #4 → stored
- Load reading #5 → stored
- Load reading #6 → evict #3 (LRU), store #6
```

---

## Slide 9: Priority Scheduler Demo (COA)
**What is a Priority Scheduler?**
- Manages tasks based on urgency
- Higher priority (lower number) runs first
- Uses min-heap for efficient ordering

**Example:**
```
Task Queue (sorted by priority):
- Priority 1: Doctor reminder (urgent)
- Priority 3: Follow-up check
- Priority 7: General note
- Priority 9: Optional reading

Execution Order: 1 → 3 → 7 → 9
```

---

## Slide 10: User Interface Design

### Accessibility Features
- ✅ Large fonts (18-24px minimum)
- ✅ High contrast colors (dark text on light)
- ✅ Simple navigation (3 main buttons)
- ✅ Minimal scrolling
- ✅ Clear labels and instructions
- ✅ Friendly tone (no medical jargon)
- ✅ Medical disclaimer on every page

### Color Scheme
- **Primary Blue** (#0056b3) - Main actions
- **Primary Green** (#28a745) - Secondary actions
- **Warning Orange** (#ff9800) - Caution/disclaimer
- **Light Background** (#f8f9fa) - Reduces eye strain

---

## Slide 11: Page Walkthrough

### Home Page (`/`)
- Large welcome heading
- 6 action cards with big buttons
- Medical disclaimer
- Simple, clean layout

### Log Reading (`/add-reading`)
- Date/time auto-filled
- Simple number input for glucose
- Select context (before/after meal, fasting, bedtime)
- Personalized recommendation after submission

### View History (`/history`)
- Two tables: readings and meals
- Color-coded glucose levels
  - 🟢 Green (70-180) = normal
  - 🟡 Orange (< 70) = low
  - 🔴 Red (> 180) = high

---

## Slide 12: Quick Start (Windows)

```cmd
# 1. Create folder
mkdir %USERPROFILE%\diabetes_simple_json
cd %USERPROFILE%\diabetes_simple_json

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate

# 4. Install Flask
pip install -r requirements.txt

# 5. Run the app
python app.py

# 6. Open browser
http://127.0.0.1:5000/static/index.html
```

---

## Slide 13: File Structure
```
diabetes_simple_json/
├── app.py                    # All backend code
├── requirements.txt          # Flask dependency
├── README.md                # Full documentation
├── data/                    # JSON storage (auto-created)
│   ├── readings.json
│   └── foods.json
└── static/
    ├── index.html           # Home page
    ├── add_reading.html     # Log glucose
    ├── add_food.html        # Log meal
    ├── history.html         # View history
    ├── cache.html           # Cache demo
    ├── scheduler.html       # Scheduler demo
    ├── css/
    │   └── style.css        # Accessibility styles
    └── js/
        ├── main.js          # Core functions
        ├── cache.js         # Cache demo logic
        └── scheduler.js     # Scheduler demo logic
```

---

## Slide 14: Sample Data Format

### Readings
```json
{
  "id": 1,
  "user_id": 1,
  "glucose": 145.5,
  "context": "post-meal",
  "meal": "lunch",
  "note": "felt good",
  "created_at": "2025-11-28T12:30:00Z"
}
```

### Recommendations by Level
- **> 250**: Very high → Consider doctor visit
- **180-250**: High → Light activity, hydration
- **70-180**: Normal → Keep monitoring
- **< 70**: Low → Fast carbs, recheck soon

---

## Slide 15: Key Design Decisions

| Decision | Why |
|----------|-----|
| JSON instead of SQL | Simpler for beginners, no DB setup |
| Flask not Django | Lightweight, easy to understand |
| Vanilla JS not React | No build tools, less complexity |
| Single app.py file | All backend code in one place |
| LRU + Scheduler demos | Teach CS306 concepts hands-on |

---

## Slide 16: Educational Value

### For Patients
- Simple, easy-to-use diabetes tracking
- Personalized, friendly recommendations
- Privacy (runs locally, no cloud)

### For CS Students (Computer Organization & Architecture)
- **Caching**: Understand memory hierarchies, LRU replacement
- **Scheduling**: Learn priority-based task management
- **REST APIs**: Understand backend/frontend separation
- **JSON**: Work with structured data persistence
- **Flask**: Build web services quickly

---

## Slide 17: Extending the App

### Possible Enhancements
1. **Real database** (SQLite, PostgreSQL)
2. **User authentication** (hashed passwords)
3. **Analytics** (charts, trends, reports)
4. **Mobile app** (React Native)
5. **Notifications** (email/SMS alerts)
6. **Wearable integration** (Fitbit, Apple Watch)

### For COA Students
1. **L1/L2/L3 cache simulation**
2. **Different scheduling algorithms** (Round-Robin, FCFS, SJF)
3. **Memory management** (page replacement, virtual memory)
4. **Interrupt handling** (simulated IRQ system)

---

## Slide 18: Live Demo Walkthrough

1. ✅ Start the server (`python app.py`)
2. ✅ Open the home page
3. ✅ Walk through adding a reading
4. ✅ Show the recommendation
5. ✅ View history with color-coded levels
6. ✅ Demo cache with readings 1-6
7. ✅ Demo scheduler with priority tasks

---

## Slide 19: Benefits Summary

✅ **For Patients:**
- Accessible (large fonts, simple interface)
- Friendly (encouraging tone, no jargon)
- Private (runs locally)
- Easy (minimal learning curve)

✅ **For Developers:**
- Simple codebase (single Python file)
- Educational (COA concepts included)
- Extensible (easy to add features)
- Professional (proper architecture)

✅ **For Teachers:**
- Real-world application (healthcare context)
- Multiple learning outcomes (web dev + CS concepts)
- Hands-on demos (interactive endpoints)
- Modular design (easy to teach incrementally)

---

## Slide 20: Conclusion

**Diabetes Tracker** demonstrates:
- 🩺 **Real-world problem**: Accessible health tracking
- 💻 **Technical solution**: Flask backend + vanilla frontend
- 🎓 **Educational concepts**: Caching, scheduling, REST APIs
- ♿ **Accessibility**: Designed for older adults
- 📚 **Learning value**: Great for CS306 students

**Get started in 5 minutes!**
Follow the README.md for Windows setup instructions.

---

## Questions?

**Repository**: This project is designed to be studied and extended.

**For help:**
1. Check README.md for troubleshooting
2. Read comments in app.py
3. Test endpoints in cache.html / scheduler.html
4. Modify and experiment!

**Key takeaway:** A well-designed app combines accessibility, simplicity, and educational value. 🎉
