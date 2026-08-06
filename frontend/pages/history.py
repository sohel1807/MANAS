import streamlit as st
import requests

from components.sidebar import app_sidebar

st.set_page_config(
    page_title="History",
    page_icon="📜",
    layout="wide"
)


# Login Check


if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.switch_page("app.py")


app_sidebar()

st.title("📜 Assessment History")

st.divider()


# Load History


response = requests.get(
    "https://sohel1807--history.modal.run",
    params={
        "user_id": st.session_state.user_id
    }
)

if response.status_code != 200:

    st.error("Unable to load history")

    st.stop()

history = response.json()

if len(history) == 0:

    st.info("No previous assessments found.")

    st.stop()


# History Cards


for report in history:

    col1, col2, col3 = st.columns([3,2,1])

    with col1:

        st.write(
            f"**{report['completed_at']}**"
        )

    with col2:

        st.write(
            f"Risk : **{report['risk']}**"
        )

    with col3:

        if st.button(
            "View Report",
            key=report["history_id"]
        ):

            response = requests.get(
                "https://sohel1807--history-report.modal.run",
                params={
                    "history_id": report["history_id"]
                }
            )

            st.session_state.messages = []
            st.session_state.session_stopped = False
            st.session_state.history_data = response.json()

            st.switch_page(
                "pages/dashboard.py"
            )