import uuid
import json
from database.database import get_connection


def get_current_session(user_id, database_url):
    conn = get_connection(database_url)
    cur = conn.cursor()

    cur.execute("""
        SELECT session_id, conversation_json
        FROM current_session
        WHERE user_id = %s
        AND status = 'IN_PROGRESS'
        LIMIT 1
    """, (user_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return {
            "session_id": str(row[0]),
            "conversation": row[1] or []
        }

    return None

def create_session(user_id, database_url):
    conn = get_connection(database_url)
    cur = conn.cursor()

    session_id = str(uuid.uuid4())

    cur.execute("""
        INSERT INTO current_session(
            session_id,
            user_id,
            conversation_json
        )
        VALUES(%s,%s,%s)
    """, (
        session_id,
        user_id,
        json.dumps([])
    ))

    conn.commit()

    cur.close()
    conn.close()

    # print(f"Created new session for user_id {user_id}: {session_id}")

    return session_id



def update_conversation(session_id, conversation, database_url):
    conn = get_connection(database_url)

    # if conn is None:
    #     print("Database connection failed.")
    #     return

    cur = conn.cursor()

    cur.execute("""
        UPDATE current_session
        SET conversation_json = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE session_id = %s
    """, (
        json.dumps(conversation),
        session_id,
    ),)

    # print("Rows Updated:", cur.rowcount)    

    conn.commit()

    cur.close()
    conn.close()