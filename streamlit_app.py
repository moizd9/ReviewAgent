import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from .reviewagentbot import process_single_business, process_csv

# Inject custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #fff6e6;
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
        }
        .section {
            background-color: #fff9ed;
            padding: 2em;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# ========================= UI Layout =========================

st.markdown("<div class='section'>", unsafe_allow_html=True)

# Hero Section
st.markdown("<div class='big-title'>🤖 ReviewAgent - AI Review Reply Generator</div>", unsafe_allow_html=True)
st.markdown("""
<div class='subtext'>
Handle Google reviews smartly. This AI agent helps you craft instant, thoughtful replies to your business reviews.
</div>

<div class='feature-list'>
✅ Personalized review replies using latest GPT-4o engine<br>
✅ Works with a single query or bulk upload via CSV<br>
✅ Saves hours of manual response effort<br>
✅ Ideal for marketers, agencies, and reputation teams<br>
</div>
""", unsafe_allow_html=True)

# ========================= Dual Mode Input =========================

mode = st.radio("Choose input mode", ["Single Business", "Upload CSV"])

if mode == "Single Business":
    query = st.text_input("Enter Business Name (e.g., Keventers Dubai)")
    if st.button("Generate Reply"):
        if query.strip():
            with st.spinner("Fetching and writing replies..."):
                df = process_single_business(query)
                st.success("Reply Generated ✅")
                st.write(df)
        else:
            st.warning("Please enter a business name.")

elif mode == "Upload CSV":
    uploaded_file = st.file_uploader("Upload CSV with business names", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())

        if st.button("Generate Replies for All"):
            with st.spinner("Processing all businesses..."):
                response_df = process_csv(df)
                st.success("Replies Generated ✅")
                st.write(response_df)

                # Add download button
                csv = response_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Replies CSV", csv, "ai_review_responses.csv", "text/csv")

st.markdown("</div>", unsafe_allow_html=True)
