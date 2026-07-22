from modal import App, Image
import modal
import os

from database.session import (
    get_current_session,
    update_session_status
)

from post_session.processor import process_session


image = (
    Image.debian_slim(python_version="3.12")
    .pip_install(
        "fastapi",
        "psycopg2-binary",
        "python-dotenv",
        "requests"
    )
    .add_local_dir(".", remote_path="/root")
)

app = App(
    "manas-session",
    image=image
)


# ==========================================================
# Background Processor
# ==========================================================

@app.function(
    secrets=[
        modal.Secret.from_name("DATABASE_URL")
    ]
)
def run_post_session(session):

    database_url = os.environ["DATABASE_URL"]

    try:

        process_session(
            session=session,
            database_url=database_url
        )

    except Exception as e:

        print(f"Post-session processing failed: {e}")

        update_session_status(
            session["session_id"],
            "FAILED",
            database_url
        )

        raise


# ==========================================================
# Stop Session Endpoint
# ==========================================================

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

    # Get active session
    session = get_current_session(
        info["user_id"],
        database_url
    )

    if session is None:

        return {
            "status": "FAILED",
            "message": "No active session"
        }

    # Mark session as processing
    update_session_status(
        session["session_id"],
        "PROCESSING",
        database_url
    )

    # Start background processing
    run_post_session.spawn(session)

    # Return immediately
    return {
        "status": "PROCESSING",
        "message": "Session stopped. Analysis started."
    }