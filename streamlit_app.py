import streamlit as st
from reviewagentbot import run_agent

# Page config
st.set_page_config(page_title="ReviewAgent - AI Review Generator", page_icon="📝", layout="centered")

# Custom background color
st.markdown("""
    <style>
        .main {
            background-color: #add8e6; /* light blue */
        }
        .stSlider > div {
            color: black;
        }
        .stRadio > label > div {
            font-weight: 600;
        }
        .stTextInput > div > input {
            border: 2px solid #ff4b4b;
        }
        .stButton > button {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Header Title
st.markdown(
    "<h1 style='text-align: center;'>📝 ReviewAgent - AI-Powered Bulk<br>Review Reply Generator</h1>",
    unsafe_allow_html=True
)

# Subtitle
st.markdown(
    "<p style='color:#ff4b4b; text-align: center; font-size: 16px;'>"
    "Handle Google reviews smartly. This AI agent helps you craft instant, thoughtful replies to your business reviews in bulk!"
    "</p>",
    unsafe_allow_html=True
)

# Features with emojis
st.markdown("""
✅ Personalized review replies using latest GPT-4o engine  
✅ Works with a single query (no CSV needed)  
✅ Saves hours of manual response effort  
✅ Ideal for marketers, agencies, and reputation teams  
""")

# Business Input
st.markdown("**Enter Business Name (e.g., Starbucks Time Square NYC)**")
query = st.text_input("", placeholder="Type business name here...")

# Slider
max_reviews = st.slider("Number of reviews to fetch", 1, 25, 5)

# Generate Button
if st.button("Generate AI Responses"):
    if not query.strip():
        st.warning("Please enter a business name.")
    else:
        with st.spinner("🔄 Fetching and generating responses..."):
            run_agent(business_query=query, max_reviews=max_reviews)
        st.success("✅ Done! AI responses saved to `ai_review_responses.csv`")
        st.download_button("📄 Download CSV", open("ai_review_responses.csv", "rb"), file_name="ai_review_responses.csv")
