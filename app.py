import streamlit as st

st.set_page_config(
    page_title="Read & Test",
    page_icon="📚",
    layout="centered"
)
st.markdown("""
<style>
.stApp {
    background-color: #F7F5EF;
}
h1, h2, h3 {
    color: #405744;
}
.stButton > button {
    background-color: #405744;
    color: white;
    border-radius: 10px;
    width: 100%;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)
st.title("Read & Test")
st.caption("Interactive English Reading Quiz")
st.divider()
if "page" not in st.session_state:
    st.session_state.page = "reading"
if st.session_state.page == "reading":
    st.header("Top Five Food Markets")
    st.write("""
    Read the passage carefully, then answer the questions.
    """)
    with st.container(border=True):
        st.subheader("1. St Lawrence Market")
        st.write("""
        In Canada, there are many different food markets,
        but one of the oldest is St Lawrence Market in Toronto.
        The market is over 200 years old. You can buy meat,
        seafood, and other fresh food there.
        """)

        st.subheader("2. Castries Market")
        st.write("""
        Castries Market is in St Lucia. It is famous for
        its fresh fruit, vegetables, fish, and local products.
        """)

        st.subheader("3. Kreta Ayer Wet Market")
        st.write("""
        This market is in Singapore. You can find fresh food
        downstairs and places to eat upstairs. People enjoy
        local dishes, including breakfast.
        """)

        st.subheader("4. La Vucciria Market")
        st.write("""
        La Vucciria is a famous market in Palermo, Italy.
        You can buy food and enjoy the lively atmosphere.
        Musicians sometimes play and sing there.
        """)

        st.subheader("5. Borough Market")
        st.write("""
        Borough Market is in London, England. It is a popular
        place to buy fresh food. It is a good idea to go early
        because the market can become busy.
        """)
    if st.button("START QUIZ"):
        st.session_state.page = "quiz"
        st.rerun()

elif st.session_state.page == "quiz":

    st.header("Reading Quiz")
    st.write("Answer all 10 questions.")

    with st.form("quiz_form"):

        st.subheader("Part 1: Multiple Choice")

        q1 = st.radio(
            "1. How old is St Lawrence Market?",
            ["100 years old", "Over 200 years old",
             "500 years old", "1,000 years old"]
        )
        q2 = st.radio(
            "2. Where is St Lawrence Market?",
            ["London", "Singapore", "Toronto", "Palermo"]
        )
        q3 = st.radio(
            "3. What can you buy at Castries Market?",
            ["Fresh fruit and vegetables",
             "Only clothes", "Books", "Electronic devices"]
        )
        q4 = st.radio(
            "4. In which country is La Vucciria Market?",
            ["Canada", "Italy", "England", "Singapore"]
        )
        st.subheader("Part 2: True or False")
        q5 = st.radio(
            "5. St Lawrence Market is in Canada.",
            ["True", "False"]
        )
        q6 = st.radio(
            "6. La Vucciria Market is in London.",
            ["True", "False"]
        )
        q7 = st.radio(
            "7. Musicians sometimes play at La Vucciria Market.",
            ["True", "False"]
        )
        st.subheader("Part 3: Short Answer")
        q8 = st.text_input(
            "8. What city is St Lawrence Market in?"
        )
        q9 = st.text_input(
          "9. What is the name of the market in Singapore?"
        )
        q10 = st.text_input(
            "10. Why is it a good idea to go to Borough Market early?"
        )
        submitted = st.form_submit_button("SUBMIT ANSWERS")
    if submitted:
      answers = [
            q1 == "Over 200 years old",
            q2 == "Toronto",
            q3 == "Fresh fruit and vegetables",
            q4 == "Italy",
            q5 == "True",
            q6 == "False",
            q7 == "True",
            q8.strip().lower() in ["toronto"],
            q9.strip().lower() in [
                "kreta ayer wet market",
                "kreta ayer"
            ],
            any(word in q10.strip().lower()
                for word in ["busy", "crowded"])
      ]
      score = sum(answers)
        percentage = score * 10
        st.session_state.score = score
        st.session_state.percentage = percentage
        st.session_state.answers = answers
        st.session_state.page = "results"
        st.rerun()
elif st.session_state.page == "results":
  st.header("Your Results")
    score = st.session_state.score
    percentage = st.session_state.percentage

    st.metric("Your Score", f"{score} / 10")
    st.metric("Your Percentage", f"{percentage}%")

    st.progress(percentage / 100)

    st.write(f"Correct answers: {score}")
    st.write(f"Incorrect answers: {10 - score}")

    if percentage >= 90:
        st.success("Excellent! You did a great job!")
    elif percentage >= 70:
        st.info("Good job! Keep learning!")
    else:
        st.warning("Keep practicing. You can do it!")
      
    if st.button("TRY AGAIN"):
        st.session_state.page = "reading"
        st.rerun()
