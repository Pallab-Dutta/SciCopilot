import streamlit as st

st.set_page_config(page_title="SciCo-search", page_icon="🔍")

st.title("🔍 SciCo-search")
st.markdown("### Semantic Search for Research")

search_type = st.radio("Select Search Type", ["Research Articles", "Target Labs"])

if search_type == "Research Articles":
    st.header("Research Article Search")
    query = st.text_input("Enter search query:")
    if st.button("Search"):
        st.success("Relevant articles would appear here")

elif search_type == "Target Labs":
    st.header("Target Lab Finder")
    research_area = st.text_input("Research Area:")
    if st.button("Find Labs"):
        st.success("Matching labs would appear here")