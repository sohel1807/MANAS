from database.session import (
    update_session_status,
    update_post_session
)

from post_session.analysis import (
    call_analysis_agent,
    call_assessment_agent
)

from post_session.recommendation import (
    call_recommendation_agent
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

    # ======================================================
    # Analysis Agent
    # ======================================================

    try:

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

    except Exception as e:

        print(f"Analysis Agent Failed: {e}")

        update_session_status(
            session_id,
            "FAILED",
            database_url
        )

        raise

    # ======================================================
    # Save Analysis
    # ======================================================

    try:

        print("Saving Analysis Results...")

        update_post_session(

            session_id=session_id,

            database_url=database_url,

            emotion_json=analysis["emotion_timeline"],

            symptom_json=analysis["symptoms"]

        )

        print("Analysis Saved")

    except Exception as e:

        print(f"Failed to Save Analysis: {e}")

        update_session_status(
            session_id,
            "FAILED",
            database_url
        )

        raise

    # ======================================================
    # Assessment Agent
    # ======================================================

    try:

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

    except Exception as e:

        print(f"Assessment Agent Failed: {e}")

        update_session_status(
            session_id,
            "FAILED",
            database_url
        )

        raise

    # ======================================================
    # Save Assessment
    # ======================================================

    try:

        print("Saving Assessment...")

        update_post_session(

            session_id=session_id,

            database_url=database_url,

            assessment_json=assessment

        )

        print("Assessment Saved")

    except Exception as e:

        print(f"Failed to Save Assessment: {e}")

        update_session_status(
            session_id,
            "FAILED",
            database_url
        )

        raise

    # ======================================================
    # Recommendation Agent
    # ======================================================

    try:

        print("Calling Recommendation Agent...")

        recommendation = call_recommendation_agent(

            conversation_summary=conversation_summary,

            emotion_summary=analysis["emotion_timeline"],

            symptoms=analysis["symptoms"],

            assessment=assessment

        )

        if recommendation is None:

            raise Exception(
                "Recommendation Agent returned None."
            )

        print("Recommendation Completed")

    except Exception as e:

        print(f"Recommendation Agent Failed: {e}")

        update_session_status(
            session_id,
            "FAILED",
            database_url
        )

        raise

    # ======================================================
    # Save Recommendation
    # ======================================================

    try:

        print("Saving Recommendation...")

        update_post_session(

            session_id=session_id,

            database_url=database_url,

            recommendation_json=recommendation

        )

        print("Recommendation Saved")

    except Exception as e:

        print(f"Failed to Save Recommendation: {e}")

        update_session_status(
            session_id,
            "FAILED",
            database_url
        )

        raise

    # ======================================================
    # Complete Session
    # ======================================================

    try:

        update_session_status(

            session_id,

            "COMPLETED",

            database_url

        )

        print("=" * 60)
        print("Session Processing Completed Successfully")
        print("=" * 60)

    except Exception as e:

        print(f"Failed to Complete Session: {e}")

        update_session_status(
            session_id,
            "FAILED",
            database_url
        )

        raise