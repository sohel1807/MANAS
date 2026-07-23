# ==========================================================
# Convert symptom severity into PHQ/GAD frequency score
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
# Apply symptom evidence to PHQ-9 and GAD-7
# ==========================================================


def apply_symptom_evidence(

    parsed_response,

    symptom_json

):


    phq_items = parsed_response["phq9"]

    gad_items = parsed_response["gad7"]



    # ======================================================
    # GAD-7 Related Symptoms
    # ======================================================


    gad_mapping = {


        # Nervousness / Anxiety

        "anxiety": "nervousness",
        "nervousness": "nervousness",
        "panic": "nervousness",
        "fear": "fear",


        # Worry

        "worry": "excessive_worry",
        "excessive_worry": "excessive_worry",
        "overthinking": "excessive_worry",


        # Control worry

        "control_worry": "control_worry",
        "unable_to_control_worry": "control_worry",


        # Relaxing

        "stress": "relaxing",
        "cannot_relax": "relaxing",
        "relaxing_problem": "relaxing",


        # Restlessness

        "restlessness": "restlessness",
        "restless": "restlessness",


        # Irritability

        "anger": "irritability",
        "irritability": "irritability",
        "frustration": "irritability"

    }



    # ======================================================
    # PHQ-9 Related Symptoms
    # ======================================================


    phq_mapping = {


        # Mood

        "low_mood": "depressed_mood",
        "sadness": "depressed_mood",
        "hopelessness": "depressed_mood",


        # Interest

        "low_interest": "interest",
        "loss_of_interest": "interest",
        "no_motivation": "interest",


        # Sleep

        "sleep_disturbance": "sleep",
        "poor_sleep": "sleep",
        "insomnia": "sleep",
        "sleep_problem": "sleep",


        # Energy

        "low_energy": "energy",
        "fatigue": "energy",
        "tiredness": "energy",


        # Appetite

        "poor_appetite": "appetite",
        "appetite_change": "appetite",


        # Guilt

        "guilt": "guilt",
        "worthlessness": "guilt",


        # Concentration

        "poor_concentration": "concentration",
        "difficulty_focusing": "concentration",


        # Movement

        "movement_change": "movement",
        "agitation": "movement",
        "slow_movement": "movement",


        # Self Harm

        "self_harm": "self_harm",
        "suicidal_thoughts": "self_harm"

    }



    # ======================================================
    # Apply GAD Mapping
    # ======================================================


    for symptom, item in gad_mapping.items():


        data = symptom_json.get(
            symptom
        )


        if isinstance(data, dict):

            if data.get("present"):


                gad_items[item] = severity_to_score(

                    data.get("severity")

                )



    # ======================================================
    # Apply PHQ Mapping
    # ======================================================


    for symptom, item in phq_mapping.items():


        data = symptom_json.get(
            symptom
        )


        if isinstance(data, dict):

            if data.get("present"):


                phq_items[item] = severity_to_score(

                    data.get("severity")

                )



    return {

        "phq9": phq_items,

        "gad7": gad_items

    }