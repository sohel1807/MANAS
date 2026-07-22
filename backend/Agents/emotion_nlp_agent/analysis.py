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

    return f"""You update structured conversation memory.

INPUT

- conversation_summary
- covered_topics
- symptom_json (contains ONLY active symptoms)
- recent_messages

The first three represent the current database state.

Update ONLY using recent_messages.

--------------------------------------------------
GENERAL RULES
--------------------------------------------------

- Preserve existing information unless recent_messages provide clear new evidence.
- Never invent facts.
- Never infer information.
- Never remove information unless the user explicitly contradicts it.
- If nothing meaningful changed, return the previous memory unchanged.

==================================================
conversation_summary
==================================================

main_issue

- Keep the current value unless the user's primary concern clearly changes.

overall_summary

- Maximum 100 words.
- Append only important long-term information.
- Ignore greetings, acknowledgements, repetition and small talk.
- Do not rewrite unless the user's situation meaningfully changes.

current_stage

Must be exactly one of:

early
exploring
moderate
well_understood

Rules:

- Advance gradually.
- Never skip stages.
- Do not move backwards unless the conversation clearly restarts.

protective_factors

- Preserve existing factors.
- Add newly discovered strengths.
- Remove only if explicitly contradicted.

risk_observations

- Include only observations directly supported by the user's statements.
- Never diagnose.
- Never infer unsupported risks.

==================================================
symptom_json
==================================================

Return ONLY active symptoms.

If there are no active symptoms return:

"symptom_json": {{}}

For existing symptoms:

- Keep unchanged if no new evidence exists.
- Append only new evidence.
- Never duplicate evidence.
- Never invent evidence.
- Remove a symptom only if the user explicitly contradicts it.

For new symptoms:

- Add only if directly supported by the user's own words.
- Add only when confidence is high.
- Do not guess.

Each symptom should follow:

{{
  "present": true,
  "confidence": 0.95,
  "evidence": [
    "Exact user statement"
  ]
}}

==================================================
covered_topics
==================================================

Treat covered_topics as permanent conversation history.

- Append only genuinely discussed topics.
- Never duplicate topics.
- Never remove topics.
- Do not add a topic from a passing mention.
- A topic is considered covered only after meaningful discussion.

==================================================

Return ONLY valid JSON.

No markdown.

No explanation.

No code fences.
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

        "symptom_json": {},

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

    if not isinstance(data["symptom_json"], dict):
        data["symptom_json"] = {}

    for symptom in data["symptom_json"].values():

        symptom.setdefault("present", False)
        symptom.setdefault("confidence", 0.0)
        symptom.setdefault("evidence", [])

        symptom["present"] = bool(symptom["present"])

        try:
            symptom["confidence"] = float(symptom["confidence"])
        except Exception:
            symptom["confidence"] = 0.0

        if not isinstance(symptom["evidence"], list):
            symptom["evidence"] = []

        symptom["evidence"] = list(dict.fromkeys([
            e.strip()
            for e in symptom["evidence"]
            if isinstance(e, str) and e.strip()
        ]))

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

    active_symptoms = {}

    for key, value in symptom_json.items():

        if value.get("present"):

            active_symptoms[key] = value

    payload = {

        "conversation_summary": conversation_summary,

        "covered_topics": covered_topics,

        "symptom_json": active_symptoms,

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