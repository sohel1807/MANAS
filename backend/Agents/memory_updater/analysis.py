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

    return """
You are responsible for maintaining the long-term memory of a mental health conversation.

INPUT

- conversation_summary
- covered_topics
- recent_messages

The first two represent the existing database state.

Update ONLY using recent_messages.

--------------------------------------------------
GENERAL RULES
--------------------------------------------------

- Preserve existing information unless new evidence appears.
- Never invent information.
- Never infer unsupported facts.
- Never delete information unless the user clearly contradicts it.
- If nothing changed, return the previous memory unchanged.

==================================================
conversation_summary
==================================================

main_issue

- Keep the current value unless the user's primary concern changes.

overall_summary

- Maximum 100 words.
- Include only long-term information.
- Ignore greetings, acknowledgements and repetition.

current_stage

Must be one of:

early
exploring
moderate
well_understood

Advance gradually.

protective_factors

- Preserve previous factors.
- Append new factors.
- Never duplicate.

risk_observations

- Include only directly supported observations.
- Never diagnose.
- Never infer unsupported risks.

==================================================
covered_topics
==================================================

covered_topics MUST be:

{
    "general": [],
    "phq9": [],
    "gad7": []
}

Rules:

GENERAL

Topics discussed outside PHQ/GAD.

PHQ9

Only include:

interest
depressed_mood
sleep
energy
appetite
worthlessness
concentration
psychomotor
suicidal_thoughts

GAD7

Only include:

nervousness
uncontrollable_worry
excessive_worry
relaxation
restlessness
irritability
fear

Append only after meaningful discussion.

Never duplicate.

Never remove topics.

==================================================

Return ONLY valid JSON.

{
    "conversation_summary": {
        "main_issue": "",
        "overall_summary": "",
        "current_stage": "",
        "protective_factors": [],
        "risk_observations": []
    },

    "covered_topics": {
        "general": [],
        "phq9": [],
        "gad7": []
    }
}

No markdown.

No explanation.
"""


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

        "covered_topics": {

            "general": [],

            "phq9": [],

            "gad7": []

        }

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

    text = re.sub(
        r"^json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

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
    # Top Level Defaults
    # ------------------------------------------------------

    if not isinstance(data, dict):
        return empty_analysis()

    data.setdefault(
        "conversation_summary",
        {}
    )

    data.setdefault(
        "covered_topics",
        {}
    )

    summary = data["conversation_summary"]

    # ------------------------------------------------------
    # Summary Defaults
    # ------------------------------------------------------

    if not isinstance(summary, dict):
        summary = {}

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

    valid_stages = {

        "early",

        "exploring",

        "moderate",

        "well_understood"

    }

    if summary["current_stage"] not in valid_stages:

        summary["current_stage"] = "early"

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
    # Risk Observations Cleanup
    # ------------------------------------------------------

    if not isinstance(
        summary["risk_observations"],
        list
    ):

        summary["risk_observations"] = []

    cleaned_risk = []

    for item in summary["risk_observations"]:

        if isinstance(item, str):

            item = item.strip()

            if item:

                cleaned_risk.append(item)

    summary["risk_observations"] = cleaned_risk

    data["conversation_summary"] = summary

    # ------------------------------------------------------
    # Covered Topics Validation
    # ------------------------------------------------------

    if not isinstance(
        data["covered_topics"],
        dict
    ):

        data["covered_topics"] = {}

    covered = data["covered_topics"]

    for section in [

        "general",

        "phq9",

        "gad7"

    ]:

        if section not in covered:

            covered[section] = []

        if not isinstance(

            covered[section],

            list

        ):

            covered[section] = []

        cleaned = []

        seen = set()

        for topic in covered[section]:

            if not isinstance(topic, str):

                continue

            topic = topic.strip().lower()

            if topic == "":

                continue

            if topic in seen:

                continue

            seen.add(topic)

            cleaned.append(topic)

        covered[section] = cleaned

    data["covered_topics"] = covered

    # ------------------------------------------------------
    # Return
    # ------------------------------------------------------

    return data

# ==========================================================
# Main Analysis Function
# ==========================================================

def generate_analysis(
    recent_messages,
    conversation_summary,
    covered_topics,
    groq_model,
):
    """
    Updates long-term conversation memory.

    Parameters
    ----------
    recent_messages : list
        Recent chat history.

    conversation_summary : dict
        Existing conversation summary.

    covered_topics : dict
        Existing covered topics.

    groq_model : ChatGroq
        Shared Groq model.

    Returns
    -------
    dict
        {
            "conversation_summary": {...},
            "covered_topics": {
                "general": [],
                "phq9": [],
                "gad7": []
            }
        }
    """

    # ------------------------------------------------------
    # Prepare Payload
    # ------------------------------------------------------

    payload = {

        "conversation_summary": conversation_summary,

        "covered_topics": covered_topics,

        "recent_messages": recent_messages

    }

    # ------------------------------------------------------
    # Prompt
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # LLM Call
    # ------------------------------------------------------

    try:

        result = groq_model.invoke(messages)

        analysis = parse_analysis(result.content)

        return analysis

    except Exception as e:

        print(f"Memory Analysis Error: {e}")

        return {

            "conversation_summary": conversation_summary,

            "covered_topics": covered_topics

        }
    
# ==========================================================
# Shared Groq Model
# ==========================================================

def load_groq_model(api_key):
    """
    Creates a reusable ChatGroq instance.

    Called once during Modal startup.
    """

    return ChatGroq(

        model_name="llama-3.3-70b-versatile",

        api_key=api_key,

        temperature=0,

        max_retries=2,

    )