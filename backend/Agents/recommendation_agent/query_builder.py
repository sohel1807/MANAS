"""
Query Builder

Builds the semantic search query used for RAG retrieval.
"""


class QueryBuilder:

    def build(self, data: dict) -> str:
        """
        Build retrieval query from conversation,
        emotion and assessment data.
        """

        query_parts = []

        # ==========================================
        # Conversation Summary
        # ==========================================

        conversation = data.get("conversation_summary", {})

        if isinstance(conversation, dict):

            main_issue = conversation.get("main_issue")
            overall_summary = conversation.get("overall_summary")

            if main_issue:
                query_parts.append(f"Main Issue: {main_issue}")

            if overall_summary:
                query_parts.append(overall_summary)

        elif isinstance(conversation, str):

            if conversation.strip():
                query_parts.append(conversation)

        # ==========================================
        # Emotion Summary
        # ==========================================

        emotion_summary = data.get("emotion_summary", [])

        if isinstance(emotion_summary, list):

            emotions = []

            for window in emotion_summary:

                for emotion in window.get("top_emotions", []):

                    name = emotion.get("emotion")

                    if name:
                        emotions.append(name)

            if emotions:
                query_parts.append(
                    "Detected emotions: " +
                    ", ".join(sorted(set(emotions)))
                )

        elif isinstance(emotion_summary, str):

            if emotion_summary.strip():
                query_parts.append(emotion_summary)

        # ==========================================
        # Symptoms
        # ==========================================

        symptoms = data.get("symptoms", {})

        if isinstance(symptoms, dict):

            symptom_names = []

            for symptom, details in symptoms.items():

                if details.get("present"):

                    symptom_names.append(symptom)

            if symptom_names:

                query_parts.append(
                    "Symptoms: " +
                    ", ".join(symptom_names)
                )

        elif isinstance(symptoms, list):

            if symptoms:
                query_parts.append(
                    "Symptoms: " +
                    ", ".join(symptoms)
                )

        # ==========================================
        # Assessment
        # ==========================================

        assessment = data.get("assessment", {})

        gad7 = assessment.get("gad7", {})

        severity = gad7.get("severity")

        if severity:
            query_parts.append(
                f"GAD-7 Severity: {severity}"
            )

        phq9 = assessment.get("phq9", {})

        severity = phq9.get("severity")

        if severity:
            query_parts.append(
                f"PHQ-9 Severity: {severity}"
            )

        # ==========================================
        # Overall Risk
        # ==========================================

        overall_risk = assessment.get("overall_risk", {})

        level = overall_risk.get("level")

        if level:
            query_parts.append(
                f"Overall Risk: {level}"
            )

        # ==========================================
        # Wellness Insights
        # ==========================================

        insights = assessment.get(
            "wellness_insights",
            {}
        )

        dominant = insights.get(
            "dominant_areas",
            []
        )

        if dominant:

            query_parts.append(
                "Dominant Areas: " +
                ", ".join(dominant)
            )

        return "\n".join(query_parts)