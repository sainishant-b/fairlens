"""
FairLens FastAPI server.

Endpoints:
    GET  /health           — liveness probe
    POST /stress-test      — run adversarial bias test on a record
    POST /explain-bias     — LLM plain-English explanation of a bias report

Run from backend/ directory:
    uvicorn main:app --reload
"""

import os
import pickle
from functools import lru_cache
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from engine.adversarial import PROTECTED_SWAPS, generate_pairs
from engine.bias_scorer import score_disparity
from engine.mitigation import suggest_mitigations

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(HERE, "models")

MODEL_FEATURES = [
    "years_experience",
    "education_level",
    "num_skills",
    "gender_encoded",
    "name_origin",
    "zip_tier",
]

app = FastAPI(title="FairLens", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # hackathon demo only — tighten before real deploy
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache(maxsize=4)
def load_model(name: str):
    path = os.path.join(MODELS_DIR, f"{name}_model.pkl")
    if not os.path.exists(path):
        raise HTTPException(
            status_code=500,
            detail=f"Model {name!r} not found. Run "
                   f"`python data/generate_biased_models.py` from backend/ first.",
        )
    with open(path, "rb") as f:
        return pickle.load(f)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "models_dir_exists": os.path.isdir(MODELS_DIR)}


@app.get("/attributes")
async def attributes() -> dict:
    return {"supported": list(PROTECTED_SWAPS.keys())}


@app.post("/stress-test")
async def stress_test(payload: dict[str, Any]) -> dict:
    """
    Body:
      {
        "record":    { ...numeric features... },
        "model":     "hiring" | "loan",
        "attribute": "name" | "zip_code"
      }
    """
    try:
        record = payload["record"]
        model_name = payload["model"]
        attribute = payload["attribute"]
    except KeyError as exc:
        raise HTTPException(status_code=400, detail=f"Missing field: {exc.args[0]}")

    model = load_model(model_name)
    pairs = generate_pairs(record, attribute)

    predictions: list[dict] = []
    for pair in pairs:
        feature_row = {f: pair.get(f, 0) for f in MODEL_FEATURES}
        score = float(model.predict_proba(pd.DataFrame([feature_row]))[0][1])
        predictions.append({**pair, "score": round(score, 4)})

    report = score_disparity(predictions)
    return {
        "pairs": pairs,
        "predictions": predictions,
        "bias_report": report,
        "mitigations": suggest_mitigations(report),
    }


@app.post("/explain-bias")
async def explain_bias(report: dict) -> dict:
    """LLM plain-English explanation of a bias_report dict (VoidAI / OpenAI-compatible)."""
    api_key = os.environ.get("VOIDAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="VOIDAI_API_KEY env var not set on backend.",
        )

    base_url = os.environ.get("VOIDAI_BASE_URL", "https://api.voidai.app/v1")
    model_name = os.environ.get("VOIDAI_MODEL", "gpt-5-mini")

    from openai import OpenAI

    client = OpenAI(api_key=api_key, base_url=base_url)
    prompt = (
        "An AI bias audit found the following results:\n"
        f"{report}\n\n"
        "Explain in 3 sentences what this means for real people affected by this system. "
        "Be direct and specific. No jargon."
    )
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"LLM call failed via {base_url} (model={model_name}): {type(exc).__name__}: {exc}",
        )
    return {"explanation": completion.choices[0].message.content}
