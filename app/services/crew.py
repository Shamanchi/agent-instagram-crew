"""Контент-команда: рубрики, подписи, брифы, хэштеги. Без сети."""

from __future__ import annotations

import re

from pydantic import BaseModel

PILLARS = ["education", "behind-the-scenes", "engagement", "promo"]

PILLAR_HOOKS = {
    "education": "3 things about {topic} you should know",
    "behind-the-scenes": "How we make {topic}, step by step",
    "engagement": "Quick poll: {topic} — what is your pick?",
    "promo": "New in {topic}: try it this week",
}

PILLAR_CTA = {
    "education": "Save this post",
    "behind-the-scenes": "Follow for part 2",
    "engagement": "Vote in comments",
    "promo": "Link in bio",
}

PILLAR_VISUAL = {
    "education": "Carousel, 5 slides, bold headline overlay",
    "behind-the-scenes": "Reel, 30s, workshop footage",
    "engagement": "Single image, big question text",
    "promo": "Carousel, before/after, price sticker",
}

_WORD_RE = re.compile(r"[a-zA-Z]+")


class Post(BaseModel):
    pillar: str
    caption: str
    cta: str
    visual_brief: str
    hashtags: list[str]


class ContentPlan(BaseModel):
    topic: str
    tone: str
    posts: list[Post]


def build_hashtags(topic: str, brand_tag: str = "#dailybrew") -> list[str]:
    """Собрать хэштеги из слов темы + фирменный. Детерминировано."""
    tags = [f"#{word.lower()}" for word in _WORD_RE.findall(topic) if len(word) > 2]
    seen: list[str] = []
    for tag in tags + [brand_tag]:
        if tag not in seen:
            seen.append(tag)
    return seen[:6]


def build_caption(topic: str, pillar: str, tone: str) -> str:
    hook = PILLAR_HOOKS[pillar].format(topic=topic)
    return f"{hook} ({tone} tone)."


def build_plan(topic: str, posts: int = 3, tone: str = "friendly", brand_tag: str = "#dailybrew") -> ContentPlan:
    """Собрать контент-план. Детерминировано."""
    if not topic or not topic.strip():
        raise ValueError("topic must not be empty")
    if posts < 1:
        raise ValueError("posts must be >= 1")
    cleaned = topic.strip()
    hashtags = build_hashtags(cleaned, brand_tag)
    plan: list[Post] = []
    for i in range(posts):
        pillar = PILLARS[i % len(PILLARS)]
        plan.append(
            Post(
                pillar=pillar,
                caption=build_caption(cleaned, pillar, tone),
                cta=PILLAR_CTA[pillar],
                visual_brief=f"{PILLAR_VISUAL[pillar]} about {cleaned}",
                hashtags=list(hashtags),
            )
        )
    return ContentPlan(topic=cleaned, tone=tone, posts=plan)
