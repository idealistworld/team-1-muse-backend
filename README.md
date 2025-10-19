# Muse - Team 1 - API

## What it does
Our API manages a content creation platform (LinkedIn, X, etc)
Users can follow creators and generate AI generated posts as they interact with creator content

## Setup

1. python3 -m venv .venv
2. source .venv/bin/activate
3. pip3 install "fastapi[standard]" uvicorn supabase psycopg2-binary python-dotenv
4. fastapi dev main.py

## Endpoints (at a minimum)

- `GET /[entity]` - List all
- `POST /[entity]` - Create new

## Key business Rule
Has strict rate limit of 10 post generation per week. For now this is for all users so that they don't make say 10,000 and crash our systems. In the future for a business model, it will serve as enticement to force the user to pay for a premium version of the model as X amount of posts is not sufficient to gain followers or get the post that most fits the message you want to get accross. 
# Process

1. https://fastapi.tiangolo.com/#create-it
2. https://supabase.com/docs/reference/python/introduction
