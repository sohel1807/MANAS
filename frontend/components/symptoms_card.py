import streamlit as st


def symptom_card(symptoms):

    st.subheader("🩺 Detected Symptoms")

    found = False

    for symptom_name, symptom in symptoms.items():

        if not symptom.get("present", False):
            continue

        found = True

        with st.container(border=True):

            st.markdown(
                f"### {symptom_name.replace('_', ' ').title()}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Severity",
                    symptom.get("severity", "N/A").title()
                )

            with col2:
                confidence = symptom.get("confidence", 0)
                st.metric(
                    "Confidence",
                    f"{confidence:.0%}"
                )

            evidence = symptom.get("evidence", [])

            if evidence:

                st.markdown("**Evidence**")

                for item in evidence:

                    st.write(f"• {item}")

            mapping = symptom.get(
                "assessment_mapping",
                {}
            )

            phq = mapping.get("phq9", [])
            gad = mapping.get("gad7", [])

            if phq:

                st.caption(
                    "PHQ-9: " + ", ".join(phq)
                )

            if gad:

                st.caption(
                    "GAD-7: " + ", ".join(gad)
                )

    if not found:

        st.success(
            "No significant symptoms detected."
        )

    st.divider()