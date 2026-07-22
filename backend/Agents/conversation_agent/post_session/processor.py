from database.session import (
    update_session_status,
    update_post_session
)

from post_session.analysis import (
    call_analysis_agent
)


# ==========================================================
# Process Session
# ==========================================================

def process_session(
    session,
    database_url,
):

    session_id = session["session_id"]
    conversation = session["conversation"]
    conversation_summary = session["conversation_summary"]
    covered_topics = session["covered_topics"]

    print("=" * 60)
    print(f"Processing Session: {session_id}")
    print("=" * 60)

    print("Conversation Loaded")

    # ------------------------------------------------------
    # Analysis Agent
    # ------------------------------------------------------

    print("Calling Analysis Agent...")

    analysis = call_analysis_agent(conversation)

    if analysis is None:
        raise Exception("Analysis Agent returned None.")

    if "emotion_timeline" not in analysis:
        raise Exception("emotion_timeline missing from Analysis Agent response.")

    if "symptoms" not in analysis:
        raise Exception("symptoms missing from Analysis Agent response.")

    print("Analysis Completed")

    # ------------------------------------------------------
    # Save Analysis Results
    # ------------------------------------------------------

    print("Saving Analysis Results...")

    update_post_session(

        session_id=session_id,

        database_url=database_url,

        emotion_json=analysis["emotion_timeline"],

        symptom_json=analysis["symptoms"]

    )

    print("Analysis Saved")

    # ------------------------------------------------------
    # Assessment Agent
    # ------------------------------------------------------

    print("Calling Assessment Agent...")

    # TODO
    # assessment = call_assessment_agent(
    #     emotion_timeline=analysis["emotion_timeline"],
    #     symptoms=analysis["symptoms"]
    # )

    print("Assessment Completed")

    # ------------------------------------------------------
    # Complete
    # ------------------------------------------------------

    update_session_status(
        session_id,
        "COMPLETED",
        database_url
    )

    print("Session Completed")
    print("=" * 60)