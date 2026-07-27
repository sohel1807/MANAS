import uuid
import json
import psycopg2


# ==========================================================
# Database Connection
# ==========================================================

def get_connection(database_url):

    try:

        conn = psycopg2.connect(database_url)

        return conn

    except Exception as e:

        print("Database Connection Error:", e)

        return None


# ==========================================================
# Save Session To History
# ==========================================================

def save_to_history(
    session,
    database_url
):

    conn = get_connection(database_url)

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO history(

            history_id,

            session_id,

            user_id,

            conversation_summary,

            emotion_json,

            symptom_json,

            assessment_json,

            recommendation_json,

            started_at,

            completed_at

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

            CURRENT_TIMESTAMP,

            CURRENT_TIMESTAMP

        )
        """,

        (

            str(uuid.uuid4()),

            session["session_id"],

            session["user_id"],

            json.dumps(
                session["conversation_summary"]
            ),

            json.dumps(
                session["emotion_json"]
            ),

            json.dumps(
                session["symptom_json"]
            ),

            json.dumps(
                session["assessment_json"]
            ),

            json.dumps(
                session["recommendation_json"]
            )

        )

    )

    conn.commit()

    cur.close()

    conn.close()


# ==========================================================
# Get User History
# ==========================================================

def get_history(
    user_id,
    database_url
):

    conn = get_connection(database_url)

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            history_id,

            completed_at,

            assessment_json

        FROM history

        WHERE user_id=%s

        ORDER BY completed_at DESC
        """,

        (user_id,)
    )

    rows = cur.fetchall()

    cur.close()

    conn.close()

    history = []

    for row in rows:

        assessment = row[2] or {}

        history.append(

            {

                "history_id": str(row[0]),

                "completed_at": row[1],

                "risk": assessment.get(
                    "overall_risk",
                    {}
                ).get(
                    "level",
                    "Unknown"
                )

            }

        )

    return history


# ==========================================================
# Get History Report
# ==========================================================

def get_history_report(
    history_id,
    database_url
):

    conn = get_connection(database_url)

    cur = conn.cursor()

    cur.execute(
        """
        SELECT

            conversation_summary,

            emotion_json,

            symptom_json,

            assessment_json,

            recommendation_json

        FROM history

        WHERE history_id=%s
        """,

        (history_id,)
    )

    row = cur.fetchone()

    cur.close()

    conn.close()

    if row is None:

        return None

    return {

        "conversation_summary": row[0] or {},

        "emotion_json": row[1] or {},

        "symptom_json": row[2] or {},

        "assessment_json": row[3] or {},

        "recommendation_json": row[4] or {}

    }