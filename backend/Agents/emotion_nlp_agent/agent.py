from emotion_model import predict_emotion
from analysis import generate_analysis


def analyze(
    conversation,
    emotion_model,
    groq_model
):

    # -------------------------
    # Latest User Message
    # -------------------------

    latest_user_message = ""

    for msg in reversed(conversation):

        if msg.get("role") == "user":

            latest_user_message = msg.get("content", "")

            break

    # -------------------------
    # Emotion Prediction
    # -------------------------

    emotion_json = predict_emotion(
        latest_user_message,
        emotion_model
    )

    # -------------------------
    # Conversation Analysis
    # -------------------------

    analysis = generate_analysis(
        conversation=conversation,
        groq_model=groq_model
    )

    # -------------------------
    # Final Response
    # -------------------------

    return {

        "conversation_summary":
            analysis["conversation_summary"],

        "emotion_json":
            emotion_json,

        "symptom_json":
            analysis["symptom_json"],

        "covered_topics":
            analysis["covered_topics"]

    }