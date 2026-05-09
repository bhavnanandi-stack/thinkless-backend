from anthropic import Anthropic
import os
import base64

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def generate_social_post(image_bytes, intent, platform):

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    prompt = f"""
    You are ThinkLess AI.

    Analyze the uploaded image carefully.

    Infer:
    - image context
    - content style
    - likely posting intent

    Then generate:
    - 1 recommended Instagram post
    - 2 alternatives

    Rules:
    - NEVER ask questions
    - ALWAYS return raw JSON
    - NEVER use markdown

    User Intent:
    {intent or "Infer automatically from image"}

    Return JSON only.
    """

    response = client.messages.create(
        #model="claude-sonnet-4-20250514",
        model="claude-haiku-4-5-20251001",
        max_tokens=700,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
    )

    return response.content[0].text