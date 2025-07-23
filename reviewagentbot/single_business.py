import openai
import os

def process_single_business(business_name: str) -> str:
    import openai

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Write a professional, kind, and engaging reply to a Google review for the business: '{business_name}'"}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return reply

    except Exception as e:
        return f"Error: {str(e)}"