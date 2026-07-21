from transformers import pipeline


def load_emotion_model():
    """
    Load the Hugging Face emotion model once.
    """

    return pipeline(
        task="text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None
    )


def predict_emotion(
    text,
    emotion_model
):

    if not text or not text.strip():

        return {

            "primary_emotion": "neutral",

            "confidence": 0.0

        }

    predictions = emotion_model(text)[0]

    predictions.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    primary = predictions[0]

    return {

        "primary_emotion": primary["label"],

        "confidence": round(
            primary["score"],
            3
        )

    }