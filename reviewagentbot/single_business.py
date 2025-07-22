import openai
import os

def process_single_business(business_name):
    try:
        prompt = f"""You are an AI assistant. Write a professional, kind, and engaging reply to a Google review for the business: "{business_name}". 
Make sure your reply sounds human, not robotic, and addresses customer concerns or compliments.
The tone should reflect excellent customer service and make the customer feel valued."""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You help businesses write replies to customer reviews."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250
        )

        reply = response['choices'][0]['message']['content'].strip()
        return reply

    except Exception as e:
        return f"Error: {str(e)}"
