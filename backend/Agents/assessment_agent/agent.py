from prompt_builder import build_prompt
from analysis import analyze as run_analysis
from parser import parse_response
from score import build_assessment
from score_mapper import apply_symptom_evidence


def analyze(
    conversation_summary,
    symptom_json,
    groq_model,
):
    """
    Run the complete assessment pipeline.
    """

    # ------------------------------------------------------
    # Build Prompt
    # ------------------------------------------------------

    prompt = build_prompt(
        conversation_summary=conversation_summary,
        symptom_json=symptom_json,
    )

    # ------------------------------------------------------
    # LLM Assessment
    # ------------------------------------------------------

    response = run_analysis(
        prompt=prompt,
        groq_model=groq_model,
    )

    # ------------------------------------------------------
    # Parse Response
    # ------------------------------------------------------

    parsed_response = parse_response(
    response
    )


    parsed_response = apply_symptom_evidence(
        parsed_response,
        symptom_json
    )

    # ------------------------------------------------------
    # Build Final Assessment
    # ------------------------------------------------------

    assessment = build_assessment(

        parsed_response=parsed_response,

        symptom_json=symptom_json,

        conversation_summary=conversation_summary,

    )

    return assessment