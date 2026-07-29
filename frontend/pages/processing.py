import streamlit as st
import requests
import time


st.set_page_config(
    page_title="Processing - MANAS AI",
    page_icon="🧠",
    layout="centered"
)


# ==========================
# Check Login
# ==========================

if "logged_in" not in st.session_state or not st.session_state.logged_in:

    st.warning(
        "Please login first"
    )

    st.stop()



# ==========================
# Header
# ==========================

st.title("🧠 MANAS AI")

st.caption(
    "Preparing your assessment report..."
)

st.divider()



# ==========================
# Progress Containers
# ==========================


summary = st.empty()
emotion = st.empty()
symptoms = st.empty()
assessment = st.empty()
recommendation = st.empty()



# Initial State

summary.info(
    "⏳ Conversation Summary"
)

emotion.info(
    "⬜ Emotion Analysis"
)

symptoms.info(
    "⬜ Symptom Extraction"
)

assessment.info(
    "⬜ PHQ/GAD Assessment"
)

recommendation.info(
    "⬜ Recommendations"
)



# ==========================
# Poll Status API
# ==========================


while True:


    try:


        response = requests.get(
            " https://sohel1807--session-status.modal.run",
            params={
                "user_id":
                st.session_state.user_id
            }
        )


        data=response.json()


        status=data["status"]



        if status=="PROCESSING":


            summary.success(
                "✓ Conversation Summary"
            )


            emotion.success(
                "✓ Emotion Analysis"
            )


            symptoms.info(
                "⏳ Symptom Extraction"
            )



        elif status=="COMPLETED":


            summary.success(
                "✓ Conversation Summary"
            )

            emotion.success(
                "✓ Emotion Analysis"
            )

            symptoms.success(
                "✓ Symptom Extraction"
            )

            assessment.success(
                "✓ PHQ/GAD Assessment"
            )

            recommendation.success(
                "✓ Recommendations"
            )


            time.sleep(10)


            st.switch_page(
                "pages/dashboard.py"
            )


        elif status=="FAILED":


            st.error(
                "Assessment failed. Please try again."
            )

            break



    except Exception as e:


        st.error(
            f"Error checking status: {e}"
        )

        break



    time.sleep(10)