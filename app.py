import streamlit as st
from summarizermp import load_and_summarize_url

st.title("Document Summarizer")

url = st.text_input("Enter document to summarize:")

if st.button("Summarize"):
    if url:
        with st.spinner("Summarizing..."):
            summaries = load_and_summarize_url(url)
        
        st.subheader("Chain Summary")
        st.write(summaries["chain_summary"])
    else:
        st.warning("Please enter a Document.")
