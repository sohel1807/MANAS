from modal import App, Image
import modal
import os
from session import (
    get_current_session,
    update_session_status
)


image = Image.debian_slim(
    python_version="3.12"
).pip_install(
    "fastapi",
    "psycopg2-binary",
    "dotenv"
).add_local_dir(".",remote_path="/root")


app = App(
    "manas-session",
    image=image
)


@app.function(
    secrets=[
        modal.Secret.from_name("DATABASE_URL")
    ]
)
@modal.fastapi_endpoint(
    method="POST",
    label="stop-session"
)
def stop_session(info: dict):

    database_url = os.environ["DATABASE_URL"]


    session = get_current_session(
        info["user_id"],
        database_url
    )


    if session is None:

        return {
            "status":"FAILED",
            "message":"No active session"
        }


    update_session_status(
        session["session_id"],
        "PROCESSING",
        database_url
    )


    return {

        "status":"PROCESSING",

        "message":
        "Session stopped. Analysis started."

    }