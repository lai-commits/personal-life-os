# Personal Life OS

A simple, local web application for quick thought logging throughout the day with unified analysis and integrated insights.

## What It Does

**New Design:** Instead of one big daily form, log quick thoughts as they happen, then review everything together at the end of the day.

- 💭 **Quick Thought Logging** (Throughout the Day): 
  - Log a thought in 10-30 seconds
  - Add mood and energy level
  - Submit and immediately ready for the next thought
  - All timestamped

- 📊 **Integrate & Review** (End of Day):
  - Button to pull ALL thoughts from today
  - Analyzes them together as a complete collection
  - Shows: integrated summary, emotional arc, themes, patterns
  - One consolidated view of your entire day's insight

- 🧠 **Smart Collection Analysis**:
  - Keywords and themes from ALL thoughts combined
  - Emotional arc throughout the day
  - Overarching patterns (anxiety, overwhelm, productivity, etc.)
  - Personalized recommendations based on full day context

- 📚 **History**: Review all past thoughts and reports

## Quick Start

### Prerequisites
- Python 3.7+
- That's it!

### Installation & Running

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   - Go to `http://localhost:5000`
   - Start logging thoughts!

## How to Use

### Throughout the Day: Log Quick Thoughts

1. Open the app (http://localhost:5000)
2. In the "Log a Thought" form:
   - Write your quick thought/observation (10-30 seconds)
   - Set your current mood (1-10)
   - Set your current energy (1-10)
3. Click "Log Thought & Continue"
4. Form clears, ready for the next thought
5. See all your thoughts listed with timestamps below

### End of Day: Integrate & Review

1. Once you've logged thoughts throughout the day, click "Integrate & Review Today"
2. See:
   - **Mood Range**: Your min/max mood and average for the day
   - **Energy Level**: Average energy
   - **Summary**: Overview of your day based on all thoughts
   - **Emotional Arc**: How your mood evolved through the day
   - **Main Themes**: Keywords and concepts across ALL thoughts (what you were thinking about)
   - **Recommendations**: Personalized suggestions based on your full day context

### Browsing History

1. Click "View History" to see all thoughts and past reports
2. Explore patterns over time

## Data Storage

- All data is stored locally in `mind_dumps.db` (SQLite database)
- No data is sent anywhere
- Completely private

## What Gets Analyzed

### Collection-Based Analysis
Unlike analyzing individual thoughts separately, the app analyzes ALL thoughts from a day together to find:

- **Keywords & Themes**: Most frequent meaningful words across all thoughts (what occupied your mind)
- **Emotional Arc**: How your mood evolved from first thought to last
- **Sentiment**: Overall tone of the entire day (positive/negative/neutral)

### Psychological Patterns
The app looks for signs of:
- **Anxiety**: worry, stress, panic, fear
- **Overwhelm**: feeling swamped, drowning, exhausted
- **Perfectionism**: should, must, flawless, ideal
- **Self-Doubt**: doubt, imposter, inadequate, insecure
- **Procrastination**: later, tomorrow, avoid, delay
- **Social Concerns**: loneliness, relationships, connection needs
- **Health Focus**: sleep, exercise, nutrition, wellness
- **Productivity**: work, tasks, deadlines, accomplishment
- **Growth Mindset**: learning, improvement, progress
- And more...

### Recommendations
Based on your full day's mood range, energy level, and detected patterns across all thoughts:
- Energy management tips (rest if low, tackle challenges if high)
- Mood support based on your emotional arc
- Pattern-specific advice (dealing with anxiety, overcoming perfectionism, etc.)
- Context-aware suggestions from the collection of thoughts

## Features

✅ Quick thought logging (10-30 seconds per entry)  
✅ Multiple entries per day with timestamps  
✅ Unified end-of-day integration and review  
✅ Collection-based analysis (not individual thought analysis)  
✅ Emotional arc tracking throughout the day  
✅ Zero-dependency setup (just pip install, then run)  
✅ Local SQLite database (all data private)  
✅ Beautiful, simple UI  
✅ Mobile-friendly  
✅ No sign-ups, no accounts, no cloud  

## Technical Details

- **Backend**: Python Flask
- **Database**: SQLite3 (thoughts table instead of dumps)
- **Frontend**: HTML/CSS/JavaScript (vanilla)
- **Analysis**: TextBlob (sentiment), keyword extraction, collection-wide pattern matching
- **No external APIs required** (for now - can add Claude API later for deeper analysis)

## API Endpoints

- `POST /api/thought` - Log a quick thought (text, mood, energy)
- `GET /api/thoughts/today` - Get all thoughts logged today
- `GET /api/integrate/daily` - Analyze & integrate all today's thoughts as a collection
- `GET /api/thoughts` - Get all thoughts (history)

## File Structure

```
personal-life-os/
├── app.py                 # Main Flask application
├── analysis.py            # Analysis functions
├── requirements.txt       # Python dependencies
├── mind_dumps.db          # SQLite database (created on first run)
├── templates/
│   ├── index.html         # Main form page
│   └── history.html       # History view
└── README.md              # This file
```

## Future Enhancements

Planned features:
- Integration with Claude API for deeper psychological insights
- Recurring pattern detection over time
- Weekly/monthly reports
- Tags for organizing dumps
- Search functionality
- Export to PDF
- Dark mode
- Mobile app version

## Troubleshooting

**Port already in use?**
```bash
python app.py
# The app runs on port 5000 by default. If it's in use, you can modify the port in app.py
```

**Database issues?**
```bash
# Delete the old database and start fresh
rm mind_dumps.db
python app.py
```

**Dependencies not installing?**
```bash
# Try upgrading pip first
pip install --upgrade pip
pip install -r requirements.txt
```

## Privacy

- All data stays on your computer
- No tracking, no analytics, no cloud sync
- Database file is just a local SQLite file you can inspect
- Complete privacy and control

## License

Open source for personal use.

---

**Made for Rachel's Personal Life OS**

Start dumping, start growing. 🚀
