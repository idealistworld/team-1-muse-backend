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

