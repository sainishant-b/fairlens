"""
Rule-based mitigation suggester. Maps disparity level + disadvantaged group
to plain-English remediation playbook entries. No external library needed --
plug Fairlearn / AIF360 here later if heavy mitigation algorithms are wanted.
"""


def suggest_mitigations(report: dict) -> list[dict]:
    bias_level = report.get("bias_level", "LOW")
    disadvantaged = report.get("disadvantaged_group", "unknown")

    if bias_level == "HIGH":
        return [
            {
                "name": "Reweighting",
                "summary": f"Up-weight {disadvantaged} samples during training so the model "
                           f"sees their qualifications with the same statistical force as the favored group.",
                "expected_disparity_reduction": "60-80%",
                "effort": "low",
            },
            {
                "name": "Equalized-odds constraint",
                "summary": "Retrain with Fairlearn ExponentiatedGradient under an equalized-odds "
                           "constraint. Forces equal true-positive and false-positive rates across groups.",
                "expected_disparity_reduction": "70-95%",
                "effort": "medium",
            },
            {
                "name": "Adversarial debiasing",
                "summary": "Train an adversary network to predict the protected attribute from the "
                           "main model's predictions; penalize the main model for leaking it.",
                "expected_disparity_reduction": "50-90%",
                "effort": "high",
            },
        ]

    if bias_level == "MEDIUM":
        return [
            {
                "name": "Counterfactual data augmentation",
                "summary": f"Synthesize additional training samples for {disadvantaged} until base "
                           f"rates match the favored group.",
                "expected_disparity_reduction": "40-70%",
                "effort": "low",
            },
            {
                "name": "Group-specific thresholds",
                "summary": "Calibrate decision thresholds per group post-hoc so positive prediction "
                           "rates match. Cheapest fix when retraining is off-limits.",
                "expected_disparity_reduction": "50-80%",
                "effort": "low",
            },
        ]

    return [
        {
            "name": "Continuous monitoring",
            "summary": "Disparity within acceptable band. Schedule monthly stress tests to catch drift.",
            "expected_disparity_reduction": "n/a",
            "effort": "low",
        },
    ]
