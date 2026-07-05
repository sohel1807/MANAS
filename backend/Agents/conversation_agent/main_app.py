from fastapi import FastAPI
from pydantic import BaseModel
import modal
from modal import App, enter, method, web_endpoint, Image
from typing import Dict 
from agent import chat
import os
from database.database import get_connection 
from database.session import get_current_session, create_session, update_conversation


image = Image.debian_slim(python_version="3.12").pip_install(
    "langchain",
    "langchain-core",
    "langchain-groq",
    "python-dotenv",
    "fastapi",
    "uvicorn[standard]",
    "psycopg2-binary",
).add_local_dir(".", remote_path="/root")



app = App(name="Conversation-Agent", image=image)

# image = image.add_local_python_source("agent.py")

@app.function(secrets=[modal.Secret.from_name("groq"),modal.Secret.from_name("DATABASE_URL")])
@modal.fastapi_endpoint(label="chat", method="POST")
def chatbot(Info: Dict):
    api_key=os.environ["GROQ_API_KEY"]
    database_url=os.environ["DATABASE_URL"]

    reply = chat(
        user_id=Info["user_id"],
        message=Info["message"],
        api_key=api_key,
        database_url=database_url
)


    return {
        "user_id": Info["user_id"],
        "reply": reply
    }
