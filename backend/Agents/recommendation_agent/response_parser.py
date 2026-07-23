"""
Response Parser

Parses and validates the LLM response into a Python dictionary.
"""

import json
import re


class ResponseParser:
    """
    Parses the JSON response returned by the LLM.
    """

    def parse(self, response: str) -> dict:
        """
        Parse LLM response.

        Parameters
        ----------
        response : str
            Raw response returned by the LLM.

        Returns
        -------
        dict
            Parsed recommendation JSON.
        """

        if not response:
            raise ValueError("Empty response received from LLM.")

        # --------------------------------------------------
        # Remove Markdown code blocks if present
        # --------------------------------------------------

        cleaned = response.strip()

        cleaned = re.sub(
            r"^```json",
            "",
            cleaned,
            flags=re.IGNORECASE
        )

        cleaned = re.sub(
            r"^```",
            "",
            cleaned
        )

        cleaned = re.sub(
            r"```$",
            "",
            cleaned
        )

        cleaned = cleaned.strip()

        # --------------------------------------------------
        # Parse JSON
        # --------------------------------------------------

        try:
            parsed = json.loads(cleaned)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON returned by LLM.\n{e}"
            )

        # --------------------------------------------------
        # Basic Validation
        # --------------------------------------------------

        if not isinstance(parsed, dict):
            raise ValueError(
                "Recommendation response must be a JSON object."
            )

        return parsed