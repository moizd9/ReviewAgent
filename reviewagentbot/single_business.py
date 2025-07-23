from openai import OpenAI

client = OpenAI()

def process_single_business(business_name):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"""You are an AI assistant. Write a professional, kind, and engaging reply to a Google review for the business: "{business_name}".
Make sure your reply sounds human, not robotic, and addresses customer concerns or compliments.
The tone should reflect excellent customer service and make the customer feel valued."""
                }
            ]
        )
        reply = response.choices[0].message.content.strip()
        return reply
    except Exception as e:
        return f"Error: {str(e)}"
