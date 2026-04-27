"""
Disparity metrics over counterfactual predictions.
Bias level thresholds chosen so demo data lands clearly in HIGH band.
"""

from typing import Any


def score_disparity(predictions: list[dict[str, Any]]) -> dict:
    """
    Compute per-group average score, max-min disparity, favored vs disadvantaged
    group, and a coarse bias level label.
    """
    groups: dict[str, list[float]] = {}
    for p in predictions:
        groups.setdefault(p["_group"], []).append(p["score"])

    avg_scores = {g: sum(v) / len(v) for g, v in groups.items()}
    max_score = max(avg_scores.values())
    min_score = min(avg_scores.values())
    disparity = max_score - min_score

    if disparity > 0.15:
        bias_level = "HIGH"
    elif disparity > 0.05:
        bias_level = "MEDIUM"
    else:
        bias_level = "LOW"

    return {
        "group_scores": {g: round(s, 3) for g, s in avg_scores.items()},
        "disparity": round(disparity, 3),
        "favored_group": max(avg_scores, key=avg_scores.get),
        "disadvantaged_group": min(avg_scores, key=avg_scores.get),
        "bias_level": bias_level,
    }
