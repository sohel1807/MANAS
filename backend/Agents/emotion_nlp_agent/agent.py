from emotion_model import predict_emotion

from analysis import generate_analysis


# ==========================================================
# Main Analysis Pipeline
# ==========================================================

def analyze(
    recent_messages,
    conversation_summary,
    symptom_json,
    covered_topics,
    emotion_model,
    groq_model,
):
    """
    Complete Emotion + NLP Analysis Pipeline.

    Parameters
    ----------
    recent_messages : list

    conversation_summary : dict

    symptom_json : dict

    covered_topics : list

    emotion_model

    groq_model

    Returns
    -------
    dict
    """

    # --------------------------------------------------
    # Find Latest User Message
    # --------------------------------------------------

# --------------------------------------------------
# Last 3 User Messages
# --------------------------------------------------

    user_messages = []

    for message in recent_messages:

        if message["role"] == "user":

            text = message["content"].strip()

        if text:

            user_messages.append(text)

    emotion_text = "\n".join(user_messages[-3:])
    # --------------------------------------------------
    # Emotion Prediction
    # --------------------------------------------------

    emotion_json = predict_emotion(emotion_text,emotion_model)
    # --------------------------------------------------
    # Rolling Memory Analysis
    # --------------------------------------------------

    analysis = generate_analysis(

        recent_messages=recent_messages,

        conversation_summary=conversation_summary,

        symptom_json=symptom_json,

        covered_topics=covered_topics,

        groq_model=groq_model

    )

    # --------------------------------------------------
    # Attach Emotion
    # --------------------------------------------------

    analysis["emotion_json"] = emotion_json

    return analysis