import streamlit as st
import pandas as pd
from ReviewAgentBot import generate_response

st.set_page_config(page_title="ReviewAgent", layout="centered")

st.title("🤖 ReviewAgent - AI Review Reply Generator")
st.markdown("Handle Google reviews smartly. Choose mode below:")

# Mode selection
mode = st.radio("Choose input mode", ["Single Business", "Upload CSV"])

# Shared API check
if "OPENAI_API_KEY" not in st.secrets or "SERPAPI_API_KEY" not in st.secrets:
    st.error("API keys missing in Streamlit secrets!")
    st.stop()

if mode == "Single Business":
    # Single business input
    business_name = st.text_input("Enter Business Name (e.g., Keventers Dubai)")
    if st.button("Generate Reply"):
        if business_name:
            with st.spinner("Thinking..."):
                result = generate_response(business_name)
                st.success("✅ AI-generated reply:")
                st.write(result)
        else:
            st.warning("Please enter a business name.")

else:
    # CSV upload input
    uploaded_file = st.file_uploader("Upload CSV with 'Business Name' column", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if 'Business Name' not in df.columns:
            st.error("❌ CSV must contain a 'Business Name' column.")
        else:
            st.write("📋 Preview of uploaded data:")
            st.dataframe(df)

            if st.button("Generate Replies for All"):
                responses = []

                with st.spinner("Generating responses..."):
                    for name in df["Business Name"]:
                        try:
                            reply = generate_response(name)
                        except Exception as e:
                            reply = f"Error: {e}"
                        responses.append(reply)

                df["AI Response"] = responses
                st.success("✅ All responses generated!")
                st.dataframe(df)

                # Allow download
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Responses CSV",
                    data=csv,
                    file_name="ai_review_responses.csv",
                    mime="text/csv"
                )
