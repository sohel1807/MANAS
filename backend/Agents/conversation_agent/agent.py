import requests

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

from prompt_builder import build_prompt

from database.session import (
    get_current_session,
    create_session,
    update_conversation,
)

model = None


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

        conversation_summary = {}

        emotion_json = {}

        symptom_json = {}

        covered_topics = []

    else:

        session_id = session["session_id"]

        conversation = session["conversation"]

        conversation_summary = session.get(
            "conversation_summary",
            {}
        )

        emotion_json = session.get(
            "emotion_json",
            {}
        )

        symptom_json = session.get(
            "symptom_json",
            {}
        )

        covered_topics = session.get(
            "covered_topics",
            []
        )

    # --------------------------------------------------
    # Use Only Recent Conversation
    # --------------------------------------------------

    recent_conversation = conversation[-8:]

    history = []

    for msg in recent_conversation:

        if msg["role"] == "user":

            history.append(
                HumanMessage(
                    content=msg["content"]
                )
            )

        elif msg["role"] == "assistant":

            history.append(
                AIMessage(
                    content=msg["content"]
                )
            )

    # --------------------------------------------------
    # Build Prompt
    # --------------------------------------------------

    messages = build_prompt(

        chat_history=recent_conversation,

        user_message=message,

        conversation_summary=conversation_summary,

        emotion_json=emotion_json,

        symptom_json=symptom_json,

        covered_topics=covered_topics,

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
    # Emotion & NLP Analysis
    # --------------------------------------------------

    EMOTION_API = "https://amans1810--emotion-dev.modal.run"

    response = requests.post(

        EMOTION_API,

        json={

            "recent_messages": conversation[-8:],

            "conversation_summary": conversation_summary,

            "symptom_json": symptom_json,

            "covered_topics": covered_topics,

        },

        timeout=60,

    )

    response.raise_for_status()

    analysis = response.json()

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