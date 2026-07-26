import streamlit as st
import requests
from components.summary_card import summary_card
from components.scored_card import score_card
from components.symptoms_card import symptom_card
from components.emotions_chart import emotion_chart
from components.recommendation_card import recommendation_card
from components.sidebar import app_sidebar

st.set_page_config(
    page_title="Dashboard",
    page_icon="🧠",
    layout="wide"
)

# ============================================
# Check Login
# ============================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.warning("Please login first.")

    st.switch_page("app.py")


app_sidebar()
# ============================================
# Dashboard API
# ============================================

DASHBOARD_API = (
    "https://sohel1807--dashboard.modal.run"
)


# ============================================
# Load Dashboard
# ============================================

with st.spinner("Loading assessment report..."):

    response = requests.get(
        DASHBOARD_API,
        params={
            "user_id": st.session_state.user_id
        }
    )

    if response.status_code != 200:

        st.error("Unable to load dashboard.")

        st.stop()

    data = response.json()


if data["status"] != "COMPLETED":

    st.warning(
        "Assessment is not completed yet."
    )

    st.stop()


summary = data["conversation_summary"]

assessment = data["assessment_json"]

symptoms = data["symptom_json"]

emotions = data["emotion_json"]

recommendations = data["recommendation_json"]


# ============================================
# Header
# ============================================

st.title("🧠 MANAS AI Dashboard")

st.caption(
    "Adaptive Mental Wellness Assessment Report"
)

st.divider()


# ============================================
# Summary
# ============================================

summary_card(summary)

# ============================================
# Risk Cards
# ============================================

score_card(assessment)

# ============================================
# Symptoms
# ============================================

symptom_card(symptoms)

# ============================================
# Emotion Timeline
# ============================================

emotion_chart(emotions)


# ============================================
# Recommendations
# ============================================

recommendation_card(recommendations)

# ============================================
# Bottom Buttons
# ============================================

col1, col2, col3 = st.columns(3)

with col1:

    if st.button("➕ New Assessment"):

        st.info("Coming Soon")

with col2:

    if st.button("📜 History"):

        st.info("Coming Soon")

with col3:

    if st.button("🚪 Logout"):

        st.session_state.clear()

        st.switch_page("app.py")