import json



PHQ9_ITEMS = [

    "interest",
    "depressed_mood",
    "sleep",
    "energy",
    "appetite",
    "guilt",
    "concentration",
    "movement",
    "self_harm"

]


GAD7_ITEMS = [

    "nervousness",
    "control_worry",
    "excessive_worry",
    "relaxing",
    "restlessness",
    "irritability",
    "fear"

]



# ==========================================================
# Validate Score
# ==========================================================

def validate_score(value):

    try:

        value = int(value)

    except Exception:

        return 0


    return min(
        max(value,0),
       3
    )



# ==========================================================
# Clean LLM Response
# ==========================================================

def clean_json_response(response):

    """
    Remove markdown formatting
    from LLM JSON response.
    """


    response = response.strip()


    if "```json" in response:

        response = (
            response
            .replace("```json","")
            .replace("```","")
            .strip()
        )


    return response



# ==========================================================
# Parse Assessment Response
# ==========================================================

def parse_response(response):


    response = clean_json_response(
        response
    )


    try:

        data = json.loads(
            response
        )


    except Exception:


        data = {}



    phq9 = {}

    gad7 = {}



    # -------------------------
    # PHQ-9
    # -------------------------

    for item in PHQ9_ITEMS:


        phq9[item] = validate_score(

            data.get(
                "phq9",
                {}
            ).get(
                item,
                0
            )

        )



    # -------------------------
    # GAD-7
    # -------------------------

    for item in GAD7_ITEMS:


        gad7[item] = validate_score(

            data.get(
                "gad7",
                {}
            ).get(
                item,
                0
            )

        )



    return {


        "phq9": phq9,


        "gad7": gad7


    }