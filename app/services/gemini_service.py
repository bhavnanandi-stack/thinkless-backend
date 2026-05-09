from anthropic import Anthropic
import os

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def generate_social_post(image_description, intent, platform):

    prompt = f"""
    You are ThinkLess AI.

    Generate:
    - 1 recommended social media post
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

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text