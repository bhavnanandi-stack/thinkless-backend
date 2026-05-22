from anthropic import Anthropic
import os
import base64
import time
from anthropic import APIStatusError

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
        - shared_context
        - content_style
        - emotional_tone
        - posting_intent
        - visual_consistency
        - carousel_narrative

        Then generate:
        - 1 recommended Instagram carousel caption
        - 2 alternative captions

        IMPORTANT:
        - Return ONLY valid raw JSON
        - Do NOT use markdown
        - Do NOT explain anything
        - Generate ONE unified caption for the full carousel
        - Keep each caption under 50 words
        - Keep hashtags to maximum 5
        - Keep hook under 10 words
        - Keep CTA under 10 words
        - Keep analysis concise

        Use EXACTLY this JSON structure:

        {{
        "analysis": {{
            "shared_context": "",
            "content_style": "",
            "emotional_tone": "",
            "posting_intent": "",
            "visual_consistency": "",
            "carousel_narrative": ""
        }},
        "recommended": {{
            "hook": "",
            "caption": "",
            "cta": "",
            "hashtags": ["", "", "", "", ""]
            "reason": "",
            "target": ""
        }},
        "alternatives": [
            {{
            "caption": "",
            "hashtags": ["", "", "", "", ""]
            "reason": "",
            "target": ""
            }},
            {{
            "caption": "",
            "hashtags": ["", "", "", "", ""]
            "reason": "",
            "target": ""
            }}
        ]
        }}

        User Intent:
        {intent or "Infer automatically from uploaded images"}

        Return JSON only.
    """
    content.append({
        "type": "text",
        "text": prompt
        })

    MODELS = [
    "claude-haiku-4-5-20251001",
    "claude-sonnet-4-20250514",
    ]
    MAX_RETRIES = 2

    last_error = None

    for model_name in MODELS:
        print(f"Trying model: {model_name}")

        for attempt in range(MAX_RETRIES):
            try:
                response = client.messages.create(
                    model=model_name,
                    max_tokens=700,
                    messages=[
                        {
                            "role": "user",
                            "content": content
                        }
                    ],
                )

                print(
                    f"Success using {model_name}"
                )

                return response.content[0].text

            except APIStatusError as e:
                last_error = e

                print(
                    f"{model_name} error: {e}"
                )

                # retry only overload
                if e.status_code == 529:
                    wait_time = 2 ** attempt

                    print(
                        f"Retrying in {wait_time}s..."
                    )

                    time.sleep(wait_time)
                    continue

                break

    raise Exception(
        f"Claude unavailable. Last error: {last_error}"
    )
  