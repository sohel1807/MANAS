from datetime import datetime

from score_mapper import apply_symptom_evidence


# ==========================================================
# PHQ-9 Severity
# ==========================================================

def phq9_severity(score):

    if score <= 4:
        return "Minimal"

    if score <= 9:
        return "Mild"

    if score <= 14:
        return "Moderate"

    if score <= 19:
        return "Moderately Severe"

    return "Severe"


# ==========================================================
# GAD-7 Severity
# ==========================================================

def gad7_severity(score):

    if score <= 4:
        return "Minimal"

    if score <= 9:
        return "Mild"

    if score <= 14:
        return "Moderate"

    return "Severe"


# ==========================================================
# Overall Risk
# ==========================================================

def overall_risk(
    phq_severity,
    gad_severity
):

    severity_rank = {

        "Minimal": 0,
        "Mild": 1,
        "Moderate": 2,
        "Moderately Severe": 3,
        "Severe": 4

    }

    highest = max(

        severity_rank[phq_severity],

        severity_rank[gad_severity]

    )

    if highest == 0:
        return "Low"

    elif highest == 1:
        return "Mild"

    elif highest == 2:
        return "Moderate"

    else:
        return "High"


# ==========================================================
# Dominant Areas
# ==========================================================

def extract_dominant_areas(
    symptom_json,
    top_k=3
):

    symptoms = symptom_json.get(
        "symptoms",
        symptom_json
    )

    areas = []

    for symptom, data in symptoms.items():

        if not isinstance(data, dict):
            continue

        if data.get("present"):

            areas.append(

                symptom
                .replace("_", " ")
                .title()

            )

    return areas[:top_k]


# ==========================================================
# Build Final Assessment JSON
# ==========================================================

def build_assessment(

    parsed_response,

    symptom_json,

    conversation_summary

):

    # ------------------------------------------------------
    # Apply symptom evidence using assessment_mapping
    # ------------------------------------------------------

    mapped_scores = apply_symptom_evidence(

        parsed_response,

        symptom_json

    )

    phq_items = mapped_scores["phq9"]

    gad_items = mapped_scores["gad7"]

    # ------------------------------------------------------
    # Calculate Scores
    # ------------------------------------------------------

    phq_score = sum(
        phq_items.values()
    )

    gad_score = sum(
        gad_items.values()
    )

    # ------------------------------------------------------
    # Calculate Severity
    # ------------------------------------------------------

    phq_severity = phq9_severity(
        phq_score
    )

    gad_severity = gad7_severity(
        gad_score
    )

    # ------------------------------------------------------
    # Final JSON
    # ------------------------------------------------------

    return {

        "generated_at":

        datetime.utcnow().isoformat(),

        "phq9": {

            "score":

            phq_score,

            "severity":

            phq_severity,

            "item_scores":

            phq_items

        },

        "gad7": {

            "score":

            gad_score,

            "severity":

            gad_severity,

            "item_scores":

            gad_items

        },

        "overall_risk": {

            "level":

            overall_risk(

                phq_severity,

                gad_severity

            )

        },

        "wellness_insights": {

            "dominant_areas":

            extract_dominant_areas(

                symptom_json

            ),

            "strengths":

            conversation_summary.get(

                "protective_factors",

                []

            )

        }

    }