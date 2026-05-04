import streamlit as st

st.set_page_config(page_title="SciCopilot Hub", page_icon="🔬")

st.title("🔬 SciCopilot")
st.markdown("### AI-Aided Research Tools for Scientists")

mode = st.radio("Select Mode", ["SciCopilot (Production)", "SciColab (Development)"])

if mode == "SciCopilot (Production)":
    st.info("Running: SciCopilot")
    st.markdown("---")
    st.markdown("### Published Tools")
    
    tool = st.selectbox("Select Tool", [
        "SciCoauthor - Thesis Writer",
        "SciCoauthor - Literature Review Writer", 
        "SciCo-search - Research Articles",
        "SciCo-search - Target Labs"
    ])
    
    if "Thesis" in tool:
        st.subheader("Thesis Writer")
        draft = st.text_area("Enter your thesis draft:")
        if st.button("Enhance with AI"):
            st.success("Rephrased thesis appears here")
            
    elif "Literature" in tool:
        st.subheader("Literature Review Writer")
        topic = st.text_input("Research topic:")
        if st.button("Generate Review"):
            st.success("Literature review appears here")
            
    elif "Research Articles" in tool:
        st.subheader("Research Article Search")
        query = st.text_input("Search query:")
        if st.button("Search"):
            st.success("Relevant articles appear here")
            
    elif "Target Labs" in tool:
        st.subheader("Target Lab Finder")
        area = st.text_input("Research area:")
        if st.button("Find Labs"):
            st.success("Matching labs appear here")

else:
    st.warning("⚠️ Running: SciColab (Development)")
    st.markdown("---")
    st.markdown("### Experimental Features")
    
    feature = st.selectbox("Select Feature", ["New Feature 1", "New Feature 2", "Beta Feature"])
    
    if feature:
        st.info(f"Working on: {feature}")
        user_input = st.text_area("Input:")
        if st.button("Run"):
            st.success("Output appears here")