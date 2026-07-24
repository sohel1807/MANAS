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
            st.info(
                "Coming Soon"
            )

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            st.session_state.clear()

            st.switch_page("app.py")