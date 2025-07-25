import streamlit as st
from reviewagentbot import run_agent

st.set_page_config(page_title="ReviewAgent - AI Review Generator", page_icon="📝", layout="centered")

# Inject custom styles
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], .main {
            background-color: #ffdbdb;
        }

        h1, h2, h3, p, div, .stTextInput, .stSlider {
            text-align: left !important;
        }

        .stTextInput > div > input {
            border: 2px solid #ff4b4b;
        }

        .stButton > button {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 0.5rem 1rem;
        }

        .footer {
            margin-top: 4rem;
            padding: 1.5rem;
            background-color: #ffdbdb;
            text-align: center;
            border-top: 1px solid #aaa;
            font-size: 14px;
        }

        .footer a {
            color: #0066cc;
            text-decoration: none;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)


# Header layout (split line with less spacing)
st.markdown("""
    <div style='margin-bottom: -10px'>
        <h2>📝 ReviewAgent</h2>
    </div>
    <h2>AI-Powered Bulk Review Reply Generator</h2>
""", unsafe_allow_html=True)

# Subtitle split into 2 lines
st.markdown(
    """
    <p style='color:#ff4b4b; font-size: 16px;'>
        Handle Google reviews smartly.<br>
        This AI agent helps you craft instant, thoughtful replies to your business reviews in bulk!
    </p>
    """,
    unsafe_allow_html=True
)

# Features list
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

# Footer
st.markdown("""
<div style="background-color: #ffdbdb; padding-top: 2rem; padding-bottom: 2rem;">
    <div style="max-width: 700px; margin: 0 auto; text-align: center;">
        <hr style="border: 0.5px solid #aaa; margin-bottom: 1rem;" />
        <p style="margin: 0;">
            Developed by <strong>Moiz Deshmukh</strong> |
            <a href="https://www.moizdeshmukh.com" target="_blank">www.moizdeshmukh.com</a>
        </p>
        <p style="margin-top: 0.5rem;">
            Curious how this AI Agent was built?
            <a href="https://www.moizdeshmukh.com/post/reviewagent-my-ai-powered-review-reply-assistant-for-local-businesses" target="_blank">Read the full blueprint here</a>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)



