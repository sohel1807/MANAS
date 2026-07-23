import requests

RECOMMENDATION_AGENT_URL = "https://atharva7758--recommendation.modal.run"


def call_recommendation_agent(
    conversation_summary,
    emotion_summary,
    symptoms,
    assessment,
):
    payload = {
        "conversation_summary": conversation_summary,
        "emotion_summary": emotion_summary,
        "symptoms": symptoms,
        "assessment": assessment,
    }

    response = requests.post(
        RECOMMENDATION_AGENT_URL,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    return response.json()