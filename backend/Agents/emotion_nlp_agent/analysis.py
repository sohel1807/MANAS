import json
import re

from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from Knowledge_base.loader import load_knowledge_base


# ==========================================================
# Load Knowledge Base (Only Once)
# ==========================================================

knowledge = load_knowledge_base()


# ==========================================================
# Prompt Builder
# ==========================================================

def build_prompt():

    return f"""
You are an expert Mental Health NLP Analysis Engine.

Your ONLY task is to update structured conversation memory.

You are NOT a chatbot.

Do NOT answer the user.

Do NOT provide advice.

Do NOT diagnose.

Use ONLY the Mental Health Knowledge Base below while extracting symptoms.

==========================================================
MENTAL HEALTH KNOWLEDGE BASE
==========================================================

{json.dumps(knowledge, indent=2)}

==========================================================
INPUT
==========================================================

You will receive ONE JSON object containing:

{{
    "conversation_summary": {{ ... }},
    "covered_topics": [...],
    "symptom_json": {{ ... }},
    "recent_messages": [...]
}}

The conversation_summary, symptom_json and covered_topics
represent PREVIOUSLY STORED MEMORY.

recent_messages contains ONLY the latest messages.

==========================================================
YOUR TASK
==========================================================

Update the existing memory.

Do NOT recreate everything from scratch.

Preserve information that is still valid.

Update only when recent_messages provide new evidence.

Merge previous memory with new conversation.

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

1. main_issue

One short sentence describing the user's primary concern.

Examples:

Work stress

Academic pressure

Relationship conflict

Sleep issues

Financial worries

2. overall_summary

Write 2–3 concise sentences.

Update the previous summary using the recent conversation.

Do NOT discard previously known information unless it is clearly contradicted.

3. current_stage

Must be exactly one of:

early

exploring

moderate

well_understood

4. protective_factors

Keep existing protective factors.

Add newly discovered strengths.

Remove only if clearly contradicted.

Examples:

supportive family

good friends

stable job

exercise

therapy

healthy coping

5. risk_observations

Return ONLY symptoms clearly supported by evidence.

Each observation:

{{
    "symptom":"",
    "present":true,
    "confidence":0.95
}}

Never diagnose.

Never invent symptoms.

==========================================================
SYMPTOM EXTRACTION RULES
==========================================================

For EVERY indicator from the knowledge base return

{{
    "<indicator_id>":
    {{
        "present": true,
        "confidence": 0.95,
        "evidence": [
            "Exact user sentence"
        ]
    }}
}}

If absent:

present = false

confidence = 0.0

evidence = []

Use ONLY indicator IDs from the knowledge base.

Never invent evidence.

==========================================================
COVERED TOPICS
==========================================================

Merge previous topics with newly discussed topics.

Remove duplicates.

Examples:

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


# ==========================================================
# Empty Symptom JSON
# ==========================================================

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


# ==========================================================
# Empty Analysis
# ==========================================================

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


# ==========================================================
# JSON Cleaner
# ==========================================================

def clean_json(text: str):

    text = text.strip()

    if text.startswith("```json"):

        text = text.replace("```json", "", 1)

    elif text.startswith("```"):

        text = text.replace("```", "", 1)

    if text.endswith("```"):

        text = text[:-3]

    text = re.sub(r"^json\s*", "", text, flags=re.IGNORECASE)

    return text.strip()

# ==========================================================
# JSON Parser
# ==========================================================

def parse_analysis(response_text):

    try:

        cleaned = clean_json(response_text)

        data = json.loads(cleaned)

    except Exception:

        return empty_analysis()

    # ------------------------------------------------------
    # Top Level Keys
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Summary Defaults
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Stage Validation
    # ------------------------------------------------------

    valid_stages = {

        "early",

        "exploring",

        "moderate",

        "well_understood"

    }

    if summary["current_stage"] not in valid_stages:

        summary["current_stage"] = "early"

    # ------------------------------------------------------
    # Ensure Every Symptom Exists
    # ------------------------------------------------------

    empty = build_empty_symptom_json()

    for key, value in empty.items():

        if key not in data["symptom_json"]:

            data["symptom_json"][key] = value

        else:

            symptom = data["symptom_json"][key]

            symptom.setdefault(
                "present",
                False
            )

            symptom.setdefault(
                "confidence",
                0.0
            )

            symptom.setdefault(
                "evidence",
                []
            )

            # ----------------------------------------------
            # Type Validation
            # ----------------------------------------------

            symptom["present"] = bool(
                symptom["present"]
            )

            try:

                symptom["confidence"] = float(
                    symptom["confidence"]
                )

            except Exception:

                symptom["confidence"] = 0.0

            if not isinstance(
                symptom["evidence"],
                list
            ):

                symptom["evidence"] = []

            cleaned_evidence = []

            seen = set()

            for evidence in symptom["evidence"]:

                if not isinstance(
                    evidence,
                    str
                ):

                    continue

                evidence = evidence.strip()

                if evidence == "":

                    continue

                if evidence in seen:

                    continue

                seen.add(evidence)

                cleaned_evidence.append(
                    evidence
                )

            symptom["evidence"] = cleaned_evidence

    # ------------------------------------------------------
    # Remove Unknown Symptom IDs
    # ------------------------------------------------------

    valid_ids = set(empty.keys())

    invalid = []

    for key in data["symptom_json"]:

        if key not in valid_ids:

            invalid.append(key)

    for key in invalid:

        del data["symptom_json"][key]

    # ------------------------------------------------------
    # Covered Topics Cleanup
    # ------------------------------------------------------

    if not isinstance(

        data["covered_topics"],

        list

    ):

        data["covered_topics"] = []

    cleaned_topics = []

    seen = set()

    for topic in data["covered_topics"]:

        if not isinstance(topic, str):

            continue

        topic = topic.strip().lower()

        if topic == "":

            continue

        if topic in seen:

            continue

        seen.add(topic)

        cleaned_topics.append(topic)

    data["covered_topics"] = cleaned_topics

    # ------------------------------------------------------
    # Protective Factors Cleanup
    # ------------------------------------------------------

    if not isinstance(
        summary["protective_factors"],
        list
    ):

        summary["protective_factors"] = []

    cleaned_pf = []

    seen = set()

    for item in summary["protective_factors"]:

        if not isinstance(item, str):

            continue

        item = item.strip()

        if item == "":

            continue

        if item.lower() in seen:

            continue

        seen.add(item.lower())

        cleaned_pf.append(item)

    summary["protective_factors"] = cleaned_pf

    # ------------------------------------------------------
    # Risk Observations Validation
    # ------------------------------------------------------

    if not isinstance(
        summary["risk_observations"],
        list
    ):

        summary["risk_observations"] = []

    validated = []

    for obs in summary["risk_observations"]:

        if not isinstance(obs, dict):

            continue

        try:

            confidence = float(
                obs.get(
                    "confidence",
                    0.0
                )
            )

        except Exception:

            confidence = 0.0

        validated.append({

            "symptom": str(
                obs.get(
                    "symptom",
                    ""
                )
            ),

            "present": bool(
                obs.get(
                    "present",
                    False
                )
            ),

            "confidence": confidence

        })

    summary["risk_observations"] = validated

    # ------------------------------------------------------
    # Return Cleaned Analysis
    # ------------------------------------------------------

    return data

# ==========================================================
# Main Analysis Function
# ==========================================================

def generate_analysis(
    recent_messages,
    conversation_summary,
    symptom_json,
    covered_topics,
    groq_model
):
    """
    Updates the conversation memory using rolling context.

    Parameters
    ----------
    recent_messages : list
        Last few conversation messages.

    conversation_summary : dict
        Previously stored summary.

    symptom_json : dict
        Previously detected symptoms.

    covered_topics : list
        Previously covered topics.

    groq_model : ChatGroq

    Returns
    -------
    dict
        {
            conversation_summary,
            symptom_json,
            covered_topics
        }
    """

    payload = {

        "conversation_summary": conversation_summary,

        "covered_topics": covered_topics,

        "symptom_json": symptom_json,

        "recent_messages": recent_messages

    }

    messages = [

        SystemMessage(
            content=build_prompt()
        ),

        HumanMessage(
            content=json.dumps(
                payload,
                indent=2,
                ensure_ascii=False
            )
        )

    ]

    result = groq_model.invoke(messages)

    analysis = parse_analysis(result.content)

    return analysis


# ==========================================================
# Shared Groq Model
# ==========================================================

def load_groq_model(api_key):
    """
    Creates a reusable ChatGroq instance.

    This should be called ONLY ONCE during
    application startup (Modal @enter()).
    """

    return ChatGroq(

        model_name="llama-3.3-70b-versatile",

        api_key=api_key,

        temperature=0,

        max_retries=2,

    )