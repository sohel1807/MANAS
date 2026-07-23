import requests


# ==========================================================
# Analysis Agent Endpoint
# ==========================================================

ANALYSIS_AGENT_URL = (
    "https://atharva7758--analysis.modal.run"
)


# ==========================================================
# Assessment Agent Endpoint
# ==========================================================

ASSESSMENT_AGENT_URL = (
    "https://atharva7758--assessment.modal.run"
)


# ==========================================================
# Call Analysis Agent
# ==========================================================

def call_analysis_agent(conversation):

    response = requests.post(

        ANALYSIS_AGENT_URL,

        json={
            "conversation": conversation
        },

        timeout=300

    )

    response.raise_for_status()

    return response.json()


# ==========================================================
# Call Assessment Agent
# ==========================================================

def call_assessment_agent(
    conversation_summary,
    symptom_json,
):

    response = requests.post(

        ASSESSMENT_AGENT_URL,

        json={

            "conversation_summary":
            conversation_summary,

            "symptom_json":
            symptom_json

        },

        timeout=300

    )

    response.raise_for_status()

    return response.json()