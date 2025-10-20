# Muse - Team 1 - API

✅ We checked our initial Supabase API using curl before building the following endpoints

Our main entities are users, posts, content, and creators

## What it does

Our API manages a content creation platform (LinkedIn, X, etc)
Users can follow creators and generate AI generated posts as they interact with creator content

## Setup

1. python3 -m venv .venv
2. source .venv/bin/activate
3. pip3 install "fastapi[standard]" uvicorn supabase python-dotenv pydantic
   OR
   pip install -r requirements.txt
4. fastapi dev main.py

## Endpoints (at a minimum)

### General Endpoint

- `GET /` - Test endpoint to see if everything is running

### User Endpoints

- `POST /users` - Create a new user object
- `GET /users` - Return all of the users from the users table (these are the end users, not creators)
- `GET /users/[user_id]` - Returns the user object with that user_id
- `POST /users/follow` - Create a new follow record. Has business logic to not allow multiple follows for same person as well as follow limits by subscription tier.

### Posts Endpoints

- `POST /posts` - Create a new post with business logic integrated to rate limit
- `DELETE /posts/[post_id]` - Delete a post with that post_id

### Content Endpoints

- `POST /content` - Create a new piece of content, i.e a LinkedIn post

### Creator Endpoints

- `POST /creators/content` - Create a new piece of creator content

## Key Business Rule

Has strict rate limit of 10 post generation per week. For now this is for all users so that they don't make say 10,000 and crash our systems. In the future for a business model, it will serve as enticement to force the user to pay for a premium version of the model as X amount of posts is not sufficient to gain followers or get the post that most fits the message you want to get across.

# Process

1. https://fastapi.tiangolo.com/#create-it
2. https://fastapi.tiangolo.com/tutorial/handling-errors/#raise-an-httpexception-in-your-code
3. https://supabase.com/docs/reference/python/introduction
