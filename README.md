# Muse - Team 1 - API

## What it does
Our API manages a content creation platform (LinkedIn, X, etc)
Users can follow creators and generate AI generated posts as they interact with creator content. 
Has strict rate limits depending on the user's usage and prevents duplicate follows. 
## Setup

1. python3 -m venv .venv
2. source .venv/bin/activate
3. pip3 install "fastapi[standard]" uvicorn supabase psycopg2-binary python-dotenv
4. fastapi dev main.py

## Endpoints (at a minimum)

- `GET /[entity]` - List all
- `POST /[entity]` - Create new

## Key business Rule

# Process

1. https://fastapi.tiangolo.com/#create-it
2. https://supabase.com/docs/reference/python/introduction
