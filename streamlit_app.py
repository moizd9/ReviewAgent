import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from reviewagentbot import process_single_business, process_csv

# ------------------- Session State for Quota -------------------
if "quota_used" not in st.session_state:
    st.session_state.quota_used = 0

MAX_QUOTA = 2  # Max allowed generations per session

# ------------------- CSS Styling -------------------
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background-color: #ffdfdb;
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
footer {
    background-color: #f6f6f6;
    padding: 1rem;
    margin-top: 4rem;
    border-top: 2px solid #ddd;
    font-size: 1em;
    text-align: center;
}
div.stButton > button:first-child {
    background-color: #f75d5d;
    color: white;
    font-weight: 600;
    border-radius: 5px;
    padding: 0.5em 1.5em;
}
div.stButton > button:first-child:hover {
    background-color: #ff1c1c;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ------------------- Title Section -------------------
st.markdown("<div class='big-title'>📝 ReviewAgent</div>", unsafe_allow_html=True)
st.markdown("<div class='big-title'>AI-Powered Review Reply Generator</div>", unsafe_allow_html=True)

# ------------------- Description -------------------
st.markdown("""
<div class="subtext">
Handle Google reviews smartly.<br>
This AI agent helps you craft instant, thoughtful replies to your business reviews in bulk!
</div>
<div class="feature-list">
✅ Personalized review replies using latest GPT-4o engine<br>
✅ Works with a single query or bulk upload via CSV<br>
✅ Saves hours of manual response effort<br>
✅ Ideal for marketers, agencies, and reputation teams
</div>
""", unsafe_allow_html=True)

# ------------------- Mode Selection -------------------
mode = st.radio("Choose input mode", ["Single Business", "Upload CSV"])

# ------------------- Single Business -------------------
if mode == "Single Business":
    query = st.text_input("Enter Business Name (e.g., Starbucks Allston)", placeholder="Write here...")

    if st.button("Generate Reply"):
        if st.session_state.quota_used >= MAX_QUOTA:
            st.error("⛔ You’ve reached the maximum usage limit for this session.")
        elif query.strip():
            with st.spinner("⏳ Generating replies..."):
                try:
                    df = process_single_business(query)
                    st.write(df)
                    st.success("✅ Reply Generated!")
                    st.session_state.quota_used += 1
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a business name.")

# ------------------- Upload CSV -------------------
elif mode == "Upload CSV":
    uploaded_file = st.file_uploader("Upload CSV with business names", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())

        if st.button("Generate Replies for All"):
            if st.session_state.quota_used >= MAX_QUOTA:
                st.error("⛔ You’ve reached the maximum usage limit for this session.")
            else:
                with st.spinner("⏳ Processing all businesses..."):
                    try:
                        response_df = process_csv(df)
                        st.write(response_df)
                        st.success("✅ Replies Generated!")
                        st.session_state.quota_used += 1

                        # Download CSV
                        csv = response_df.to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Download Replies CSV", csv, "ai_review_responses.csv", "text/csv")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# ------------------- Quota Tracker -------------------
st.markdown(f"<p style='text-align:center;font-size:13px;color:#555;'>Remaining Quota: {MAX_QUOTA - st.session_state.quota_used} / {MAX_QUOTA}</p>", unsafe_allow_html=True)

# ------------------- Footer -------------------
st.markdown("""
<hr style="border: 0.5px solid #ccc; margin-top: 3rem;"/>

<div style="text-align: center; font-size: 14px; background-color: #ffdfdb; padding: 1rem;">
    <strong>Developed by Moiz Deshmukh</strong> |
    <a href="https://www.moizdeshmukh.com" target="_blank">www.moizdeshmukh.com</a><br>
    Curious how this AI Agent was built?
    <a href="https://link-to-blueprint" target="_blank">Read the full blueprint here</a>
</div>
""", unsafe_allow_html=True)
