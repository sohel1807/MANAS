"""
LLM Interface

Handles communication with the Groq LLM.
"""

import os

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage


class RecommendationLLM:
    """
    Wrapper around the Groq LLM used by the Recommendation Agent.
    """

    def __init__(self):

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile",
            temperature=0.2,
        )

    def generate(self, prompt: str) -> str:
        """
        Generate recommendations from the LLM.

        Parameters
        ----------
        prompt : str
            Prompt built by PromptBuilder.

        Returns
        -------
        str
            Raw response from the LLM.
        """

        try:

            response = self.llm.invoke(
                [
                    HumanMessage(
                        content=prompt
                    )
                ]
            )

            return response.content

        except Exception as e:

            raise RuntimeError(
                f"Groq generation failed: {str(e)}"
            ) from e