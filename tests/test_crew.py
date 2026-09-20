"""Unit-тесты команды: без сети, детерминированы."""

import pytest

from app.services.crew import build_caption, build_hashtags, build_plan


def test_hashtags() -> None:
    assert build_hashtags("morning coffee") == ["#morning", "#coffee", "#dailybrew"]
    assert build_hashtags("AI") == ["#dailybrew"]


def test_plan_pillars_cycle() -> None:
    plan = build_plan("morning coffee", posts=5, tone="friendly")
    assert [post.pillar for post in plan.posts] == [
        "education",
        "behind-the-scenes",
        "engagement",
        "promo",
        "education",
    ]
    first = plan.posts[0]
    assert first.cta == "Save this post"
    assert "morning coffee" in first.caption
    assert "Carousel" in first.visual_brief


def test_caption_tone() -> None:
    assert "(bold tone)" in build_caption("tea", "promo", "bold")


def test_bad_input_rejected() -> None:
    with pytest.raises(ValueError):
        build_plan("   ", posts=3)
    with pytest.raises(ValueError):
        build_plan("tea", posts=0)
