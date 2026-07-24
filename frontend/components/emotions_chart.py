import streamlit as st
import pandas as pd


def emotion_chart(emotions):

    st.subheader("😊 Emotion Timeline")

    if not emotions:

        st.info("No emotion data available.")

        st.divider()

        return

    rows = []

    for window in emotions:

        window_no = window.get("window", 0)

        for emotion in window.get("top_emotions", []):

            rows.append(
                {
                    "Window": f"Window {window_no}",
                    "Emotion": emotion["emotion"].title(),
                    "Confidence": emotion["confidence"]
                }
            )

    if not rows:

        st.info("No emotion data available.")

        st.divider()

        return

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        data=df,
        x="Window",
        y="Confidence",
        color="Emotion"
    )

    st.divider()