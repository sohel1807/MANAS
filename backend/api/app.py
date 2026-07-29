from modal import App, Image
import modal
from typing import Dict
import os
from auth import register_user, login_user

image =Image.debian_slim(python_version="3.12").pip_install(
        "fastapi",
        "psycopg2-binary",
        "bcrypt",
        "python-dotenv"
    ).add_local_dir(".", remote_path="/root")

# image = image.add_local_python_source("auth.py")
# image = image.add_local_python_source("database.py")

app = App("manas-auth", image=image)


@app.function(secrets=[modal.Secret.from_name("DATABASE_URL")])
@modal.fastapi_endpoint(method="POST", label="register")
def register(info: Dict):
    database_url = os.environ["DATABASE_URL"]
    return register_user(
        info["name"],
        info["email"],
        info["password"],
        database_url
    )


@app.function(secrets=[modal.Secret.from_name("DATABASE_URL")])
@modal.fastapi_endpoint(method="POST", label="login")
def login(info: Dict):
    database_url = os.environ["DATABASE_URL"]
    return login_user(
        info["email"],
        info["password"],
        database_url
    )