"""Эндпоинт контент-плана."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.core.config import Settings, get_settings
from app.services.crew import ContentPlan, build_plan

router = APIRouter()


class PlanRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=200)
    posts: int = Field(default=3, ge=1, le=20)
    tone: str = Field(default="friendly", max_length=32)


@router.post("/plan", response_model=ContentPlan)
async def plan(
    request: PlanRequest,
    settings: Settings = Depends(get_settings),
) -> ContentPlan:
    if request.posts > settings.max_posts:
        raise HTTPException(status_code=422, detail=f"posts must be <= {settings.max_posts}")
    try:
        return build_plan(request.topic, request.posts, request.tone, settings.brand_tag)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
