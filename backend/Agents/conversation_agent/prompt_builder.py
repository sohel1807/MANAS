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
    conversation_context=None,
):

    system_prompt = load_system_prompt()

    context = []

    if conversation_context:

        context.append(
            "Conversation Context:\n"
            + json.dumps(
                conversation_context,
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