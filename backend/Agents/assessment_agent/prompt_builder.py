import json
from pathlib import Path



SYSTEM_PROMPT_PATH = (
    Path(__file__).parent /
    "system_prompt.txt"
)



def load_system_prompt():

    with open(
        SYSTEM_PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()



def build_prompt(

    conversation_summary,

    symptom_json,

):

    """
    Build assessment prompt.

    Input:
    - Conversation summary
    - Extracted symptoms

    Output:
    - Complete LLM prompt
    """



    system_prompt = load_system_prompt()



    prompt = f"""
{system_prompt}


Conversation Summary:

{json.dumps(
    conversation_summary,
    indent=2
)}


Extracted Symptoms:

{json.dumps(
    symptom_json,
    indent=2
)}
"""


    return prompt