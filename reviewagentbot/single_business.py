from openai import OpenAI

client = OpenAI()

def process_single_business(review_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant. Write a professional, human-like, and empathetic response to customer reviews."},
                {"role": "user", "content": f"""Review: {review_text}

Write a kind, respectful, and brand-appropriate reply. Avoid sounding robotic. End with a warm closing and sign off from the customer service team."""}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return reply
    except Exception as e:
        return f"Error: {str(e)}"


