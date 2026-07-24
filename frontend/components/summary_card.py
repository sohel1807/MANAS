import streamlit as st


def summary_card(summary):

    st.subheader("📝 Conversation Summary")

    st.markdown(
        f"**Main Issue:** {summary.get('main_issue', 'N/A')}"
    )

    st.markdown(
        f"**Current Stage:** {summary.get('current_stage', 'N/A')}"
    )

    st.markdown("**Overall Summary**")

    st.info(
        summary.get(
            "overall_summary",
            "No summary available."
        )
    )


    if summary.get("risk_observations"):

        st.markdown("### ⚠️ Risk Observations")

        for item in summary["risk_observations"]:

            st.write(f"• {item}")


    if summary.get("protective_factors"):

        st.markdown("### ✅ Protective Factors")

        for item in summary["protective_factors"]:

            st.write(f"• {item}")


    st.divider()