# Mind Dump App - API Examples

## Quick Reference for API Endpoints

### 1. Log a Quick Thought
```
POST /api/thought
Content-Type: application/json

{
  "text": "Feeling productive today, made good progress on the design",
  "mood": 7,
  "energy": 8
}

Response (201 Created):
{
  "success": true,
  "id": 1,
  "message": "Thought logged successfully!"
}
```

### 2. Get Today's Thoughts List
```
GET /api/thoughts/today

Response (200 OK):
{
  "success": true,
  "thoughts": [
    {
      "id": 1,
      "text": "Feeling productive today...",
      "mood": 7,
      "energy": 8,
      "created_at": "2026-04-10 14:23:15"
    },
    {
      "id": 2,
      "text": "Getting tired, might wrap up soon",
      "mood": 6,
      "energy": 5,
      "created_at": "2026-04-10 17:45:32"
    }
  ],
  "count": 2
}
```

### 3. Integrate & Review Today (MAIN ENDPOINT)
```
GET /api/integrate/daily

Response (200 OK):
{
  "date": "2026-04-10",
  "thoughts_count": 2,
  "summary": "You recorded 2 thoughts today. Overall tone was balanced and neutral. Your day ranged from mood 6/10 to 7/10.",
  "emotional_arc": "Mood remained stable throughout the day",
  "mood_average": 6.5,
  "energy_average": 6.5,
  "themes": [
    {
      "name": "Design",
      "frequency": 1
    },
    {
      "name": "Progress",
      "frequency": 1
    }
  ],
  "recommendations": [
    "Continue documenting your thoughts - awareness is the foundation for growth."
  ],
  "patterns": [
    {
      "name": "Productivity",
      "strength": "moderate"
    }
  ],
  "all_thoughts": [
    {
      "id": 1,
      "text": "Feeling productive today...",
      "mood": 7,
      "energy": 8,
      "created_at": "2026-04-10 14:23:15",
      "sentiment": "positive"
    },
    {
      "id": 2,
      "text": "Getting tired, might wrap up soon",
      "mood": 6,
      "energy": 5,
      "created_at": "2026-04-10 17:45:32",
      "sentiment": "neutral"
    }
  ]
}
```

### 4. Get All Thoughts (History)
```
GET /api/thoughts

Response (200 OK):
{
  "success": true,
  "thoughts": [
    {
      "id": 2,
      "text": "Getting tired...",
      "mood": 6,
      "energy": 5,
      "created_at": "2026-04-10 17:45:32",
      ...
    },
    {
      "id": 1,
      "text": "Feeling productive...",
      "mood": 7,
      "energy": 8,
      "created_at": "2026-04-10 14:23:15",
      ...
    }
  ]
}
```

## Key Differences from Old API

### Old Flow (❌ Removed)
```
POST /api/dump  →  GET /api/report/daily
(One big form)    (Analyze individually)
```

### New Flow (✅ Current)
```
POST /api/thought  →  GET /api/thoughts/today  →  GET /api/integrate/daily
(Quick logging)       (See list)                (Unified analysis)
```

## Integration Report Structure

The `/api/integrate/daily` endpoint returns everything needed for the unified daily report:

```javascript
{
  // Basic Info
  "date": "YYYY-MM-DD",
  "thoughts_count": number,
  
  // Unified Summary
  "summary": "Human-readable narrative of the whole day",
  "emotional_arc": "Mood improved/declined/remained stable",
  
  // Statistics
  "mood_average": number (1-10),
  "energy_average": number (1-10),
  
  // Themes from All Thoughts Combined
  "themes": [
    {
      "name": "keyword",
      "frequency": number
    }
  ],
  
  // Smart Recommendations
  "recommendations": ["recommendation 1", "recommendation 2"],
  
  // Psychological Patterns Detected
  "patterns": [
    {
      "name": "Pattern Name",
      "strength": "high|moderate"
    }
  ],
  
  // Raw Data for Reference
  "all_thoughts": [
    {
      "id": number,
      "text": "thought content",
      "mood": number,
      "energy": number,
      "created_at": "ISO timestamp",
      "sentiment": "positive|negative|neutral"
    }
  ]
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- **201 Created**: Thought successfully logged
- **200 OK**: Data retrieved successfully
- **400 Bad Request**: Missing required fields
- **500 Internal Server Error**: Server error

Example error response:
```json
{
  "error": "Thought text is required"
}
```

## Frontend Usage Pattern

The frontend (index.html) uses these endpoints like this:

1. **Page Load**: Call `GET /api/thoughts/today` → display list
2. **User Submits Thought**: Call `POST /api/thought` → reset form
3. **User Clicks Integrate**: Call `GET /api/integrate/daily` → show report
4. **View History Link**: Navigate to `/history` (uses `GET /api/thoughts`)

## Testing with curl

```bash
# Log a thought
curl -X POST http://localhost:5000/api/thought \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Testing the API",
    "mood": 5,
    "energy": 5
  }'

# Get today's thoughts
curl http://localhost:5000/api/thoughts/today

# Get integrated report
curl http://localhost:5000/api/integrate/daily
```

## Collection Analysis Details

The `/api/integrate/daily` endpoint's collection analysis differs from old individual analysis:

**Old**: Each thought analyzed separately
- Keywords from that one thought
- Sentiment of that one thought
- Patterns from that one thought

**New**: All thoughts analyzed together
- Keywords from the day as a whole (what you thought about most)
- Overall sentiment (positive/negative/neutral across all thoughts)
- Patterns showing overarching themes
- Emotional arc showing mood progression
- One coherent summary of your entire day

This gives Rachel the unified, integrated view she requested!
