import os

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage


# ==========================================================
# Load Groq Model
# ==========================================================

def load_groq_model(
    groq_api_key,
):
    """
    Load the Groq LLM.
    """

    return ChatGroq(

        api_key=groq_api_key,

        model="llama-3.3-70b-versatile",

        temperature=0,

    )


# ==========================================================
# Assessment Analysis
# ==========================================================

def analyze(

    prompt,

    groq_model,

):

    """
    Run assessment LLM.

    Input:
        Complete assessment prompt

    Output:
        Raw LLM response string
    """

    try:


        response = groq_model.invoke(

            [

                HumanMessage(

                    content=prompt

                )

            ]

        )


        return response.content



    except Exception as e:


        print(
            "Assessment LLM Error:",
            e
        )


        # Return valid empty JSON
        # so parser does not fail

        return """
        {
            "phq9": {},
            "gad7": {}
        }
        """