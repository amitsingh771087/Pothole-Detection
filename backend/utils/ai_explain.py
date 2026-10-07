"""
ai_explain.py
-------------
Generates a short, human-readable explanation of the road condition
based on the detection summary.

Two modes:
1. RULE_BASED (default, no API key / no internet needed) - perfect for
   a college submission where you can't rely on an external service
   being reachable during evaluation/demo.
2. LLM mode - if you set an ANTHROPIC_API_KEY environment variable,
   the app will call the Claude API to generate a richer, natural
   language explanation instead. This is optional.

Either way, the API response field is called "ai_explanation", so the
frontend never needs to know which mode produced it.
"""

import os

USE_LLM = bool(os.environ.get("ANTHROPIC_API_KEY"))


def _rule_based_explanation(summary: dict) -> str:
    total = summary.get("total", 0)
    severe = summary.get("Severe", 0)
    moderate = summary.get("Moderate", 0)
    minor = summary.get("Minor", 0)

    if total == 0:
        return ("No potholes were detected in this image. The road surface "
                "appears to be in good condition.")

    if severe > 0:
        risk = "HIGH RISK"
        advice = ("Immediate repair is recommended. Large/deep potholes can "
                  "cause tyre and suspension damage and are a safety hazard, "
                  "especially at night or in wet conditions.")
    elif moderate > 0:
        risk = "MODERATE RISK"
        advice = ("These potholes should be scheduled for repair soon before "
                  "they widen further due to traffic and rain.")
    else:
        risk = "LOW RISK"
        advice = ("These are minor surface defects. Routine monitoring is "
                  "sufficient for now.")

    return (
        f"Road Condition Report: {total} pothole(s) detected "
        f"({severe} severe, {moderate} moderate, {minor} minor). "
        f"Overall risk level: {risk}. {advice}"
    )


def _llm_explanation(summary: dict) -> str:
    """Optional: uses the Anthropic API to phrase the explanation naturally."""
    try:
        import anthropic
        client = anthropic.Anthropic()
        prompt = (
            "You are a civil-engineering assistant. Given this pothole "
            f"detection summary: {summary}, write a 2-3 sentence road "
            "condition report for a municipal maintenance dashboard. "
            "Mention the risk level and a repair recommendation."
        )
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception:
        # Fall back safely if the API/library isn't available at demo time
        return _rule_based_explanation(summary)


def generate_ai_explanation(summary: dict) -> str:
    if USE_LLM:
        return _llm_explanation(summary)
    return _rule_based_explanation(summary)
