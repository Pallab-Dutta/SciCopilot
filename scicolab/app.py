import streamlit as st

st.set_page_config(page_title="SciColab", page_icon="🧪")

st.title("🧪 SciColab")
st.markdown("### Development & Staging Features")

st.warning("⚠️ These features are not yet published to production")

st.markdown("---")
st.markdown("### Experimental Tools")

feature = st.selectbox("Select Feature", ["New Tool 1", "New Tool 2", "Beta Feature"])

if feature:
    st.info(f"Working on: {feature}")
    user_input = st.text_area("Input:")
    if st.button("Run"):
        st.success("Output would appear here")