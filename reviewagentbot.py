import json
import os
import pandas as pd
from serpapi import GoogleSearch
from openai import OpenAI
import streamlit as st

# Load API keys
import streamlit as st

SERPAPI_KEY = st.secrets["SERPAPI_API_KEY"]
OPENAI_KEY = st.secrets["OPENAI_API_KEY"]

# ✅ Set SerpAPI Key (this was missing)
GoogleSearch.SERP_API_KEY = SERPAPI_KEY

# Set OpenAI Client
client = OpenAI(api_key=OPENAI_KEY)



# --------------------------------------------------------------------
# 1) Lookup place_id from a business name using Google Maps via SerpAPI
# --------------------------------------------------------------------
def lookup_place_id(query: str) -> str:
    print(f"🔍 Searching for business: '{query}'...")

    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "hl": "en",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    print("🌐 Raw response from SerpAPI:")
    print(json.dumps(results, indent=2))  # helpful for debugging

    local_results = results.get("local_results", [])
    if not local_results:
        print("⚠️ No local results found.")
        return None

    # Try getting the first one, but fallback if needed
    first_result = local_results[0]
    pid = first_result.get("place_id")
    title = first_result.get("title", "Unknown")
    
    if not pid:
        print("❌ No place_id found in the first local result.")
        return None

    print(f"✅ Found place: {title} (place_id: {pid})")
    return pid


# --------------------------------------------------------------------
# 2) Fetch reviews using the resolved place_id
# --------------------------------------------------------------------
def fetch_reviews_by_place_id(place_id: str, num: int = 10):
    params = {
        "engine": "google_maps_reviews",
        "place_id": place_id,
        "hl": "en",
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    state = results.get("search_information", {}).get("reviews_results_state")
    print(f"🔍 reviews_results_state: {state}")

    all_reviews = results.get("reviews", [])
    reviews = all_reviews[:num]  # ✅ Limit based on slider input

    print(f"📦 Retrieved {len(reviews)} raw reviews.")
    return reviews


# --------------------------------------------------------------------
# 3) Generate an AI response to a review
# --------------------------------------------------------------------
def generate_response(review_text: str, rating=None):
    if not review_text.strip():
        return "(No review text provided.)"
    
    rating_line = f"The customer gave a rating of {rating}." if rating else ""
    
    prompt = f"""
You are a courteous reputation manager for a local business.
{rating_line}
Customer review:
\"\"\"{review_text}\"\"\"

Write a brief reply (2–3 sentences max) that:
- Thanks the reviewer by sentiment (no personal names unless present)
- Addresses any concern or praise
- Invites them back / next step
- Uses a warm, human tone and do not sound like a robot.
- End with Best Regards and the business' name for which you are the reputation manager.
"""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=180,
        temperature=0.5,
    )
    return resp.choices[0].message.content.strip()

# --------------------------------------------------------------------
# 4) Orchestrate: search → fetch reviews → respond → export to CSV
# --------------------------------------------------------------------
def run_agent(business_query: str, out_csv: str = "ai_review_responses.csv", max_reviews: int = 10):
    place_id = lookup_place_id(business_query)

    if not place_id:
        print("🧠 Tip: Try simplifying the business name, like just 'Starbucks Kenmore'")
        print(f"❌ Could not resolve business: '{business_query}'. Please try a more specific name.")
        return

    reviews = fetch_reviews_by_place_id(place_id, num=max_reviews)
    if not reviews:
        print("❌ No reviews returned from SerpAPI.")
        return

    rows = []
    for idx, r in enumerate(reviews, start=1):
        text = r.get("snippet", "") or r.get("text", "")
        rating = r.get("rating", "")
        date = r.get("date", "")

        print(f"🧠 Processing review {idx}/{len(reviews)}: {text[:60]}...")
        ai_reply = generate_response(text, rating=rating)

        rows.append({
            "Rating": rating,
            "Date": date,
            "Review": text,
            "AI Response": ai_reply
        })

    df = pd.DataFrame(rows)
    print("\n📊 Sample of results:")
    print(df.head())

    df.to_csv(out_csv, index=False)
    print(f"\n✅ Saved {len(df)} rows to '{out_csv}'")


# --------------------------------------------------------------------
# MAIN RUN
# --------------------------------------------------------------------
# if __name__ == "__main__":
#     run_agent("Starbucks Kenmore Boston MA", max_reviews=5)
