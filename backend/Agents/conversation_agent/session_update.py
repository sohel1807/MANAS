from modal import App, Image
import modal
import os

from database.session import (
    get_latest_session,
    get_current_session,
    create_session,
    delete_current_session,
    update_session_status
)

from database.history import (
    save_to_history,get_history,get_history_report
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



# Background Processor


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



# Stop Session Endpoint


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
    

# Session Status Endpoint


@app.function(
    secrets=[
        modal.Secret.from_name("DATABASE_URL")
    ]
)
@modal.fastapi_endpoint(
    method="GET",
    label="session-status"
)
def session_status(user_id: int):

    database_url = os.environ["DATABASE_URL"]


    # Get current session
    session = get_latest_session(
        user_id,
        database_url
    )


    if session is None:

        return {
            "status": "NO_SESSION"
        }


    return {
        "session_id": session["session_id"],
        "status": session["status"]
    }
    
    
from database.session import get_latest_session


@app.function(
    secrets=[
        modal.Secret.from_name("DATABASE_URL")
    ]
)
@modal.fastapi_endpoint(
    method="GET",
    label="dashboard"
)
def dashboard(user_id: int):

    database_url = os.environ["DATABASE_URL"]

    session = get_latest_session(
        user_id,
        database_url,
        "COMPLETED"
    )

    if session is None:

        return {
            "status": "FAILED",
            "message": "No session found"
        }

    return session



# New Session Endpoint


@app.function(
    secrets=[
        modal.Secret.from_name("DATABASE_URL")
    ]
)
@modal.fastapi_endpoint(
    method="POST",
    label="new-session"
)
def new_session(info: dict):

    database_url = os.environ["DATABASE_URL"]

    user_id = info["user_id"]

    # Check if completed session exists
    session = get_latest_session(
        user_id,
        database_url,
        status="COMPLETED"
    )

    if session is not None:

        # Save to history
        save_to_history(
            session,
            database_url
        )

        # Remove from current_session
        delete_current_session(
            session["session_id"],
            database_url
        )

    # Create fresh session
    session_id = create_session(
        user_id,
        database_url
    )

    return {

        "status": "SUCCESS",

        "session_id": session_id

    }


# History List


@app.function(
    secrets=[
        modal.Secret.from_name("DATABASE_URL")
    ]
)
@modal.fastapi_endpoint(
    method="GET",
    label="history"
)
def history(user_id: int):

    database_url = os.environ["DATABASE_URL"]

    history = get_history(
        user_id,
        database_url
    )

    return history


# History Report


@app.function(
    secrets=[
        modal.Secret.from_name("DATABASE_URL")
    ]
)
@modal.fastapi_endpoint(
    method="GET",
    label="history-report"
)
def history_report(history_id: str):

    database_url = os.environ["DATABASE_URL"]

    report = get_history_report(
        history_id,
        database_url
    )

    if report is None:

        return {
            "status": "FAILED",
            "message": "History report not found"
        }

    report["status"] = "COMPLETED"

    return report
    
    
    