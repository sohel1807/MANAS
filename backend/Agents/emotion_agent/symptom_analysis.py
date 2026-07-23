import json
import re

from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)


# ==========================================================
# Prompt
# ==========================================================

def build_prompt():

    return """
You are a mental health symptom extraction assistant.

Your task is to analyze ONLY the USER'S messages.

Rules:

- Never analyze assistant messages.
- Never diagnose disorders.
- Never infer unsupported symptoms.
- Only extract symptoms explicitly supported by the user's own words.
- Ignore greetings and casual conversation.
- Do not include symptoms with weak evidence.
- For every detected symptom, map it to the closest PHQ-9 and/or GAD-7 assessment item(s).

Allowed PHQ-9 items:
interest
depressed_mood
sleep
energy
appetite
guilt
concentration
movement
self_harm

Allowed GAD-7 items:
nervousness
control_worry
excessive_worry
relaxing
restlessness
irritability
fear

For every symptom return:

{
    "present": true,
    "severity": "mild | moderate | severe",
    "confidence": 0.95,
    "assessment_mapping": {
        "phq9": [],
        "gad7": []
    },
    "evidence": [
        "Exact user statement"
    ]
}

Return JSON in the following format:

{
    "symptoms": {

        "sleep_disturbance": {
            "present": true,
            "severity": "moderate",
            "confidence": 0.93,
            "assessment_mapping": {
                "phq9": ["sleep"],
                "gad7": []
            },
            "evidence": []
        }

    }
}

Return ONLY valid JSON.

No markdown.

No explanation.
"""


# ==========================================================
# Empty Response
# ==========================================================

def empty_response():

    return {
        "symptoms": {}
    }


# ==========================================================
# JSON Cleaner
# ==========================================================

def clean_json(text):

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    elif text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    text = re.sub(
        r"^json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


# ==========================================================
# Parser
# ==========================================================

def parse_response(response_text):

    try:

        cleaned = clean_json(response_text)

        data = json.loads(cleaned)

    except Exception:

        return empty_response()

    if not isinstance(data, dict):
        return empty_response()

    symptoms = data.get("symptoms", {})

    if not isinstance(symptoms, dict):
        symptoms = {}

    cleaned_symptoms = {}

    for name, symptom in symptoms.items():

        if not isinstance(symptom, dict):
            continue

        try:
            confidence = float(
                symptom.get("confidence", 0)
            )
        except Exception:
            confidence = 0.0

        evidence = symptom.get("evidence", [])

        if not isinstance(evidence, list):
            evidence = []

        evidence = [
            item.strip()
            for item in evidence
            if isinstance(item, str) and item.strip()
        ]

        mapping = symptom.get(
            "assessment_mapping",
            {}
        )

        if not isinstance(mapping, dict):
            mapping = {}

        phq9 = mapping.get(
            "phq9",
            []
        )

        gad7 = mapping.get(
            "gad7",
            []
        )

        if not isinstance(phq9, list):
            phq9 = []

        if not isinstance(gad7, list):
            gad7 = []

        cleaned_symptoms[name] = {

            "present": bool(
                symptom.get("present", False)
            ),

            "severity": symptom.get(
                "severity",
                "mild"
            ),

            "confidence": confidence,

            "assessment_mapping": {

                "phq9": phq9,

                "gad7": gad7

            },

            "evidence": evidence

        }

    return {

        "symptoms": cleaned_symptoms

    }

# ==========================================================
# Symptom Extraction
# ==========================================================

def extract_symptoms(
    conversation,
    groq_model
):

    messages = [

        SystemMessage(
            content=build_prompt()
        ),

        HumanMessage(
            content=json.dumps(
                {
                    "conversation": conversation
                },
                indent=2,
                ensure_ascii=False
            )
        )

    ]

    response = groq_model.invoke(messages)

    return parse_response(
        response.content
    )


# ==========================================================
# Shared Groq Model
# ==========================================================

def load_groq_model(api_key):

    return ChatGroq(

        model_name="llama-3.3-70b-versatile",

        api_key=api_key,

        temperature=0,

        max_retries=2,

    )