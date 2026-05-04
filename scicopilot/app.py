import streamlit as st

st.set_page_config(page_title="SciCopilot", page_icon="🔬")

st.title("🔬 SciCopilot")
st.markdown("### AI-Aided Research Tools for Scientists")

st.markdown("---")
st.markdown("### Available Tools")

col1, col2 = st.columns(2)

with col1:
    st.info("**SciCoauthor**")
    st.markdown("- Thesis Writer")
    st.markdown("- Literature Review Writer")

with col2:
    st.info("**SciCo-search**")
    st.markdown("- Semantic Search of Research Articles")
    st.markdown("- Best Target Labs Finder")

st.markdown("---")
st.markdown("*Development features available in [SciColab](../scicolab)*")