import streamlit as st

# Custom CSS for better alignment, styling, and responsiveness
st.markdown("""
    <style>
    .title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .header, .subheader {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
    }
    .feedback {
        font-size: 14px;
        padding: 10px;
        background-color: #f1f1f1;
        border-radius: 5px;
        margin-top: 10px;
        text-align: center;
    }
    .progress-bar {
        width: 80%;
        background-color: #f3f3f3;
        border-radius: 5px;
        margin-top: 10px;
        margin-left: auto;
        margin-right: auto;
    }
    .progress-bar-inner {
        height: 24px;
        text-align: center;
        line-height: 24px;
        color: white;
        border-radius: 5px;
    }
    .rate-box {
        text-align: center;
    }
    .rate-widget {
        margin-top: -10px;
        text-align: center;
    }
    .ask-section {
        text-align: center;
        margin-bottom: 20px;
    }
    .center-content {
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)


def display_progress(match_percent):
    color = "green" if match_percent > 75 else "orange" if match_percent > 50 else "red"
    st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-bar-inner" style="width:{match_percent}%; background-color:{color};">
                {match_percent}%
            </div>
        </div>
    """, unsafe_allow_html=True)


def main():
    # Title
    st.markdown('<div class="title">Knowledge Assistant</div>', unsafe_allow_html=True)

    # Ask Section
    st.markdown('<div class="header">Ask</div>', unsafe_allow_html=True)
    st.markdown('<div class="ask-section">', unsafe_allow_html=True)

    # Centered content container
    st.markdown('<div class="center-content">', unsafe_allow_html=True)

    user_question = st.text_input("", placeholder="Enter your question here...", label_visibility="collapsed")
    col1, col2 = st.columns([4, 1])

    with col1:
        answer_mode = st.radio("", ['Direct Answer', 'Step by Step'], horizontal=True, label_visibility="collapsed")

    with col2:
        if st.button("Answer"):
            st.markdown("---")
            # Display Answer Section
            st.markdown('<div class="header">Answer</div>', unsafe_allow_html=True)
            answer_col1, answer_col2 = st.columns([3, 1])

            with answer_col1:
                if answer_mode == 'Direct Answer':
                    st.write("Direct answer summary")
                else:
                    st.write("Step-by-step guidance")

            with answer_col2:
                st.markdown('<div class="subheader">Rate this answer</div>', unsafe_allow_html=True)
                with st.container():
                    rating = st.slider("", 1, 5, 3, label_visibility="collapsed")
                    feedback = st.text_area("", placeholder="Provide feedback", label_visibility="collapsed")
                    st.write("")

            st.markdown("---")

            # Knowledge Source Section
            st.markdown('<div class="header">Knowledge Source</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<div class="subheader">RULE/REQUIREMENT</div>', unsafe_allow_html=True)
                display_progress(85)  # Example progress percentage
                st.write("This section displays the rule or requirement.")

            with col2:
                st.markdown('<div class="subheader">INTERPRETATION</div>', unsafe_allow_html=True)
                display_progress(60)  # Example progress percentage
                st.write("Summary of the interpretation and rationale.")
                st.image("https://via.placeholder.com/150", caption="Data Lineage")

            with col3:
                st.markdown('<div class="subheader">IMPLEMENTATION</div>', unsafe_allow_html=True)
                display_progress(40)  # Example progress percentage
                st.code("def implementation():\n    pass  # Implementation code here", language="python")

    st.markdown('</div>', unsafe_allow_html=True)  # Close center-content div
    st.markdown('</div>', unsafe_allow_html=True)  # Close ask-section div


if __name__ == "__main__":
    main()
