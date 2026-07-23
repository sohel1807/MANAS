import uuid
import json
import psycopg2
from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection(database_url):
    try:
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        print("Database Connection Error:", e)
        return None


# ==========================================================
# Default Structures
# ==========================================================

DEFAULT_SUMMARY = {
    "main_issue": "",
    "overall_summary": "",
    "current_stage": "early",
    "protective_factors": [],
    "risk_observations": []
}

DEFAULT_COVERED_TOPICS = {
    "general": [],
    "phq9": [],
    "gad7": []
}


# ==========================================================
# Get Current Session
# ==========================================================

def get_current_session(user_id, database_url):

    conn = get_connection(database_url)

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

        session_id,

        conversation_json,

        conversation_summary,

        emotion_json,

        symptom_json,

        assessment_json,

        covered_topics

        FROM current_session
        WHERE user_id=%s

        AND status='IN_PROGRESS'

        LIMIT 1
        """,
        (user_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    # ------------------------------------------------------
    # Handle old sessions created before covered_topics
    # was changed from list -> dictionary
    # ------------------------------------------------------

    assessment_json = row[5]

    covered_topics = row[6]

    if not isinstance(covered_topics, dict):
        covered_topics = DEFAULT_COVERED_TOPICS.copy()

    conversation_summary = row[2]

    if not isinstance(conversation_summary, dict):
        conversation_summary = DEFAULT_SUMMARY.copy()

    return {

        "session_id": str(row[0]),

        "conversation": row[1] or [],

        "conversation_summary": conversation_summary,

        "emotion_json": row[3] or {},

        "symptom_json": row[4] or {},

        "assessment_json": assessment_json or {},

        "covered_topics": covered_topics

    }


# ==========================================================
# Create Session
# ==========================================================

def create_session(user_id, database_url):

    conn = get_connection(database_url)

    cur = conn.cursor()

    session_id = str(uuid.uuid4())

    cur.execute(
        """
        INSERT INTO current_session(

            session_id,
            user_id,
            conversation_json,
            conversation_summary,
            emotion_json,
            symptom_json,
            assessment_json,
            covered_topics,
            status

        )

        VALUES(

            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s

        )
        """,
        (

            session_id,

            user_id,

            json.dumps([]),

            json.dumps(DEFAULT_SUMMARY),

            json.dumps({}),          # emotion_json

            json.dumps({}),          # symptom_json

            json.dumps({}),          # assessment_json

            json.dumps(DEFAULT_COVERED_TOPICS),

            "IN_PROGRESS"

        )

    )

    conn.commit()

    cur.close()

    conn.close()

    return session_id


# ==========================================================
# Update Conversation
# ==========================================================

def update_conversation(

    session_id,

    conversation,

    analysis,

    database_url

):

    conn = get_connection(database_url)

    cur = conn.cursor()

    if analysis is None:

        cur.execute(
            """
            UPDATE current_session

            SET

                conversation_json=%s,

                updated_at=CURRENT_TIMESTAMP

            WHERE session_id=%s
            """,

            (

                json.dumps(conversation),

                session_id

            )

        )

    else:

        cur.execute(
            """
            UPDATE current_session

            SET

                conversation_json=%s,

                conversation_summary=%s,

                covered_topics=%s,

                updated_at=CURRENT_TIMESTAMP

            WHERE session_id=%s
            """,

            (

                json.dumps(conversation),

                json.dumps(
                    analysis["conversation_summary"]
                ),

                json.dumps(
                    analysis["covered_topics"]
                ),

                session_id

            )

        )

    conn.commit()

    cur.close()

    conn.close()


# ==========================================================
# Update Session Status
# ==========================================================

def update_session_status(
    session_id,
    status,
    database_url
):

    conn = get_connection(database_url)

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE current_session

        SET
            status=%s,
            updated_at=CURRENT_TIMESTAMP

        WHERE session_id=%s
        """,

        (
            status,
            session_id
        )
    )

    conn.commit()

    cur.close()

    conn.close()

# ==========================================================
# Update Post Session Analysis
# ==========================================================

def update_post_session(
    session_id,
    database_url,
    emotion_json=None,
    symptom_json=None,
    assessment_json=None,
    recommendation_json=None
):

    conn = get_connection(database_url)

    cur = conn.cursor()

    updates = []
    values = []


    if emotion_json is not None:

        updates.append("emotion_json=%s")

        values.append(
            json.dumps(emotion_json)
        )


    if symptom_json is not None:

        updates.append("symptom_json=%s")

        values.append(
            json.dumps(symptom_json)
        )


    if assessment_json is not None:

        updates.append("assessment_json=%s")

        values.append(
            json.dumps(assessment_json)
        )


    if recommendation_json is not None:

        updates.append("recommendation_json=%s")

        values.append(
            json.dumps(recommendation_json)
        )


    # Always update timestamp

    updates.append(
        "updated_at=CURRENT_TIMESTAMP"
    )


    # Add WHERE condition value

    values.append(session_id)


    query = f"""
        UPDATE current_session

        SET
            {", ".join(updates)}

        WHERE session_id=%s
    """


    cur.execute(
        query,
        tuple(values)
    )


    conn.commit()

    cur.close()

    conn.close()