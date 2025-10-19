from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import uuid

# Supabase
import psycopg2
from dotenv import load_dotenv
import os
from supabase import create_client, Client
#for the ratelimit feature
from datetime import datetime

app = FastAPI()

# Load environment variables from .env
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# API Routes

@app.get("/")
def read_root():
    return ("Hello World")

# User Routes

@app.get("/users")
def get_all_users():
    try:
        response = (
            supabase.table("user_profiles")
            .select("*")
            .execute()
        )
        return {"code": 200, "response": response.data}

    except Exception as e:
        print(f"Error: {e}")


@app.get("/users/{user_id}")
def get_user_by_id(user_id: str):
    try:
        response = (
            supabase.table("user_profiles")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return {"code": 200, "response": response.data}

    except Exception as e:
        print(f"Error: {e}")


# Type Declaration for Endpoint
class CreateUserModel(BaseModel):
    subscription_tier: str

@app.post("/users/")
def create_new_user(user: CreateUserModel):
    try:
        response = (
            supabase.table("user_profiles")
            .insert({"user_id": str(uuid.uuid4()), "subscription_tier": user.subscription_tier})
            .execute()
        )
        return {"code": 200, "response": response.data}

    except Exception as e:
        print(f"Error: {e}")


#limit AI-generated posts to 10 per week

from datetime import datetime, timedelta

class create_post(base_model):
    user_id: str
    post_content: str

@app.post("/newpost")
def create_new_post(post: create_post):
    one_week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    recent_posts = supabase.table("user_posts").select("*").eq("user_id", post.user_id).gte("created_at", one_week_ago).execute()
    post_count = len(recent_posts.data)
    
    WEEKLY_LIMIT = 10
    if post_count >= WEEKLY_LIMIT:
        return {"code": 400, "error": "Weekly post limit reached. You can only create 10 AI-generated posts per week."}
    
    response = supabase.table("user_posts").insert({"post_id": str(uuid.uuid4()), "user_id": post.user_id, "post_content": post.post_content, "ai_generated": True}).execute()
    
    return {"code": 201, "message": "Post created successfully", "response": response.data, "remaining_posts": WEEKLY_LIMIT - post_count - 1}
#Following a creator

follow_caps = {"free": 5, "pro": 30}

@app.post("/follow")
def create_new_follow(user_id: str, creator_id: int):
    try:
        creator = (
            supabase.table("creator_profiles")
            .select("*")
            .eq("creator_id", creator_id)
            .execute()
        )
        if not creator.data:
            return {"code": 404, "error": "Creator not found"}
        existing = (
            supabase.table("user_follows")
            .select("*")
            .eq("user_id", user_id)
            .eq("creator_id", creator_id)
            .execute()
        )
        if existing.data:
            return {"code": 409, "error": "Creator is already followed"}
        user = (
            supabase.table("user_profiles")
            .select("subscription_tier")
            .eq("user_id", user_id)
            .single()
            .execute()
        )
        tier = user.data["subscription_tier"].lower()
        cap = follow_caps.get(tier)
        follows = (
            supabase.table("user_follows")
            .select("id", count="exact")
            .eq("user_id", user_id)
            .execute()
        )
        if follows.count >= cap:
            return {"code": 429, "error": "User is at their following limit"}
        result = (
            supabase.table("user_follows").insert({
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "creator_id": creator_id
            }).execute()
        )
        return {"code": 200, "response": "Follow created"}
    except Exception as e:
        print(f"Error: {e}")
>>>>>>> cc0575d6349629478c15a9f78a5ac4fe8c897d68
