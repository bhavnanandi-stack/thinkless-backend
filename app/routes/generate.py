from fastapi import APIRouter, UploadFile, File, Form
from app.services.gemini_service import generate_social_post
import json

router = APIRouter()

@router.post("/generate")
async def generate_post(
    image: UploadFile = File(...),
    platform: str = Form(...),
    intent: str = Form(None)
):
    image_description = "User uploaded creator content image"

    ai_response = generate_social_post(
        image_description=image_description,
        intent=intent or "",
        platform=platform
    )

    try:
        parsed = json.loads(ai_response)
        return parsed
    except Exception:
        return {
            "recommended": {
                "caption": ai_response,
                "hook": "AI Generated",
                "cta": "Save this post",
                "hashtags": ["#thinkless"],
                "reason": "Fallback parser triggered",
                "target": "Engagement"
            },
            "alternative_1": {
                "caption": "Alternative caption unavailable.",
                "reason": "Fallback",
                "target": "Reach"
            },
            "alternative_2": {
                "caption": "Alternative caption unavailable.",
                "reason": "Fallback",
                "target": "Engagement"
            }
        }