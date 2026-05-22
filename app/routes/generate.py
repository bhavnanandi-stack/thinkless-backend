from fastapi import APIRouter, UploadFile, File, Form
from app.services.gemini_service import generate_social_post
import json

router = APIRouter()
DEBUG_MODE = False

@router.post("/generate")
async def generate_post(
    images: list[UploadFile] = File(...),
    platform: str = Form(...),
    intent: str = Form(None)
    ):
    print("TOTAL IMAGES:", len(images))
    for image in images:
        print("IMAGE:", image.filename)
        image_payloads = []

    for image in images:
        image_bytes = await image.read()
        image_payloads.append({
            "bytes": image_bytes,
            "media_type": image.content_type
        })

    if DEBUG_MODE:
        return {
            "analysis": {
                "context": "Test office bag image",
                "style": "Professional lifestyle",
                "intent": "Motivation"
            },

            "recommended": {
                "caption": "New bag, fresh mindset, same goals. ✨",
                "hook": "Small upgrades matter.",
                "cta": "Keep growing every day.",
                "hashtags": ["#motivation", "#office", "#growth"],
                "reason": "Motivational office aesthetic",
                "target": "Engagement"
            },

            "alternative_1": {
                "caption": "Carrying ambition everywhere I go.",
                "reason": "Professional inspiration",
                "target": "Reach"
            },

            "alternative_2": {
                "caption": "Sometimes growth starts with small changes.",
                "reason": "Subtle motivation",
                "target": "Connection"
            }
        }
    
    try:
        ai_response = generate_social_post(
            image_payloads=image_payloads,
            intent=intent or "",
            platform=platform
        )

        try:
            cleaned_response = ai_response.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned_response)
            normalized_response = {
                "analysis": parsed.get("analysis", {}),

                "recommended": parsed.get("recommended", {}),

                "alternative_1": (
                    {
                        "caption": parsed["alternatives"][0].get("caption", ""),
                        "hashtags": parsed["alternatives"][0].get(
                            "hashtags", []
                        ),
                        "reason": parsed["alternatives"][0].get(
                            "reason", ""
                        ),
                        "target": parsed["alternatives"][0].get(
                            "target", ""
                        ),
                    }
                    if len(parsed.get("alternatives", [])) > 0
                    else {
                        "caption": "",
                        "hashtags": [],
                        "reason": "",
                        "target": "",
                    }
                ),

                "alternative_2": (
                    {
                        "caption": parsed["alternatives"][0].get("caption", ""),
                        "hashtags": parsed["alternatives"][0].get(
                            "hashtags", []
                        ),
                        "reason": parsed["alternatives"][0].get(
                            "reason", ""
                        ),
                        "target": parsed["alternatives"][0].get(
                            "target", ""
                        ),
                    }
                    if len(parsed.get("alternatives", [])) > 0
                    else {
                        "caption": "",
                        "hashtags": [],
                        "reason": "",
                        "target": "",
                    }
                ),
            }
            return normalized_response

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

    except Exception as e:
        print("GEMINI ERROR:", str(e))

        return {
            "recommended": {
                "caption": f"AI temporarily unavailable — {str(e)}",
                "hook": "Fallback mode",
                "cta": "Retry later",
                "hashtags": ["#fallback"],
                "reason": "Gemini exception caught",
                "target": "Debug"
            },
            "alternative_1": {
                "caption": "Fallback response",
                "reason": "Debug",
                "target": "Reach"
            },
            "alternative_2": {
                "caption": "Fallback response",
                "reason": "Debug",
                "target": "Engagement"
            }
        }