import json
import re

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


def build_prompt():

    return """
You are an expert mental wellness conversation summarizer.

Your task is ONLY to summarize the conversation.

Do NOT chat.
Do NOT answer the user.
Do NOT diagnose.

Analyze the COMPLETE conversation and populate EVERY field below.

Return ONLY valid JSON.

Schema:

{
    "main_issue": "",
    "overall_summary": "",
    "current_stage": "",
    "protective_factors": [],
    "risk_observations": [
        {
            "symptom": "",
            "present": true,
            "confidence": 0.0
        }
    ]
}

Rules:

1. main_issue MUST NEVER be empty if enough information exists.

Examples:
- Work-related stress
- Academic pressure
- Relationship difficulties
- Financial worries
- Sleep problems

2. overall_summary MUST NEVER be empty.

Write 2-3 concise sentences describing the user's overall situation.

3. current_stage must be one of:

early
exploring
moderate
well_understood

4. protective_factors should contain only strengths clearly mentioned.

Examples:

supportive family
good friends
exercise
stable job
therapy
religious support
positive coping

5. risk_observations should contain ONLY symptoms clearly mentioned.

Each item must be:

{
    "symptom":"sleep",
    "present":true,
    "confidence":0.95
}

6. Never invent symptoms.

7. Never diagnose.

8. Never return empty strings when the conversation provides enough information.

9. Return ONLY JSON.
"""


def empty_summary():

    return {
        "main_issue": "",
        "overall_summary": "",
        "current_stage": "early",
        "protective_factors": [],
        "risk_observations": []
    }


def clean_json(text):

    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```json", "", text)
        text = re.sub(r"^```", "", text)
        text = re.sub(r"```$", "", text)
        text = text.strip()

    return text


def generate_summary(conversation, api_key):

    conversation_text = ""

    for msg in conversation:

        conversation_text += (
            f"{msg['role'].capitalize()}: {msg['content']}\n"
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

    # print("\n========== SUMMARY RAW OUTPUT ==========\n")
    # print(result.content)
    # print("\n========================================\n")

    try:

        cleaned = clean_json(result.content)

        return json.loads(cleaned)

    except Exception as e:

        # print("\nSUMMARY JSON PARSE ERROR\n")
        # print(e)

        return empty_summary()