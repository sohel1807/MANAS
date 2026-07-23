"""
Prompt Builder

Builds the final prompt for the Recommendation LLM.
"""


class PromptBuilder:

    def build(
        self,
        data: dict,
        documents: list
    ) -> str:

        conversation_summary = data.get(
            "conversation_summary",
            {}
        )

        emotion_summary = data.get(
            "emotion_summary",
            []
        )

        assessment = data.get(
            "assessment",
            {}
        )

        # =====================================================
        # Build Retrieved Knowledge Context
        # =====================================================

        knowledge_chunks = []

        for i, doc in enumerate(documents, start=1):

            metadata = doc.get("metadata", {})

            source = metadata.get("source", "Unknown")

            score = round(doc.get("score", 0), 3)

            content = doc.get("content", "")

            knowledge_chunks.append(
                f"""
Document {i}

Source: {source}
Similarity Score: {score}

Content:
{content}
"""
            )

        knowledge_context = "\n".join(knowledge_chunks)

        # =====================================================
        # Example Output
        # =====================================================

        example_json = """
{
  "wellness_recommendations": [
    {
      "title": "Manage Placement Anxiety",
      "description": "Your responses suggest that worries about placements are contributing to your anxiety. Learning to identify anxious thoughts and viewing situations more realistically can help reduce excessive worry and improve confidence while preparing for placements.",
      "why_recommended": "This recommendation is based on the anxiety-related concerns identified during your conversation and assessment.",
      "benefits": [
        "Reduces excessive worry",
        "Improves emotional resilience",
        "Builds confidence"
      ],
      "references": [
        {
          "document": "Social Anxiety Information Sheet - 07 - Analysing your Thinking.pdf"
        }
      ]
    }
  ],

  "self_care_activities": [
    {
      "title": "Practice Relaxation",
      "description": "Simple relaxation activities such as deep breathing or gentle stretching can help reduce physical tension associated with anxiety.",
      "why_recommended": "These activities may help calm the body's stress response.",
      "benefits": [
        "Reduces muscle tension",
        "Promotes relaxation",
        "Improves emotional balance"
      ],
      "references": [
        {
          "document": "Stress Management.pdf"
        }
      ]
    }
  ],

  "lifestyle_improvements": [],

  "sleep_recommendations": [],

  "stress_management_tips": [],

  "mindfulness_suggestions": [],

  "professional_help": []
}
"""

        # =====================================================
        # Prompt
        # =====================================================

        prompt = f"""
You are MANAS, an AI Mental Wellness Recommendation Assistant.

Your responsibility is to generate supportive, personalized, evidence-based wellness recommendations.

You MUST ONLY use the retrieved knowledge provided below.

==========================================================
Conversation Summary
==========================================================

{conversation_summary}

==========================================================
Emotion Summary
==========================================================

{emotion_summary}

==========================================================
Assessment
==========================================================

{assessment}

==========================================================
Retrieved Knowledge
==========================================================

{knowledge_context}

==========================================================
Instructions
==========================================================

Generate personalized recommendations based on:

- Conversation Summary
- Emotion Summary
- Assessment
- Retrieved Knowledge

Return the following sections whenever relevant:

1. wellness_recommendations
2. self_care_activities
3. lifestyle_improvements
4. sleep_recommendations
5. stress_management_tips
6. mindfulness_suggestions
7. professional_help

For EVERY recommendation include:

- title
- description
- why_recommended
- benefits
- references

Description Guidelines:

- 2–4 sentences.
- Explain WHY this recommendation fits THIS user.
- Mention the user's situation naturally.
- Be supportive and empathetic.
- Do NOT sound like a therapist giving homework.
- Do NOT generate long treatment plans.

Benefits Guidelines:

Return 2–4 concise benefits.

Example:

[
    "Reduces anxiety",
    "Improves emotional resilience",
    "Encourages healthy coping"
]

Reference Rules:

- References MUST ONLY contain document names.
- Never invent document names.
- Use ONLY retrieved documents.
- If multiple retrieved chunks come from the same document,
  include that document ONLY ONCE.
- Do NOT include page numbers.

General Rules:

- Personalize recommendations using the conversation.
- Avoid generic advice.
- Avoid repeating recommendations.
- Avoid repeating document references.
- Never diagnose.
- Never prescribe medication.
- Never invent facts.
- Never recommend anything unsupported by the retrieved knowledge.
- If there is insufficient evidence for a recommendation,
  leave that section empty ([]).

Return ONLY valid JSON.

==========================================================
Example Output
==========================================================

{example_json}
"""

        return prompt