def build_conversation_context(

    conversation_summary,

    covered_topics,

):

    conversation_summary = conversation_summary or {}
    covered_topics = covered_topics or []

    return {

        "main_issue": conversation_summary.get(
            "main_issue",
            ""
        ),

        "stage": conversation_summary.get(
            "current_stage",
            "early"
        ),

        "topics_done": covered_topics

    }