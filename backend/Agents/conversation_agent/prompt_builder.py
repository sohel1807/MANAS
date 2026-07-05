from langchain_core.messages import SystemMessage, HumanMessage

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# import json

# with open("C:\\Users\\sm\\OneDrive\\Documents\\CDAC_PROJECT\\backend\\Knowledge_base\\mental_health_indicators.json", "r", encoding="utf-8") as f:
#     knowledge_base = json.load(f)


def build_prompt(chat_history, user_message):

    with open("system_prompt.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read()

    assessment_context = """
Mental health areas that may naturally appear:

- Interest and enjoyment
- Mood
- Sleep
- Energy
- Appetite
- Self-worth
- Concentration
- Activity level
- Safety
- Nervousness
- Worry
- Relaxation
- Restlessness
- Irritability
- Fear

Do not ask about every topic.
Do not ask questionnaire-style questions.
Naturally move to another area if enough information has already been gathered.
"""

    messages = [
        SystemMessage(
            content=f"{system_prompt}\n\n{assessment_context}"
        )
    ]

    messages.extend(chat_history)

    messages.append(HumanMessage(content=user_message))

    return messages