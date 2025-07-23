from openai import OpenAI

client = OpenAI()

def process_single_business(business_name):
    if business_name.strip() == "":
        raise ValueError("Business name cannot be empty.")
    
    # 1. Use SerpAPI or other method to fetch Google reviews
    reviews = fetch_reviews_from_google_maps(business_name)  # You must define this

    if not reviews:
        raise ValueError("No reviews found.")

    # 2. Loop through each review and generate GPT reply
    data = []
    for review in reviews:
        prompt = f"Write a polite, thoughtful, and professional response to this customer review:\n\n{review['text']}"
        reply = call_gpt(prompt)  # You must define this
        data.append({
            "Rating": review["rating"],
            "Date": review["date"],
            "Review": review["text"],
            "AI Response": reply
        })

    # 3. Create dataframe
    df = pd.DataFrame(data)
    return df


