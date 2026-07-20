from emotion_model import predict_emotion
from summary import generate_summary
from nlp_extractor import extract


def analyze(
    conversation,
    api_key,
    emotion_model
):

    # -------------------------
    # Latest User Message
    # -------------------------

    latest_user_message = ""

    for msg in reversed(conversation):

        if msg["role"] == "user":

            latest_user_message = msg["content"]

            break

    # -------------------------
    # Emotion
    # -------------------------

    emotion_json = predict_emotion(
        latest_user_message,
        emotion_model
    )

    # -------------------------
    # Conversation Summary
    # -------------------------

    conversation_summary = generate_summary(
        conversation,
        api_key
    )

    # -------------------------
    # NLP Extraction
    # -------------------------

    extraction = extract(
        conversation,
        api_key
    )

    # -------------------------
    # Final Response
    # -------------------------

    return {

        "conversation_summary": conversation_summary,

        "emotion_json": emotion_json,

        "symptom_json": extraction["symptom_json"],

        "covered_topics": extraction["covered_topics"]

    }