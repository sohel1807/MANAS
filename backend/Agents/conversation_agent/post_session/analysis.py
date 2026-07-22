import requests


# ==========================================================
# Analysis Agent Endpoint
# ==========================================================

ANALYSIS_AGENT_URL = (
    "https://atharva7758--analysis-dev.modal.run"
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