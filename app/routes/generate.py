from fastapi import APIRouter, UploadFile, File, Form

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
        }
    }