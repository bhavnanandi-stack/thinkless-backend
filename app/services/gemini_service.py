from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_social_post(image_description, intent, platform):
    prompt = f"""
    You are ThinkLess AI.

    Generate:
    - 1 recommended post
    - 2 alternatives

    Platform: {platform}
    User Intent: {intent}
    Image Context: {image_description}

    Return ONLY JSON.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text