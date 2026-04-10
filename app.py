from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime, timedelta
import json
from pathlib import Path
import pytz
from analysis import analyze_dump, generate_daily_report, analyze_collection

app = Flask(__name__)

# Set timezone to Hong Kong
HK_TZ = pytz.timezone('Asia/Hong_Kong')

# Database setup
DB_PATH = 'mind_dumps.db'

def init_db():
    """Initialize database with schema"""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE thoughts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                text TEXT NOT NULL,
                mood INTEGER,
                energy INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                keywords TEXT,
                sentiment TEXT,
                patterns TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized successfully!")

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Serve the main form"""
    return render_template('index.html')

@app.route('/api/thought', methods=['POST'])
def create_thought():
    """Quick thought logging - 10-30 seconds"""
    try:
        data = request.get_json()

        # Extract minimal form data
        text = data.get('text', '').strip()
        mood = data.get('mood', 5)
        energy = data.get('energy', 5)

        if not text:
            return jsonify({'error': 'Thought text is required'}), 400

        # Analyze the individual thought
        analysis = analyze_dump(text)

        # Store in database
        conn = get_db()
        c = conn.cursor()
        today = datetime.now(HK_TZ).strftime('%Y-%m-%d')

        c.execute('''
            INSERT INTO thoughts
            (date, text, mood, energy, keywords, sentiment, patterns)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            today,
            text,
            int(mood),
            int(energy),
            json.dumps(analysis['keywords']),
            analysis['sentiment'],
            json.dumps(analysis['patterns'])
        ))

        conn.commit()
        thought_id = c.lastrowid
        conn.close()

        return jsonify({
            'success': True,
            'id': thought_id,
            'message': 'Thought logged successfully!'
        }), 201

    except Exception as e:
        print(f"Error logging thought: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/integrate/daily', methods=['GET'])
def get_daily_integration():
    """Integrate & Review all today's thoughts as a collection"""
    try:
        conn = get_db()
        c = conn.cursor()

        # Get today's thoughts
        today = datetime.now(HK_TZ).strftime('%Y-%m-%d')
        c.execute('''
            SELECT * FROM thoughts WHERE date = ? ORDER BY created_at
        ''', (today,))

        thoughts = c.fetchall()
        conn.close()

        if not thoughts:
            return jsonify({
                'date': today,
                'thoughts_count': 0,
                'summary': 'No thoughts recorded yet today.',
                'emotional_arc': 'N/A',
                'themes': [],
                'recommendations': [],
                'mood_average': 0,
                'energy_average': 0,
                'all_thoughts': []
            }), 200

        # Convert to list of dicts for analysis
        thoughts_data = [dict(row) for row in thoughts]

        # Analyze the COLLECTION as a whole
        report = analyze_collection(thoughts_data)

        return jsonify({
            'date': today,
            'thoughts_count': len(thoughts),
            'summary': report['summary'],
            'emotional_arc': report['emotional_arc'],
            'themes': report['themes'],
            'recommendations': report['recommendations'],
            'mood_average': report['mood_average'],
            'energy_average': report['energy_average'],
            'all_thoughts': thoughts_data
        }), 200

    except Exception as e:
        print(f"Error generating integration: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/thoughts/today', methods=['GET'])
def get_today_thoughts():
    """Get all thoughts logged today"""
    try:
        conn = get_db()
        c = conn.cursor()

        today = datetime.now(HK_TZ).strftime('%Y-%m-%d')
        c.execute('''
            SELECT id, text, mood, energy, created_at FROM thoughts
            WHERE date = ? ORDER BY created_at DESC
        ''', (today,))

        thoughts = [dict(row) for row in c.fetchall()]
        conn.close()

        return jsonify({
            'success': True,
            'thoughts': thoughts,
            'count': len(thoughts)
        }), 200

    except Exception as e:
        print(f"Error fetching thoughts: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/thoughts', methods=['GET'])
def get_all_thoughts():
    """Get all thoughts for history"""
    try:
        conn = get_db()
        c = conn.cursor()

        c.execute('SELECT * FROM thoughts ORDER BY created_at DESC LIMIT 50')
        thoughts = [dict(row) for row in c.fetchall()]

        conn.close()

        return jsonify({
            'success': True,
            'thoughts': thoughts
        }), 200

    except Exception as e:
        print(f"Error fetching thoughts: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    """View dump history"""
    return render_template('history.html')

if __name__ == '__main__':
    init_db()
    print("\n" + "="*60)
    print("Personal Life OS is starting up!")
    print("="*60)
    print("Open your browser to: http://localhost:5000")
    print("="*60 + "\n")
    # For local use: debug=True, port=5000
    # For cloud deployment: debug=False, host=0.0.0.0
    debug_mode = os.getenv('DEBUG', 'True') == 'True'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
