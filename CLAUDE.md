# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI backend that scrapes YouTube video comments via the YouTube Data API v3 and classifies them using Google Gemini 2.5 Flash (via Vertex AI) into POSITIVE, NEGATIVE, or GARBAGE categories with summaries and importance scores.

## Commands

### Run the server
```bash
uvicorn app.main:app --reload
```

### Run a single request (test the API)
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

### Health check
```bash
curl http://localhost:8000/health
```

There is no test suite or linter configured.

## Environment Variables

Required in `.env`:
- `YT_API_KEY` — YouTube Data API v3 key
- `GEMINI_API_KEY` — Google Generative AI key
- `PROJECT_ID` — Google Cloud project ID
- `LOCATION` — Google Cloud region (e.g. `us-central1`)

## Architecture

**Entry point:** `app/main.py` — creates the FastAPI app and mounts the router from `app/routes/analyze.py`.

**Data flow for `POST /api/analyze`:**
1. `app/routes/analyze.py` receives a YouTube URL
2. `app/scraper.py` — `parse_video_id()` extracts the video ID, then `get_video_comments()` paginates through the YouTube API, fetches replies via `get_all_replies()`, and filters out the channel owner's own comments
3. `app/classifier.py` — `classify_comments()` batches comments 10 at a time and calls Gemini 2.5 Flash to assign each a category (ACTIONABLE/SUPPORTIVE/IRRELEVANT), a one-sentence summary, and an importance level (HIGH/MEDIUM/LOW based on like count thresholds); `save_response()` exports results to `output/results.csv`
4. Response is returned as JSON matching the `AnalyzeResponse` schema

**Schemas:** `app/schemas.py` defines `AnalyzeRequest`, `CommentResult`, and `AnalyzeResponse` (Pydantic models).

**Known issues:**
- There is a duplicate/legacy route file at `routes/analyze.py` (top-level) that is not used by the app
- `GET /api/results/{video_id}` in `main.py` is a stub with no real implementation
- The `ModelName` enum in `main.py` is unused
