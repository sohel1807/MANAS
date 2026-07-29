# ==========================================================
# Convert severity -> PHQ/GAD frequency score
# ==========================================================

def severity_to_score(level):

    if not level:
        return 0

    mapping = {

        "mild": 1,

        "moderate": 2,

        "severe": 3

    }

    return mapping.get(
        level.lower(),
        0
    )


# ==========================================================
# Apply symptom evidence using LLM assessment mapping
# ==========================================================

def apply_symptom_evidence(

    parsed_response,

    symptom_json

):

    phq_items = parsed_response["phq9"]

    gad_items = parsed_response["gad7"]


    symptoms = symptom_json.get(
        "symptoms",
        symptom_json
    )


    for symptom in symptoms.values():

        if not isinstance(symptom, dict):
            continue

        if not symptom.get("present"):
            continue

        score = severity_to_score(

            symptom.get("severity")

        )


        mapping = symptom.get(

            "assessment_mapping",

            {}

        )


        # ---------------- PHQ-9 ----------------

        for item in mapping.get(

            "phq9",

            []

        ):

            if item in phq_items:

                phq_items[item] = max(

                    phq_items[item],

                    score

                )


        # ---------------- GAD-7 ----------------

        for item in mapping.get(

            "gad7",

            []

        ):

            if item in gad_items:

                gad_items[item] = max(

                    gad_items[item],

                    score

                )


    return {

        "phq9": phq_items,

        "gad7": gad_items

    }