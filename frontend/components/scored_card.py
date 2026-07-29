import streamlit as st


def score_card(assessment):

    st.subheader("📊 Assessment Results")

    col1, col2, col3 = st.columns(3)

    # ==========================
    # Overall Risk
    # ==========================

    with col1:

        risk = assessment.get("overall_risk", {})

        st.metric(
            label="Overall Risk",
            value=risk.get("level", "N/A")
        )

        st.caption(
            f"Concern: {risk.get('symptom_concern', 'N/A')}"
        )

    # ==========================
    # PHQ-9
    # ==========================

    with col2:

        phq = assessment.get("phq9", {})

        st.metric(
            label="PHQ-9",
            value=phq.get("score", 0)
        )

        st.caption(
            phq.get("severity", "N/A")
        )

        with st.expander("View PHQ-9 Item Scores"):

            for item, score in phq.get("item_scores", {}).items():

                st.write(
                    f"{item.replace('_',' ').title()}: {score}"
                )

    # ==========================
    # GAD-7
    # ==========================

    with col3:

        gad = assessment.get("gad7", {})

        st.metric(
            label="GAD-7",
            value=gad.get("score", 0)
        )

        st.caption(
            gad.get("severity", "N/A")
        )

        with st.expander("View GAD-7 Item Scores"):

            for item, score in gad.get("item_scores", {}).items():

                st.write(
                    f"{item.replace('_',' ').title()}: {score}"
                )

    # ==========================
    # Wellness Insights
    # ==========================

    insights = assessment.get("wellness_insights", {})

    st.subheader("🌱 Wellness Insights")

    dominant = insights.get("dominant_areas", [])

    strengths = insights.get("strengths", [])

    if dominant:

        st.markdown("**Dominant Areas**")

        for area in dominant:

            st.write(f"• {area}")

    if strengths:

        st.markdown("**Strengths**")

        for strength in strengths:

            st.write(f"• {strength}")

    st.divider()