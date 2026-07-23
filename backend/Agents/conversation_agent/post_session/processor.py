from database.session import (
    update_session_status,
    update_post_session
)

from post_session.analysis import (
    call_analysis_agent,
    call_assessment_agent
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
        raise Exception(
            "emotion_timeline missing from Analysis Agent response."
        )

    if "symptoms" not in analysis:
        raise Exception(
            "symptoms missing from Analysis Agent response."
        )

    print("Analysis Completed")

    # ------------------------------------------------------
    # Save Analysis
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

    assessment = call_assessment_agent(

        conversation_summary=conversation_summary,

        symptom_json=analysis["symptoms"]

    )

    if assessment is None:

        raise Exception(
            "Assessment Agent returned None."
        )

    print("Assessment Completed")

    # ------------------------------------------------------
    # Save Assessment
    # ------------------------------------------------------

    print("Saving Assessment...")

    update_post_session(

        session_id=session_id,

        database_url=database_url,

        assessment_json=assessment

    )

    print("Assessment Saved")

    # ------------------------------------------------------
    # RAG Agent
    # ------------------------------------------------------

    # print("Calling RAG Agent...")

    # recommendation = call_rag_agent(
    #     assessment_json=assessment,
    #     emotion_json=analysis["emotion_timeline"],
    #     symptom_json=analysis["symptoms"]
    # )

    # update_post_session(
    #     session_id=session_id,
    #     database_url=database_url,
    #     recommendation_json=recommendation
    # )

    # print("RAG Completed")

    # ------------------------------------------------------
    # Complete Session
    # ------------------------------------------------------

    # update_session_status(
    #     session_id,
    #     "COMPLETED",
    #     database_url
    # )

    print("RAG Agent not implemented yet.")
    print("Session remains in PROCESSING state.")

    print("=" * 60)