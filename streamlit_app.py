import streamlit as st
from reviewagentbot import run_agent  # this is your main function

st.set_page_config(page_title="AI Review Generator", page_icon="🤖")

st.title("🧠 AI Review Generator")
st.markdown("Generate smart responses to Google Reviews using SerpAPI + OpenAI")

query = st.text_input("Enter a business name", "Starbucks Times Square")

max_reviews = st.slider("Number of reviews to fetch", 1, 25, 8)

if st.button("Generate AI Responses"):
    with st.spinner("Working on it..."):
        run_agent(business_query=query, max_reviews=max_reviews)
    st.success("✅ Done! Responses saved to `ai_review_responses.csv`")
    st.download_button("📥 Download CSV", open("ai_review_responses.csv", "rb"), file_name="ai_review_responses.csv")
