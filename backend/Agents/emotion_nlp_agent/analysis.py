import json
import re

from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from Knowledge_base.loader import load_knowledge_base


# --------------------------------------------------
# Load Knowledge Base Once
# --------------------------------------------------

knowledge = load_knowledge_base()


# --------------------------------------------------
# Prompt Builder
# --------------------------------------------------

def build_prompt():

    return f"""
You are an expert Mental Health NLP Analysis Engine.

Your ONLY task is to analyze a conversation.

Do NOT chat.

Do NOT answer the user.

Do NOT provide advice.

Do NOT diagnose.

Use ONLY the Mental Health Knowledge Base below while extracting symptoms.

==========================================================
MENTAL HEALTH KNOWLEDGE BASE
==========================================================

{json.dumps(knowledge, indent=2)}

==========================================================
YOUR TASK
==========================================================

Analyze the COMPLETE conversation.

Return ONLY valid JSON.

Schema:

{{
    "conversation_summary":
    {{
        "main_issue":"",
        "overall_summary":"",
        "current_stage":"",
        "protective_factors":[],
        "risk_observations":[]
    }},

    "symptom_json":
    {{}},

    "covered_topics":[]
}}

==========================================================
SUMMARY RULES
==========================================================

1.

main_issue

One short sentence.

Examples

Work stress

Relationship conflict

Academic pressure

Sleep issues

Financial worries

2.

overall_summary

2-3 concise sentences.

Summarize the user's situation.

3.

current_stage

Must be one of

early

exploring

moderate

well_understood

4.

protective_factors

Only include strengths clearly mentioned.

Examples

supportive family

good friends

stable job

exercise

therapy

religious support

positive coping

5.

risk_observations

Return ONLY clearly mentioned symptoms.

Each item:

{{
    "symptom":"",
    "present":true,
    "confidence":0.95
}}

Do NOT include evidence.

Never diagnose.

Never invent symptoms.

==========================================================
SYMPTOM EXTRACTION RULES
==========================================================

For EVERY indicator from the knowledge base return

{{
    "<indicator_id>":
    {{
        "present":true,
        "confidence":0.95,
        "evidence":[
            "Exact user sentence"
        ]
    }}
}}

If absent

present=false

confidence=0.0

evidence=[]

Use ONLY indicator IDs from the knowledge base.

Never invent evidence.

==========================================================
COVERED TOPICS
==========================================================

Return major topics only.

Examples

work

career

sleep

college

health

family

relationship

money

stress

anxiety

==========================================================

Return ONLY valid JSON.

No markdown.

No explanation.

No code fences.
"""

# --------------------------------------------------
# Empty Symptom JSON
# --------------------------------------------------

def build_empty_symptom_json():

    symptoms = {}

    for category in knowledge.values():

        for indicator in category:

            symptoms[indicator["id"]] = {

                "present": False,

                "confidence": 0.0,

                "evidence": []

            }

    return symptoms


# --------------------------------------------------
# Empty Analysis
# --------------------------------------------------

def empty_analysis():

    return {

        "conversation_summary": {

            "main_issue": "",

            "overall_summary": "",

            "current_stage": "early",

            "protective_factors": [],

            "risk_observations": []

        },

        "symptom_json": build_empty_symptom_json(),

        "covered_topics": []

    }


# --------------------------------------------------
# JSON Cleaner
# --------------------------------------------------

def clean_json(text: str):

    text = text.strip()

    if text.startswith("```json"):

        text = text.replace("```json", "", 1)

    elif text.startswith("```"):

        text = text.replace("```", "", 1)

    if text.endswith("```"):

        text = text[:-3]

    return text.strip()


# --------------------------------------------------
# JSON Parser
# --------------------------------------------------

def parse_analysis(response_text):

    try:

        cleaned = clean_json(response_text)

        data = json.loads(cleaned)

    except Exception:

        return empty_analysis()

    # -----------------------------
    # Ensure top-level keys exist
    # -----------------------------

    data.setdefault(
        "conversation_summary",
        {}
    )

    data.setdefault(
        "symptom_json",
        {}
    )

    data.setdefault(
        "covered_topics",
        []
    )

    summary = data["conversation_summary"]

    summary.setdefault(
        "main_issue",
        ""
    )

    summary.setdefault(
        "overall_summary",
        ""
    )

    summary.setdefault(
        "current_stage",
        "early"
    )

    summary.setdefault(
        "protective_factors",
        []
    )

    summary.setdefault(
        "risk_observations",
        []
    )

    # -----------------------------
    # Ensure every KB indicator exists
    # -----------------------------

    empty = build_empty_symptom_json()

    for key, value in empty.items():

        if key not in data["symptom_json"]:

            data["symptom_json"][key] = value

    return data


# --------------------------------------------------
# Main Analysis Function
# --------------------------------------------------

def generate_analysis(
    conversation,
    groq_model
):
    """
    Analyze the complete conversation.

    Returns:
        {
            conversation_summary,
            symptom_json,
            covered_topics
        }
    """

    conversation_text = ""

    for message in conversation:

        role = message.get("role", "user").capitalize()

        content = message.get("content", "")

        conversation_text += f"{role}: {content}\n"

    messages = [

        SystemMessage(
            content=build_prompt()
        ),

        HumanMessage(
            content=conversation_text
        )

    ]

    result = groq_model.invoke(messages)

    return parse_analysis(
        result.content
    )


# --------------------------------------------------
# Create Shared Groq Model
# --------------------------------------------------

def load_groq_model(api_key):
    """
    Creates a reusable ChatGroq instance.

    This should be called ONLY ONCE inside
    Modal @enter().
    """

    return ChatGroq(

        model_name="llama-3.3-70b-versatile",

        api_key=api_key,

        temperature=0,

        max_retries=2

    )