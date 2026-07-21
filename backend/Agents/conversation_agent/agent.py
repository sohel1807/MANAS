from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from prompt_builder import build_prompt
from database.database import get_connection 
from database.session import get_current_session, create_session, update_conversation
import json
import requests

model = None

def chat(user_id, message, api_key, database_url):
    global model

    if model is None:
        model = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            api_key=api_key,
        )

    # print("=" * 50)
    # print("USER ID:", user_id)
    # print("MESSAGE:", message)

    session = get_current_session(user_id, database_url)
    # print("SESSION:", session)

    if session is None:
        print("No session found. Creating new session...")
        session_id = create_session(user_id, database_url)
        conversation = []
    else:
        session_id = session["session_id"]
        conversation = session["conversation"]

        # print("Conversation type:", type(conversation))
        # print("Conversation:", conversation)

        if isinstance(conversation, str):
            conversation = json.loads(conversation)

    history = []

    for msg in conversation:
        if msg["role"] == "user":
            history.append(HumanMessage(content=msg["content"]))
        else:
            history.append(AIMessage(content=msg["content"]))

    messages = build_prompt(history, message)

    result = model.invoke(messages)

    conversation.append(
        {
            "role": "user",
            "content": message,
        }
    )

    conversation.append(
        {
            "role": "assistant",
            "content": result.content,
        }
    )

    EMOTION_API = "https://atharva7758--emotion-dev.modal.run"

    response = requests.post(
        EMOTION_API,
        json={
            "conversation": conversation
        },
        timeout=60
    )

    print(response)

    response.raise_for_status()
    analysis = response.json()



    # print("Conversation before update:")
    # print(conversation)

    # print("Conversation updated successfully.")
    # print("=" * 50)


    update_conversation(
        session_id=session_id,
        conversation=conversation,
        analysis=analysis,
        database_url=database_url
    )

    return result.content