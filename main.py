from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import uuid

# Supabase
import psycopg2
from dotenv import load_dotenv
import os
from supabase import create_client, Client

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


class create_content(BaseModel):
    creator_id: int 
    post_url: str

@app.post("/creator-content")
def create_new_creator_content(post: create_content):
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
            "post_url": post.post_url
        })
        .execute()
    )
    return {"code": 201, "message": "Post created successfully", "response": response}

@app.delete("/user-posts/{post_id}")
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
