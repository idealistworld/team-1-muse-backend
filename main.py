from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import uuid
from dotenv import load_dotenv
import os
from supabase import create_client, Client
from datetime import datetime, timedelta


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

# Return all users
@app.get("/users")
def get_all_users():
    try:
        response = (
            supabase.table("user_profiles")
            .select("*")
            .execute()
        )
        return {"response": response.data}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Return data for a specific user
@app.get("/users/{user_id}")
def get_user_by_id(user_id: str):
    try:
        exists = (
            supabase.table("user_profiles")
            .select("user_id")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )
        
        if not exists.data:
            raise HTTPException(status_code=404, detail="User does not exist")

        response = (
            supabase.table("user_profiles")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        return {"code": 200, "response": response.data}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))



class CreateUserModel(BaseModel):
    subscription_tier: str

# Create a new user object
@app.post("/users")
def create_new_user(user: CreateUserModel):

    valid_subscription_tiers = ["free", "pro"]

    if user.subscription_tier not in valid_subscription_tiers:
        raise HTTPException(status_code=400, detail="Select a valid subscription tier")

    try:
        response = (
            supabase.table("user_profiles")
            .insert({"user_id": str(uuid.uuid4()), "subscription_tier": user.subscription_tier})
            .execute()
        )
        return {"response": response.data}

    except Exception as e:
        print(f"Error: {e}")
        return {"code": 500, "error": str(e)}


# Create a new record to follow a creator with a follow limit implemented to separate "free" vs "paid" users
@app.post("/users/follow")
def create_new_follow(user_id: str, creator_id: int):
    follow_caps = {"free": 5, "pro": 30}

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
        return {"code": 500, "error": str(e)}


# Return data on a specific post
@app.get("/posts/{post_id}")
def get_post_by_id(post_id: str):
    try:
        exists = (
            supabase.table("user_posts")
            .select("post_id")
            .eq("post_id", post_id)
            .limit(1)
            .execute()
        )
        
        if not exists.data:
            raise HTTPException(status_code=404, detail="Post does not exist")

        response = (
            supabase.table("user_posts")
            .select("*")
            .eq("post_id", post_id)
            .execute()
        )

        return {"response": response.data}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Return all posts * added business logic by filtering here by user_id
@app.get("/posts/user/{user_id}")
def get_all_posts_by_user(user_id: str):
    try:
        response = (
            supabase.table("user_posts")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        return {"response": response.data}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Delete a post with a given post_id
@app.delete("/posts/{post_id}")
def delete_user_post(post_id: str):
    try:
        exists = (
            supabase.table("user_posts")
            .select("post_id")
            .eq("post_id", post_id)
            .limit(1)
            .execute()
        )
        if not exists.data:
            return {"code": 404, "error": "Post not found"}

        response = (
            supabase.table("user_posts")
            .delete()
            .eq("post_id", post_id)
            .execute()
        )
        return {"code": 200, "message": "Post deleted successfully", "response": response.data}
    
    except Exception as e:
        print(f"Error: {e}")
        return {"code": 500, "error": str(e)}


class create_post(BaseModel):
    user_id: str
    post_content: str

# Creates a new post with business logic included to enforce rate limiting
@app.post("/posts")
def create_new_post(post: create_post):
    one_week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    recent_posts = supabase.table("user_posts").select("*").eq("user_id", post.user_id).gte("created_at", one_week_ago).execute()
    post_count = len(recent_posts.data)
    
    WEEKLY_LIMIT = 10
    if post_count >= WEEKLY_LIMIT:
        return {"code": 400, "error": "Weekly post limit reached. You can only create 10 AI-generated posts per week."}
    
    response = supabase.table("user_posts").insert({"post_id": str(uuid.uuid4()), "user_id": post.user_id, "raw_text": post.post_content}).execute()
    
    return {"code": 201, "message": "Post created successfully", "response": response.data, "remaining_posts": WEEKLY_LIMIT - post_count - 1}


class CreateCreatorModel(BaseModel):
    profile_url: HttpUrl
    platform: str

# Create a new creator object
@app.post("/creators")
def create_new_creator(creator: CreateCreatorModel):
    try:

        valid_platforms = ["linkedin", "instagram"]

        if creator.platform not in valid_platforms:
             raise HTTPException(status_code=400, detail="Please use a valid platform")

        response = (
            supabase.table("creator_profiles")
            .insert({"profile_url": str(creator.profile_url), "platform": creator.platform})
            .execute()
        )
        return {"response": response.data}

    except Exception as e:
        print(f"Error: {e}")
        return {"code": 500, "error": str(e)}


# Get all creators on the platform *can create a separate endpoint for getting all creators that someone follows
@app.get("/creators")
def get_all_creators():
    try:
        response = (
            supabase.table("creator_profiles")
            .select("*")
            .execute()
        )
        return {"response": response.data}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Return data on a specific creator
@app.get("/creators/{creator_id}")
def get_creator_by_id(creator_id: int):
    try:
        exists = (
            supabase.table("creator_profiles")
            .select("creator_id")
            .eq("creator_id", creator_id)
            .limit(1)
            .execute()
        )
        
        if not exists.data:
            raise HTTPException(status_code=404, detail="Creator does not exist")

        response = (
            supabase.table("creator_profiles")
            .select("*")
            .eq("creator_id", creator_id)
            .execute()
        )

        return {"response": response.data}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Get all content from a specific creator
@app.get("/content/creator/{creator_id}")
def get_all_content_by_creator(creator_id: int):
    try:
        response = (
            supabase.table("creator_content")
            .select("*")
            .eq("creator_id", creator_id)
            .execute()
        )
        return {"response": response.data}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class create_content(BaseModel):
    creator_id: int 
    post_url: HttpUrl
    post_raw: str


# Creates a new piece of content
@app.post("/content")
def create_new_creator_content(post: create_content):
    try:
        existing_post = (
            supabase.table("creator_content")
            .select("*")
            .eq("post_url", post.post_url)
            .execute()
        )
        if existing_post.data:
            return {"code": 400, "error": "Duplicate URL detected. This post already exists."}

        response = (
            supabase.table("creator_content")
            .insert({
                "creator_id": post.creator_id,
                "post_url": str(post.post_url),
                "post_raw": post.post_raw
            })
            .execute()
        )
        return {"code": 201, "message": "Post created successfully", "response": response}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Return data for a specific piece of content
@app.get("/content/{content_id}")
def get_content_by_id(content_id: int):
    try:
        exists = (
            supabase.table("creator_content")
            .select("content_id")
            .eq("content_id", content_id)
            .limit(1)
            .execute()
        )
        
        if not exists.data:
            raise HTTPException(status_code=404, detail="Content does not exist")

        response = (
            supabase.table("creator_content")
            .select("*")
            .eq("content_id", content_id)
            .execute()
        )

        return {"code": 200, "response": response.data}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))