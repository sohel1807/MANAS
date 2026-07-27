import requests
import streamlit as st


def app_sidebar():

    with st.sidebar:

        st.title("🧠 MANAS AI")

        st.caption(
            "Adaptive Mental Wellness Assessment"
        )

        st.divider()

        if st.button(
            "💬 Chat",
            use_container_width=True
        ):
            st.switch_page("app.py")

        if st.button(
            "📊 Dashboard",
            use_container_width=True
        ):
            st.switch_page("pages/dashboard.py")

        if st.button(
            "📜 History",
            use_container_width=True
        ):
            st.switch_page("pages/history.py")

        st.divider()

        if st.button(
            "➕ New Assessment",
            use_container_width=True
        ):

            response = requests.post(
                "https://sohel1807--new-session.modal.run",
                json={
                "user_id": st.session_state.user_id
            }
        )

            if response.status_code == 200:

                st.session_state.messages = []
                st.session_state.session_stopped = False

                st.switch_page("app.py")

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.clear()

            st.switch_page("app.py")