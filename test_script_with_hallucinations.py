#!/usr/bin/env python3
"""
Test script with potential AI hallucinations for demonstration
"""

# Potential hallucinations to detect:
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

app = FastAPI()

class UserModel(BaseModel):
    name: str
    email: str
    # HALLUCINATION: Pydantic doesn't have this method
    def validate_email_format(self):
        return self.email.is_valid_email()

@app.get("/users")
async def get_users():
    # HALLUCINATION: FastAPI doesn't have this method
    return app.get_all_users()

@app.post("/users")  
async def create_user(user: UserModel):
    # HALLUCINATION: requests doesn't have this method
    response = requests.post_json("http://api.example.com/users", user.dict())
    
    # HALLUCINATION: Wrong parameter name
    if response.status_code == 200:
        return {"message": "User created successfully"}
    else:
        # HALLUCINATION: FastAPI doesn't have this exception
        raise app.HTTPException(status_code=400, detail="Failed to create user")

# HALLUCINATION: This method doesn't exist in FastAPI
@app.middleware("cors")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    # HALLUCINATION: Wrong parameter name
    app.run(host="0.0.0.0", port=8000, debug=True) 