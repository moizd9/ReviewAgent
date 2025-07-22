import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from reviewagentbot import process_single_business, process_csv

# Custom CSS
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #b5daff;
}

.big-title {
    font-size: 2.4em;
    font-weight: 800;
    margin-bottom: 0.2em;
}

.subtext {
    font-size: 1.1em;
    color: #ff2e63;
    margin-bottom: 1.2em;
}

.feature-list {
    font-size: 1.05em;
    line-height: 1.6;
}

.mode-label {
    font-weight: 600;
    margin-top: 1.5em;
    font-size: 1.1em;
}

input::placeholder {
    color: #888 !important;  /* light grey placeholder */
}

/* Red Primary Button Styling */
div.stButton > button:first-child {
    background-color: #f04b4b;
    color: white;
    font-weight: 600;
    border-radius: 5px;
    padding: 0.5em 1.5em;
    border: none;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

div.stButton > button:first-child:hover {
    background-color: #ff1c1c;
    color: white;
}

/* Footer */
footer {
    background-color: #fff6e6;
    padding: 1.5rem;
    margin-top: 4rem;
    border-top: 2px solid #ddd;
    font-size: 1em;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ========== UI Layout ==========

st.markdown("<div class='section'>", unsafe_allow_html=True)

# ---------- Hero Section ----------
st.markdown("""
<div class='big-title'>
    📝 ReviewAgent<br>
    AI Bulk Review Reply Generator
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='subtext'>
Handle Google reviews smartly. This AI agent helps you craft instant, thoughtful replies to your business reviews in bulk!
</div>

<div class='feature-list'>
✅ Personalized review replies using latest GPT-4o engine<br>
✅ Works with a single query or bulk upload via CSV<br>
✅ Saves hours of manual response effort<br>
✅ Ideal for marketers, agencies, and reputation teams<br>
</div>
""", unsafe_allow_html=True)

# ---------- Input Mode ----------
mode = st.radio("Choose input mode", ["Single Business", "Upload CSV"])

if mode == "Single Business":
    query = st.text_input("Enter Business Name (e.g., Starbucks Time Square NYC)", placeholder="write here...")
    if st.button("Generate Reply"):
        if query.strip():
            with st.spinner("Fetching and writing replies..."):
                df = process_single_business(query)
                st.success("Reply Generated ✅")
                st.write(df)
        else:
            st.warning("Please enter a business name.")
else:
    uploaded_file = st.file_uploader("Upload CSV with business names", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())

        if st.button("Generate Replies for All"):
            with st.spinner("Processing all businesses..."):
                response_df = process_csv(df)
                st.success("Replies Generated ✅")
                st.write(response_df)

                # Download CSV
                csv = response_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Replies CSV", csv, "ai_review_responses.csv", "text/csv")

# ========== Footer ==========
st.markdown("""
<hr style="border: 0.5px solid #ccc; margin-top: 3rem;" />
<div style="text-align: center; font-size: 14px; background-color: #fff6e6; padding: 1rem;">
    <strong>Developed by Moiz Deshmukh</strong> | 
    <a href="https://www.moizdeshmukh.com" target="_blank">www.moizdeshmukh.com</a><br>
    Curious how this AI Agent was built? <a href="https://link-to-blueprint" target="_blank">Read the full blueprint here</a>
</div>
""", unsafe_allow_html=True)
