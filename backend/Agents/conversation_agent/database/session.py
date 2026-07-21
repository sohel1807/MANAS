import uuid
import json

from database.database import get_connection


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

    if row:

        return {

            "session_id": str(row[0]),

            "conversation": row[1] or [],

            "conversation_summary": row[2] or {},

            "emotion_json": row[3] or {},

            "symptom_json": row[4] or {},

            "covered_topics": row[5] or []

        }

    return None


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

            covered_topics

        )

        VALUES(

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

            json.dumps({}),

            json.dumps({}),

            json.dumps({}),

            json.dumps([])

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

    cur.execute(
        """
        UPDATE current_session

        SET

            conversation_json=%s,

            conversation_summary=%s,

            emotion_json=%s,

            symptom_json=%s,

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
                analysis["emotion_json"]
            ),

            json.dumps(
                analysis["symptom_json"]
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