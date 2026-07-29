from transformers import pipeline

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"


def load_emotion_model():
    """
    Load the Hugging Face emotion classification model.
    """

    return pipeline(
        task="text-classification",
        model=MODEL_NAME,
        top_k=None
    )


def predict_emotions(
    text: str,
    emotion_model,
    top_k: int = 3
):
    """
    Predict the top-k emotions for a piece of text.

    Args:
        text (str)
        emotion_model
        top_k (int)

    Returns:
        list
    """

    if not text.strip():
        return []

    predictions = emotion_model(text)[0]

    predictions.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return [
        {
            "emotion": prediction["label"],
            "confidence": round(
                float(prediction["score"]),
                3
            )
        }
        for prediction in predictions[:top_k]
    ]