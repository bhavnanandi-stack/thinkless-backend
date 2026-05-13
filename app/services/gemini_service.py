from anthropic import Anthropic
import os
import base64

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def generate_social_post(image_payloads, intent, platform):

    content = []
    for image_data in image_payloads:
        base64_image = base64.b64encode(image_data["bytes"]).decode("utf-8")

        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": image_data["media_type"],
                "data": base64_image,
            },
        })

    prompt = f"""
        You are ThinkLess AI.

        Analyze ALL uploaded images together.

        Infer:
        - shared image context
        - content style
        - emotional tone
        - likely posting intent
        - visual consistency
        - possible carousel narrative

        Then generate:
        - 1 recommended Instagram carousel post
        - 2 alternatives

        Rules:
        - NEVER ask questions
        - ALWAYS return raw JSON
        - NEVER use markdown
        - Generate ONE unified caption for the full carousel
        - Return ONLY valid JSON

        User Intent:
        {intent or "Infer automatically from uploaded images"}

        Return JSON only.
        """
        content.append({
            "type": "text",
            "text": prompt
            })
    response = client.messages.create(
        #model="claude-sonnet-4-20250514",
        model="claude-haiku-4-5-20251001",
        max_tokens=700,
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
    )
  
    return response.content[0].text