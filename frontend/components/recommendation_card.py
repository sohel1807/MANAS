import streamlit as st


def _render_section(title, items):

    if not items:
        return

    st.subheader(title)

    for item in items:

        with st.container(border=True):

            st.markdown(
                f"### {item.get('title','Recommendation')}"
            )

            st.write(
                item.get(
                    "description",
                    "No description available."
                )
            )

            benefits = item.get(
                "benefits",
                []
            )

            if benefits:

                st.markdown("**Benefits**")

                for benefit in benefits:

                    st.write(
                        f"• {benefit}"
                    )

            references = item.get(
                "references",
                []
            )

            if references:

                st.markdown("**References**")

                for ref in references:

                    st.write(
                        f"• {ref.get('document','')}"
                    )

            why = item.get(
                "why_recommended"
            )

            if why:

                st.info(why)


def recommendation_card(recommendations):

    st.header("💡 Personalized Recommendations")

    _render_section(
        "🌱 Self Care Activities",
        recommendations.get(
            "self_care_activities",
            []
        )
    )

    _render_section(
        "🏃 Lifestyle Improvements",
        recommendations.get(
            "lifestyle_improvements",
            []
        )
    )

    _render_section(
        "😴 Sleep Recommendations",
        recommendations.get(
            "sleep_recommendations",
            []
        )
    )

    _render_section(
        "🧘 Mindfulness Suggestions",
        recommendations.get(
            "mindfulness_suggestions",
            []
        )
    )

    _render_section(
        "🌿 Stress Management",
        recommendations.get(
            "stress_management_tips",
            []
        )
    )

    _render_section(
        "👩‍⚕️ Professional Help",
        recommendations.get(
            "professional_help",
            []
        )
    )

    _render_section(
        "❤️ Wellness Recommendations",
        recommendations.get(
            "wellness_recommendations",
            []
        )
    )

    st.divider()