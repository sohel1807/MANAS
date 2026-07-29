from analysis import generate_analysis


# ==========================================================
# Main Memory Pipeline
# ==========================================================

def analyze(
    recent_messages,
    conversation_summary,
    covered_topics,
    groq_model,
):
    """
    Complete Conversation Memory Pipeline.

    Parameters
    ----------
    recent_messages : list

    conversation_summary : dict

    covered_topics : dict

    groq_model

    Returns
    -------
    dict
    """

    analysis = generate_analysis(

        recent_messages=recent_messages,

        conversation_summary=conversation_summary,

        covered_topics=covered_topics,

        groq_model=groq_model

    )

    return analysis