from pathlib import Path
import json


SYSTEM_PROMPT_PATH = Path(__file__).parent / "system_prompt.txt"


def load_system_prompt():

    with open(
        SYSTEM_PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()


def build_prompt(
    chat_history,
    user_message,
    conversation_summary=None,
    covered_topics=None,
    emotion_json=None,
    symptom_json=None,
):

    system_prompt = load_system_prompt()

    context = []

    # --------------------------------------------------
    # Conversation Summary
    # --------------------------------------------------

    if conversation_summary:

        context.append(
            "Conversation Summary:\n"
            + json.dumps(
                conversation_summary,
                indent=2
            )
        )

    # --------------------------------------------------
    # Emotion
    # --------------------------------------------------

    if emotion_json:

        context.append(
            "Detected Emotion:\n"
            + json.dumps(
                emotion_json,
                indent=2
            )
        )

    # --------------------------------------------------
    # Symptoms
    # --------------------------------------------------

    if symptom_json:

        context.append(
            "Symptoms:\n"
            + json.dumps(
                symptom_json,
                indent=2
            )
        )

    # --------------------------------------------------
    # Covered Topics
    # --------------------------------------------------

    if covered_topics:

        context.append(
            "Covered Topics:\n"
            + json.dumps(
                covered_topics,
                indent=2
            )
        )

    if context:

        system_prompt += "\n\n"

        system_prompt += "\n\n".join(context)

    messages = [

        {
            "role": "system",
            "content": system_prompt
        }

    ]

    # --------------------------------------------------
    # Recent Chat History
    # --------------------------------------------------

    for msg in chat_history[-8:]:

        messages.append(msg)

    # --------------------------------------------------
    # Current User Message
    # --------------------------------------------------

    messages.append(

        {
            "role": "user",
            "content": user_message
        }

    )

    return messages