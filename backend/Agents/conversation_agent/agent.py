import requests
from langchain_groq import ChatGroq

from prompt_builder import build_prompt
from context_builder import build_conversation_context

from database.session import (
    get_current_session,
    create_session,
    update_conversation,
)

model = None

# ==========================================================
# Memory Agent Endpoint
# ==========================================================

MEMORY_API = "https://atharva7758--memory-dev.modal.run"


def chat(user_id, message, api_key, database_url):
    global model

    # --------------------------------------------------
    # Initialize LLM (Only Once)
    # --------------------------------------------------

    if model is None:

        model = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            api_key=api_key,
        )

    # --------------------------------------------------
    # Load Existing Session
    # --------------------------------------------------

    session = get_current_session(
        user_id,
        database_url
    )

    if session is None:

        session_id = create_session(
            user_id,
            database_url
        )

        conversation = []

        conversation_summary = {
            "main_issue": "",
            "overall_summary": "",
            "current_stage": "early",
            "protective_factors": [],
            "risk_observations": []
        }

        covered_topics = {
            "general": [],
            "phq9": [],
            "gad7": []
        }

    else:

        session_id = session["session_id"]

        conversation = session["conversation"]

        conversation_summary = session.get(
            "conversation_summary",
            {
                "main_issue": "",
                "overall_summary": "",
                "current_stage": "early",
                "protective_factors": [],
                "risk_observations": []
            }
        )

        covered_topics = session.get(
            "covered_topics",
            {
                "general": [],
                "phq9": [],
                "gad7": []
            }
        )

    # --------------------------------------------------
    # Use Only Recent Conversation
    # --------------------------------------------------

    recent_conversation = (
        conversation
        + [
            {
                "role": "user",
                "content": message
            }
        ]
    )[-8:]

    # --------------------------------------------------
    # Build Prompt
    # --------------------------------------------------

    conversation_context = build_conversation_context(
        conversation_summary,
        covered_topics,
    )

    messages = build_prompt(
        chat_history=recent_conversation,
        conversation_context=conversation_context,
    )

    # --------------------------------------------------
    # Generate Assistant Response
    # --------------------------------------------------

    result = model.invoke(messages)

    assistant_reply = result.content

    # --------------------------------------------------
    # Update Conversation History
    # --------------------------------------------------

    conversation.append(
        {
            "role": "user",
            "content": message,
        }
    )

    conversation.append(
        {
            "role": "assistant",
            "content": assistant_reply,
        }
    )

    # --------------------------------------------------
    # Memory Update
    # --------------------------------------------------

    try:

        response = requests.post(

            MEMORY_API,

            json={

                "recent_messages": conversation[-8:],

                "conversation_summary": conversation_summary,

                "covered_topics": covered_topics,

            },

            timeout=60,

        )

        response.raise_for_status()

        analysis = response.json()

    except Exception as e:

        print(f"Memory Agent Error: {e}")

        analysis = {
            "conversation_summary": conversation_summary,
            "covered_topics": covered_topics,
        }

    # --------------------------------------------------
    # Save Updated Conversation + Memory
    # --------------------------------------------------

    update_conversation(

        session_id=session_id,

        conversation=conversation,

        analysis=analysis,

        database_url=database_url,

    )

    # --------------------------------------------------
    # Return Assistant Reply
    # --------------------------------------------------

    return assistant_reply