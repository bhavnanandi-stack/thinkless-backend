import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")


def generate_social_post(image_description, intent, platform):
    prompt = f"""
    You are ThinkLess AI.

    Generate:
    - 1 recommended post
    - 2 alternative captions

    Platform: {platform}
    User Intent: {intent}

    Image Context:
    {image_description}

    Return ONLY valid JSON in this format:

    {{
      "recommended": {{
        "caption": "",
        "hook": "",
        "cta": "",
        "hashtags": [],
        "reason": "",
        "target": ""
      }},
      "alternative_1": {{
        "caption": "",
        "reason": "",
        "target": ""
      }},
      "alternative_2": {{
        "caption": "",
        "reason": "",
        "target": ""
      }}
    }}
    """

    response = model.generate_content(prompt)

    return response.text