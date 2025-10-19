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
            return {"code": 429, "error": "User is at their following linit"}
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