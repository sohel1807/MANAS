import streamlit as st
import requests

st.set_page_config(page_title="MANAS AI")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []


if not st.session_state.logged_in:

    st.title("MANAS AI")

    tab1, tab2 = st.tabs(["Login", "Register"])

   
    with tab1:

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):

            response = requests.post(
                "https://sohel1807--login.modal.run",
                json={
                    "email": email,
                    "password": password
                }
            )

            data = response.json()

            if "user_id" in data:

                st.session_state.logged_in = True
                st.session_state.user_id = data["user_id"]

                st.success("Login Successful")
                st.rerun()

            else:
                st.error(data["message"])


    with tab2:

        name = st.text_input("Name", key="register_name")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")

        if st.button("Register"):

            response = requests.post(
                "https://sohel1807--register.modal.run",
                json={
                    "name": name,
                    "email": email,
                    "password": password
                }
            )

            data = response.json()

            if data["message"] == "Registration Successful":
                st.success(data["message"])
            else:
                st.error(data["message"])


else:

    st.title("MANAS AI")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type here...")

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        response = requests.post(
            "https://sohel1807--chat.modal.run",
            json={
                "user_id": st.session_state.user_id,
                "message": user_input
            }
        )

        reply = response.json()["reply"]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        st.rerun()