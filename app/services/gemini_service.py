from anthropic import Anthropic
import os

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def generate_social_post(image_description, intent, platform):

    prompt = f"""
      You are ThinkLess AI.

      Generate Instagram content immediately.

      Do NOT ask questions.
      Do NOT explain anything.
      Do NOT add markdown.

      Use the following context:

      Intent: {intent or "General creator content"}

      Image Description: {image_description}

      Return ONLY valid JSON in this exact format:

      {{
        "recommended": {{
          "caption": "string",
          "hook": "string",
          "cta": "string",
          "hashtags": ["#tag1", "#tag2"],
          "reason": "string",
          "target": "string"
        }},
        "alternative_1": {{
          "caption": "string",
          "reason": "string",
          "target": "string"
        }},
        "alternative_2": {{
          "caption": "string",
          "reason": "string",
          "target": "string"
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