import json

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from Knowledge_base.loader import load_knowledge_base


knowledge = load_knowledge_base()


def build_prompt():

    return f"""
You are an NLP extraction engine for a mental wellness assistant.

Your ONLY responsibility is to analyze the conversation.

Do NOT chat.

Do NOT diagnose.

Use ONLY the Mental Health Knowledge Base below.

========================
MENTAL HEALTH KNOWLEDGE BASE
========================

{json.dumps(knowledge, indent=2)}

========================
TASK
========================

For EVERY indicator in the knowledge base return:

{{
    "symptom_json": {{
        "<indicator_id>": {{
            "present": true/false,
            "confidence": 0.0-1.0,
            "evidence": [
                "Exact user sentence(s)"
            ]
        }}
    }},
    "covered_topics": [
    ]
}}

Rules

1. Use ONLY indicator IDs from the knowledge base.

2. Every indicator MUST appear.

3. If an indicator is not mentioned:

    present = false
    confidence = 0.0
    evidence = []

4. Evidence must contain ONLY exact user statements.

5. Never invent evidence.

6. covered_topics should contain ONLY the major topics discussed.

7. Return ONLY valid JSON.

"""
    

def empty_symptom_json():

    symptoms = {}

    for category in knowledge.values():

        for indicator in category:

            symptoms[indicator["id"]] = {

                "present": False,
                "confidence": 0.0,
                "evidence": []

            }

    return symptoms


def extract(conversation, api_key):

    conversation_text = ""

    for msg in conversation:

        conversation_text += (
            f"{msg['role'].capitalize()}: "
            f"{msg['content']}\n"
        )

    model = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        api_key=api_key
    )

    messages = [

        SystemMessage(
            content=build_prompt()
        ),

        HumanMessage(
            content=conversation_text
        )

    ]

    result = model.invoke(messages)

    try:

        return json.loads(result.content)

    except Exception:

        return {

            "symptom_json": empty_symptom_json(),

            "covered_topics": []

        }