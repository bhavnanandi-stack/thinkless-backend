from fastapi import APIRouter, UploadFile, File, Form
from app.services.gemini_service import generate_social_post

router = APIRouter()

@router.post("/generate")
async def generate_post(
    image: UploadFile = File(...),
    platform: str = Form(...),
    intent: str = Form(None)
):
    return {
        "recommended": {
            "caption": "ThinkLess generated caption",
            "hook": "Stop overthinking your content.",
            "cta": "Save this post.",
            "hashtags": ["#creator", "#content"],
            "reason": "High engagement structure",
            "target": "Engagement"
        },
        "alternative_1": {
            "caption": "Consistency beats perfection every time.",
            "reason": "Short motivational style optimized for shares.",
            "target": "Reach"
        },
        "alternative_2": {
            "caption": "Creators often overthink posting — just start.",
            "reason": "Relatable storytelling builds trust.",
            "target": "Engagement"
        }
    } 