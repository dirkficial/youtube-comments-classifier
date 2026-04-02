# YouTube Comment Classifier

A REST API that scrapes YouTube video comments and uses AI to classify them into actionable feedback, supportive messages, or irrelevant noise — helping creators cut through the clutter and focus on what actually matters.

## What it does

Submit any YouTube URL and get back every comment classified as:

- **ACTIONABLE** : specific feedback the creator can act on (e.g. "the audio drops after the intro", "the explanation at 3:20 really clicked for me")
- **SUPPORTIVE** : positive engagement with no specific takeaway (e.g. "great video!", "love your content")
- **IRRELEVANT** : spam, memes, off-topic arguments, self-promotion

Each comment also gets a one-sentence summary and an importance score (HIGH / MEDIUM / LOW) based on its like count relative to the video's most-liked comment.

## Tech Stack

| Layer | Technology |
|---|---|
| API framework | FastAPI |
| Database | PostgreSQL via SQLAlchemy ORM |
| AI classification | Google Gemini 2.5 Flash (Vertex AI) |
| Comment scraping | YouTube Data API v3 |
| Validation | Pydantic v2 |
| Runtime | Python 3.12, Uvicorn |
| Containerization | Docker, Docker Compose |

## Project Structure

```
app/
├── main.py              # FastAPI app setup, lifespan (DB init)
├── db.py                # SQLAlchemy engine, session, Base
├── models.py            # ORM models: User, Analysis, Comment
├── schemas.py           # Pydantic request/response schemas
├── scraper.py           # YouTube API: fetch comments + replies
├── classifier.py        # Gemini batched classification logic
└── routes/
    ├── analyze.py       # POST /api/analyze
    ├── results.py       # GET  /api/results/{video_id}
    └── users.py         # POST /api/users
```

## API Endpoints

### `POST /api/analyze`
Scrape and classify comments for a YouTube video.

**Request**
```json
{ "url": "https://www.youtube.com/watch?v=VIDEO_ID" }
```

**Response**
```json
{
  "video_id": "VIDEO_ID",
  "total_comments": 250,
  "actionable": 42,
  "supportive": 130,
  "irrelevant": 78,
  "comments": [
    {
      "comment_text": "The mic quality dropped around the 5 minute mark",
      "like_count": 312,
      "reply_count": 4,
      "category": "ACTIONABLE",
      "summary": "Viewer noticed audio quality issues at the 5-minute mark.",
      "importance": "HIGH"
    }
  ]
}
```

### `GET /api/results/{video_id}`
Retrieve a previously stored analysis from the database.

### `POST /api/users`
Register a new user account.

### `GET /health`
Health check returns `{ "status": "ok" }`.

## Setup

### Prerequisites
- Google Cloud project with Vertex AI enabled
- YouTube Data API v3 key

### Environment Variables

Create a `.env` file:

```
YT_API_KEY=your_youtube_data_api_key
GEMINI_API_KEY=your_gemini_api_key
PROJECT_ID=your_gcp_project_id
LOCATION=us-central1
DATABASE_URL=postgresql://postgres:password@db:5432/youtubedb
```

### Run with Docker (recommended)

The app runs as two containers — the FastAPI server and a PostgreSQL 16 database — managed by Docker Compose. The database password is read from `db/password.txt` as a Docker secret.

1. Create the password file:
   ```bash
   mkdir -p db && echo "your_db_password" > db/password.txt
   ```

2. Start the services:
   ```bash
   docker compose up --build
   ```

The server starts at `http://localhost:8000`. Interactive API docs are available at `http://localhost:8000/docs`.

### Run locally (without Docker)

Additional prerequisites: Python 3.12+, PostgreSQL

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Data Model

```
User ──< Analysis ──< Comment
```

Each `Analysis` is tied to a video ID and timestamps when it was run. Each `Comment` stores the raw text, like/reply counts, AI-assigned category, summary, and importance level.

## What I Learned

This project was built to learn **FastAPI** and **PostgreSQL**:

- Structuring a FastAPI app with routers, dependency injection, and lifespan events
- Defining SQLAlchemy ORM models with typed `Mapped` columns and relationships
- Using Pydantic v2 for request validation and response serialization
- Managing database sessions safely with a generator-based `get_db` dependency
- Paginating through a third-party API (YouTube) and filtering results before storing them
- Batching LLM prompts to stay within token limits while processing large comment threads
