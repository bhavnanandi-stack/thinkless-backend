from anthropic import Anthropic
import os

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def generate_social_post(image_description, intent, platform):

    prompt = f"""
      Generate Instagram post content.

      Intent: {intent}
      Image: {image_description}

      Return valid JSON:
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
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text