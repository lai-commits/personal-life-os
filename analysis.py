"""
Analysis module for extracting insights from mind dumps
Uses basic NLP techniques for keyword extraction and sentiment analysis
"""

import re
from collections import Counter
from textblob import TextBlob

# Common stop words to filter out
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
    'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
    'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both',
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 'my', 'me', 'him',
    'her', 'his', 'their', 'your', 'our', 'just', 'also', 'being', 'if',
    'because', 'while', 'through', 'during', 'before', 'after', 'above',
    'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again', 'further',
    'then', 'once', 'here', 'there', 'about', 'am', 'don', 'doesn', 'hadn',
    'hasn', 'haven', 'isn', 'shouldn', 'wasn', 'weren', 'won', 'wouldn',
    'it', 'its'
}

def extract_keywords(text, top_n=10):
    """
    Extract keywords from text using frequency analysis
    Filters out stop words and common words
    """
    # Convert to lowercase and extract words
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())

    # Filter stop words
    filtered_words = [w for w in words if w not in STOP_WORDS]

    # Count frequencies
    word_freq = Counter(filtered_words)

    # Return top keywords with their frequencies
    keywords = word_freq.most_common(top_n)
    return [{'word': w, 'count': c} for w, c in keywords]

def analyze_sentiment(text):
    """
    Analyze sentiment of text
    Returns: positive, negative, or neutral
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'

def identify_psychological_patterns(text, keywords):
    """
    Identify psychological patterns based on keywords and text analysis
    """
    patterns = []
    text_lower = text.lower()

    # Pattern definitions
    pattern_rules = {
        'anxiety': ['worry', 'anxious', 'nervous', 'stress', 'panic', 'afraid', 'fear', 'overwhelming'],
        'overwhelm': ['overwhelmed', 'too much', 'can\'t handle', 'drowning', 'stressed', 'exhausted'],
        'perfectionism': ['perfect', 'should', 'must', 'flawless', 'ideal', 'mistake', 'failure'],
        'self_doubt': ['doubt', 'not good enough', 'imposter', 'inadequate', 'insecure', 'unworthy'],
        'procrastination': ['later', 'tomorrow', 'eventually', 'delay', 'avoid', 'put off', 'postpone'],
        'social_concerns': ['people', 'social', 'alone', 'lonely', 'friend', 'relationship', 'connection'],
        'health_focus': ['tired', 'sleep', 'health', 'sick', 'exercise', 'eat', 'body', 'pain'],
        'productivity': ['work', 'productive', 'accomplish', 'deadline', 'project', 'task', 'done'],
        'emotional_intensity': ['angry', 'furious', 'heartbroken', 'devastated', 'ecstatic', 'amazing'],
        'growth_mindset': ['learn', 'improve', 'grow', 'challenge', 'opportunity', 'develop', 'progress']
    }

    # Check for pattern matches
    for pattern_name, keywords_list in pattern_rules.items():
        matches = sum(1 for kw in keywords_list if kw in text_lower)
        if matches >= 2:  # At least 2 keywords match
            patterns.append({
                'name': pattern_name.replace('_', ' ').title(),
                'strength': 'high' if matches >= 3 else 'moderate'
            })

    return patterns

def analyze_dump(text):
    """
    Analyze a mind dump and extract insights
    Returns: keywords, sentiment, patterns
    """
    keywords = extract_keywords(text)
    sentiment = analyze_sentiment(text)

    # Extract just the words from keywords for pattern analysis
    keyword_words = [kw['word'] for kw in keywords]
    patterns = identify_psychological_patterns(text, keyword_words)

    return {
        'keywords': keywords,
        'sentiment': sentiment,
        'patterns': patterns
    }

def generate_daily_report(dumps_data):
    """
    Generate a daily report summarizing all dumps and patterns
    """
    if not dumps_data:
        return {
            'summary': 'No mind dumps recorded yet today.',
            'patterns': [],
            'recommendation': 'Start by recording your first mind dump!'
        }

    # Calculate averages
    moods = [d['mood'] for d in dumps_data if d['mood']]
    energies = [d['energy'] for d in dumps_data if d['energy']]

    mood_avg = sum(moods) / len(moods) if moods else 5
    energy_avg = sum(energies) / len(energies) if energies else 5

    # Aggregate all patterns
    all_patterns = {}
    for dump in dumps_data:
        patterns_str = dump.get('patterns', '[]')
        if isinstance(patterns_str, str):
            import json
            try:
                patterns = json.loads(patterns_str)
                for p in patterns:
                    name = p.get('name', 'Unknown')
                    if name not in all_patterns:
                        all_patterns[name] = 0
                    all_patterns[name] += 1
            except:
                pass

    # Sort patterns by frequency
    top_patterns = sorted(all_patterns.items(), key=lambda x: x[1], reverse=True)[:5]

    # Aggregate sentiments
    sentiments = [d.get('sentiment', 'neutral') for d in dumps_data]
    sentiment_counts = Counter(sentiments)
    dominant_sentiment = sentiment_counts.most_common(1)[0][0] if sentiment_counts else 'neutral'

    # Generate summary
    num_dumps = len(dumps_data)
    summary = f"You recorded {num_dumps} mind dump{'s' if num_dumps != 1 else ''} today. "

    if dominant_sentiment == 'positive':
        summary += "Overall mood was quite positive."
    elif dominant_sentiment == 'negative':
        summary += "Overall mood was more challenging - be gentle with yourself."
    else:
        summary += "Overall mood was balanced and neutral."

    summary += f" Average mood: {mood_avg:.1f}/10, Energy: {energy_avg:.1f}/10."

    # Generate recommendation based on energy and mood
    recommendation = generate_recommendation(mood_avg, energy_avg, top_patterns)

    return {
        'summary': summary,
        'patterns': [{'name': p[0], 'count': p[1]} for p in top_patterns],
        'recommendation': recommendation,
        'mood_average': round(mood_avg, 1),
        'energy_average': round(energy_avg, 1)
    }

def generate_recommendation(mood_avg, energy_avg, patterns):
    """
    Generate personalized recommendations based on mood, energy, and patterns
    """
    recommendations = []

    # Energy recommendations
    if energy_avg < 4:
        recommendations.append("Your energy is low - prioritize rest, sleep, and gentle activities today.")
    elif energy_avg > 7:
        recommendations.append("You have good energy - use it for important tasks or challenging projects.")

    # Mood recommendations
    if mood_avg < 4:
        recommendations.append("Your mood needs attention - consider a walk, time with loved ones, or creative outlet.")
    elif mood_avg > 7:
        recommendations.append("You're feeling great - share this energy with others or tackle something meaningful.")

    # Pattern-based recommendations
    pattern_names = [p[0].lower() for p in patterns]

    if 'anxiety' in pattern_names:
        recommendations.append("Consider grounding techniques or breathing exercises to manage anxiety.")

    if 'overwhelm' in pattern_names:
        recommendations.append("Break tasks into smaller steps - focus on one thing at a time.")

    if 'procrastination' in pattern_names:
        recommendations.append("Use the 2-minute rule: commit to just 2 minutes on a task you're avoiding.")

    if 'perfectionism' in pattern_names:
        recommendations.append("Remember: done is better than perfect. Aim for progress, not perfection.")

    if 'self_doubt' in pattern_names:
        recommendations.append("Write down 3 things you did well today - combat self-doubt with evidence of your capability.")

    if 'social_concerns' in pattern_names:
        recommendations.append("Reach out to someone you trust - connection often helps.")

    if 'health_focus' in pattern_names:
        recommendations.append("Pay attention to sleep, movement, and nutrition - they fuel everything else.")

    # If no specific recommendations, give a general one
    if not recommendations:
        recommendations.append("Continue reflecting on your patterns - awareness is the first step to growth.")

    return " ".join(recommendations[:2])  # Return top 2 recommendations

def analyze_collection(thoughts_data):
    """
    Analyze a COLLECTION of thoughts as a whole, not individually.
    Identifies patterns, themes, and emotional arc throughout the day.
    """
    if not thoughts_data:
        return {
            'summary': 'No thoughts recorded yet today.',
            'emotional_arc': 'N/A',
            'themes': [],
            'recommendations': [],
            'mood_average': 0,
            'energy_average': 0
        }

    # Calculate averages
    moods = [d['mood'] for d in thoughts_data if d['mood']]
    energies = [d['energy'] for d in thoughts_data if d['energy']]

    mood_avg = sum(moods) / len(moods) if moods else 5
    energy_avg = sum(energies) / len(energies) if energies else 5

    # Combine all text for overall analysis
    all_text = ' '.join([d['text'] for d in thoughts_data])

    # Extract top keywords from all thoughts combined
    all_keywords = extract_keywords(all_text, top_n=15)
    keyword_words = [kw['word'] for kw in all_keywords]

    # Identify patterns from the whole collection
    all_patterns = identify_psychological_patterns(all_text, keyword_words)

    # Determine emotional arc by analyzing mood progression
    mood_progression = [d['mood'] for d in thoughts_data]
    if len(mood_progression) > 1:
        if mood_progression[-1] > mood_progression[0]:
            arc = "Mood improved throughout the day"
        elif mood_progression[-1] < mood_progression[0]:
            arc = "Mood declined throughout the day"
        else:
            arc = "Mood remained stable throughout the day"
    else:
        arc = "Single thought recorded"

    # Extract main themes from keywords
    themes = []
    for kw in all_keywords[:8]:  # Top 8 keywords as themes
        themes.append({
            'name': kw['word'].capitalize(),
            'frequency': kw['count']
        })

    # Generate integrated summary
    num_thoughts = len(thoughts_data)
    summary = f"You recorded {num_thoughts} thought{'s' if num_thoughts != 1 else ''} today. "

    # Analyze sentiment across all thoughts
    sentiments = []
    for d in thoughts_data:
        sentiment_str = d.get('sentiment', 'neutral')
        sentiments.append(sentiment_str)

    sentiment_counts = Counter(sentiments)
    dominant_sentiment = sentiment_counts.most_common(1)[0][0] if sentiment_counts else 'neutral'

    if dominant_sentiment == 'positive':
        summary += "Overall tone was quite positive."
    elif dominant_sentiment == 'negative':
        summary += "Overall tone was challenging - be gentle with yourself."
    else:
        summary += "Overall tone was balanced and neutral."

    summary += f" Your day ranged from mood {min(mood_progression)}/10 to {max(mood_progression)}/10."

    # Generate recommendations based on collection analysis
    recommendations = []

    if energy_avg < 4:
        recommendations.append("Your energy is low - prioritize rest and gentle activities.")
    elif energy_avg > 7:
        recommendations.append("You have good energy - channel it into meaningful work.")

    if mood_avg < 4:
        recommendations.append("Your mood needs care - consider self-compassion practices.")
    elif mood_avg > 7:
        recommendations.append("You're in a great mental space - share this positivity.")

    # Pattern-based recommendations
    pattern_names = [p['name'].lower() for p in all_patterns]

    if 'anxiety' in pattern_names:
        recommendations.append("Grounding exercises or breathing work could help with the anxiety themes you mentioned.")

    if 'overwhelm' in pattern_names:
        recommendations.append("Break things into smaller, manageable steps.")

    if 'productivity' in pattern_names:
        recommendations.append("You're thinking about tasks - prioritize the most important ones.")

    if not recommendations:
        recommendations.append("Continue documenting your thoughts - awareness is the foundation for growth.")

    return {
        'summary': summary,
        'emotional_arc': arc,
        'themes': themes,
        'recommendations': recommendations,
        'mood_average': round(mood_avg, 1),
        'energy_average': round(energy_avg, 1),
        'patterns': all_patterns
    }
