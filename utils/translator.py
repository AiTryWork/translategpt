import openai
import os

def translate_text(text, target_language):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if not openai.api_key:
        raise Exception("OpenAI API key missing.")

    print("🌍 Translating using OpenAI...")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a professional translator. Translate the following into {target_language}."
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response['choices'][0]['message']['content']
