import streamlit as st

st.set_page_config(page_title="SciCoauthor", page_icon="✍️")

st.title("✍️ SciCoauthor")
st.markdown("### AI Scientist Coauthor for Thesis & Literature Review")

tool = st.radio("Select Tool", ["Thesis Writer", "Literature Review Writer"])

if tool == "Thesis Writer":
    st.header("Thesis Writer")
    thesis_input = st.text_area("Enter your draft:")
    if st.button("Enhance"):
        st.success("Enhanced thesis text would appear here")

elif tool == "Literature Review Writer":
    st.header("Literature Review Writer")
    topic = st.text_input("Research Topic:")
    if st.button("Generate Review"):
        st.success("Generated literature review would appear here")