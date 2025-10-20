# Muse - Team 1 - API

✅ We checked our initial Supabase API using curl before building the following endpoints

Our main entities are users, posts, content, and creators

## What it does

Our API is built ot manage the interactions between users, user posts, creators, and creator content. We've built out some of the basic CRUD functions with business logic and validation built in along with error handling. In the future we plan to expand using the Next API rather than FastAPI, so here are the basic endpoints we built out.

The platform itself will allow users to create their own posts for platforms such as LinkedIn that take inspiration from other successful posts on other platforms from creators that they choose to follow.

## Setup

1. python3 -m venv .venv
2. source .venv/bin/activate
3. pip install -r requirements.txt
4. fastapi dev main.py
5. Test at http://127.0.0.1:8000/docs

## Endpoints (at a minimum)

### General Endpoint

- `GET /` - Test endpoint to see if everything is running

### User Endpoints

- `POST /users` - Create a new user object. Has business logic to check if it's a valid subscription type.
- `GET /users` - Return all of the users from the users table (these are the end users, not creators)
- `GET /users/[user_id]` - Returns the user object with that user_id
- `POST /users/follow` - Create a new follow record. Has business logic to not allow multiple follows for same person as well as follow limits by subscription tier.

### Posts Endpoints

- `POST /posts` - Create a new post with business logic integrated to rate limit
- `DELETE /posts/[post_id]` - Delete a post with that post_id
- `GET /posts/{post_id}` - Returns the information about a post with a specific post_id
- `GET /posts/user/{user_id}` - Return all posts by user_id

### Content Endpoints

- `POST /content` - Create a new piece of content, i.e a LinkedIn post, makes sure that URL is valid
- `GET /content/{content_id}` - Return content given its content_id, returns error if post does not exist
- `GET /content/creator/{creator_id}` - Returns all the content for a given creator_id

### Creator Endpoints

- `POST /creators` - Create a new piece of creator content. Makes sure that the profile URL is a valid URL. It also checks that their platform is allowed
- `GET /creators` - Returns all creators
- `GET /creators/{creator_id}` - Returns creator given creator_id

## Key Business Rule

Has strict rate limit of 10 post generation per week. For now this is for all users so that they don't make say 10,000 and crash our systems. In the future for a business model, it will serve as enticement to force the user to pay for a premium version of the model as X amount of posts is not sufficient to gain followers or get the post that most fits the message you want to get across.

We also included many other examples of business logic. We have examples of rate limiting and data validation for subscription tiers or other platforms or valid URLs. In the future we plan to add more, but plan to do so incrementally as we build the product to avoid any technical debt. These initial edits were made to create a strong foundation that we could build upon.

# Process

1. https://fastapi.tiangolo.com/#create-it
2. https://fastapi.tiangolo.com/tutorial/handling-errors/#raise-an-httpexception-in-your-code
3. https://supabase.com/docs/reference/python/introduction
