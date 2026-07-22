from concurrent.futures import ThreadPoolExecutor

from emotion_model import predict_emotions
from symptom_analysis import extract_symptoms


WINDOW_SIZE = 4
TOP_K_EMOTIONS = 3


# ==========================================================
# Collect User Messages
# ==========================================================

def collect_user_messages(conversation):

    user_messages = []

    user_count = 0

    for conversation_index, message in enumerate(conversation, start=1):

        if message["role"] != "user":
            continue

        user_count += 1

        user_messages.append({

            "user_message_number": user_count,

            "conversation_index": conversation_index,

            "text": message["content"]

        })

    return user_messages


# ==========================================================
# Split Into Windows
# ==========================================================

def split_into_windows(user_messages):

    windows = []

    for start in range(0, len(user_messages), WINDOW_SIZE):

        chunk = user_messages[start:start + WINDOW_SIZE]

        windows.append({

            "messages": chunk,

            "user_messages": {

                "start": chunk[0]["user_message_number"],

                "end": chunk[-1]["user_message_number"]

            },

            "conversation_messages": {

                "start": chunk[0]["conversation_index"],

                "end": chunk[-1]["conversation_index"]

            }

        })

    return windows


# ==========================================================
# Predict Emotions
# ==========================================================

def predict_window_emotions(
    windows,
    emotion_model
):

    for window in windows:

        text = "\n".join(

            message["text"]

            for message in window["messages"]

        )

        window["top_emotions"] = predict_emotions(

            text=text,

            emotion_model=emotion_model,

            top_k=TOP_K_EMOTIONS

        )

        del window["messages"]

    return windows


# ==========================================================
# Build Emotion Timeline
# ==========================================================

def build_emotion_timeline(windows):

    for index, window in enumerate(windows, start=1):

        window["window"] = index

    return windows


# ==========================================================
# Complete Emotion Analysis
# ==========================================================

def analyze_emotions(
    conversation,
    emotion_model
):

    user_messages = collect_user_messages(
        conversation
    )

    windows = split_into_windows(
        user_messages
    )

    windows = predict_window_emotions(
        windows,
        emotion_model
    )

    return build_emotion_timeline(
        windows
    )


# ==========================================================
# Main Analysis
# ==========================================================

def analyze(
    conversation,
    emotion_model,
    groq_model
):

    with ThreadPoolExecutor(max_workers=2) as executor:

        emotion_future = executor.submit(

            analyze_emotions,

            conversation,

            emotion_model

        )

        symptom_future = executor.submit(

            extract_symptoms,

            conversation,

            groq_model

        )

        emotion_timeline = emotion_future.result()

        symptoms = symptom_future.result()

    return {

        "emotion_timeline": emotion_timeline,

        "symptoms": symptoms["symptoms"]

    }