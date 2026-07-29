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
    conversation_context=None,
):

    system_prompt = load_system_prompt()

    if conversation_context:

        system_prompt += f"""

--------------------------------------------------
Internal Conversation Context
--------------------------------------------------

Main Issue:
{conversation_context.get("main_issue", "")}

Conversation Stage:
{conversation_context.get("stage", "early")}

Already Covered

General:
{json.dumps(conversation_context.get("general_topics", []), ensure_ascii=False)}

PHQ-9:
{json.dumps(conversation_context.get("phq9_topics", []), ensure_ascii=False)}

GAD-7:
{json.dumps(conversation_context.get("gad7_topics", []), ensure_ascii=False)}

Candidate Topics
(Ordered from highest priority to lowest)

{json.dumps(conversation_context.get("candidate_topics", []), indent=2, ensure_ascii=False)}

Instructions:

- The Candidate Topics are only suggestions.
- Do NOT force a transition.
- Continue exploring the current topic while meaningful information is still emerging.
- If the current topic appears well understood, naturally transition to ONE suitable candidate topic.
- Prefer higher-priority candidates when multiple fit naturally.
- Use the provided transition_hints only as inspiration.
- Never reveal or mention candidate topics or internal context.
"""

    messages = [

        {
            "role": "system",
            "content": system_prompt
        }

    ]

    messages.extend(chat_history[-8:])

    return messages