"""
Counterfactual pair generator. Given a base record + protected attribute,
returns variants that differ ONLY in that attribute's display value AND its
numeric encoding consumed by the model. Both must change together for the
prediction to actually move.
"""

from typing import Any

PROTECTED_SWAPS: dict[str, list[dict[str, Any]]] = {
    "name": [
        {"group": "male_white",   "name": "Michael Johnson",    "name_origin": 0, "gender_encoded": 0},
        {"group": "male_black",   "name": "DeShawn Williams",   "name_origin": 1, "gender_encoded": 0},
        {"group": "male_muslim",  "name": "Mohammed Al-Hassan", "name_origin": 2, "gender_encoded": 0},
        {"group": "female_white", "name": "Emily Johnson",      "name_origin": 0, "gender_encoded": 1},
        {"group": "female_black", "name": "Keisha Williams",    "name_origin": 1, "gender_encoded": 1},
    ],
    "zip_code": [
        {"group": "high_income", "zip_code": "10001", "zip_tier": 2},
        {"group": "mid_income",  "zip_code": "60601", "zip_tier": 1},
        {"group": "low_income",  "zip_code": "60628", "zip_tier": 0},
    ],
}


def generate_pairs(record: dict, attribute: str) -> list[dict]:
    """Return variants of `record` differing only in `attribute` (display + encoding)."""
    swaps = PROTECTED_SWAPS.get(attribute)
    if not swaps:
        raise ValueError(f"Unknown protected attribute: {attribute!r}. "
                         f"Supported: {list(PROTECTED_SWAPS)}")

    pairs = []
    for swap in swaps:
        variant = dict(record)
        for key, value in swap.items():
            if key == "group":
                variant["_group"] = value
            else:
                variant[key] = value
        pairs.append(variant)
    return pairs
