# Hackathon Blueprint: FairLens — Adversarial Bias Stress Tester

> Canonical spec. Source of truth for scope decisions.

---

## 1. Problem Statement

AI systems now make life-altering decisions in hiring, lending, and healthcare. These models are typically audited using static metrics that measure *average* fairness — which masks discriminatory edge cases. A model can pass a fairness audit and still systematically reject qualified candidates based on a name, zip code, or gender marker.

Existing tools (IBM AIF360, Fairlearn, Google What-If Tool) require data science expertise, show numbers instead of stories, and do not generate adversarial examples. Organizations deploying AI have no easy way to *stress test* their models the way a bad actor would exploit them.

**FairLens** solves this by automatically generating adversarial test cases that expose hidden bias — turning an abstract fairness audit into a live, undeniable demonstration.

---

## 2. Solution Overview

FairLens is a web-based adversarial bias testing platform. Users upload a dataset or model, and the system:

1. **Generates counterfactual pairs** — identical records differing only in a protected attribute (name, gender, race-correlated zip code, age).
2. **Runs both through the model** — captures the decision difference.
3. **Scores and visualizes the bias** — a Bias Exposure Report with dramatic side-by-side comparisons.
4. **Suggests mitigations** — reweighting, fairness constraints, or data augmentation.

Demo moment: paste two identical resumes where only the name differs ("Michael Johnson" vs "Mohammed Al-Hassan") and watch the hiring model score them differently in real time.

---

## 3. Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite + TailwindCSS |
| Frontend Hosting | Appwrite Sites (free, CDN, Git auto-deploy) |
| Auth | Appwrite Auth |
| Database | Appwrite Database (audit history) |
| Backend | Python FastAPI — hosted on Render (free tier) |
| Bias Engine | IBM AIF360 + custom adversarial generator |
| ML Models (demo) | scikit-learn (pre-trained hiring, loan approval models) |
| Visualization | Recharts / D3 |
| AI Explanations | Gemini API |

**Why this split:** Appwrite Functions cannot run heavy Python ML libraries (scikit-learn, AIF360, pickle files). Render handles the ML compute; Appwrite handles everything else.

---

## 4. Repository Structure

```
fairlens/
├── README.md
├── CLAUDE.md
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── hiring_model.pkl
│   │   └── loan_model.pkl
│   ├── engine/
│   │   ├── adversarial.py
│   │   ├── bias_scorer.py
│   │   └── mitigation.py
│   └── data/
│       ├── hiring_dataset.csv
│       ├── loan_dataset.csv
│       └── generate_biased_models.py
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── StressTest.jsx
│   │   │   └── Report.jsx
│   │   ├── components/
│   │   │   ├── PairComparison.jsx
│   │   │   ├── BiasScore.jsx
│   │   │   └── MitigationCard.jsx
│   │   └── lib/
│   │       ├── appwrite.js
│   │       └── saveAudit.js
├── deploy/
│   ├── render.md
│   ├── appwrite.md
│   └── .env.example
└── docs/
    └── BLUEPRINT.md   (this file)
```

(`submission/` for deck + demo video added later.)

---

## 5. Build Reference — Code Snippets

### Backend

**`backend/engine/adversarial.py`**
```python
PROTECTED_SWAPS = {
    "name": {
        "male_white": ["Michael Johnson", "David Smith", "James Williams"],
        "male_black": ["DeShawn Williams", "Jamal Carter", "Marcus Brown"],
        "male_muslim": ["Mohammed Al-Hassan", "Ahmed Ibrahim", "Omar Khalid"],
        "female_white": ["Emily Johnson", "Sarah Davis", "Jennifer Smith"],
        "female_black": ["Keisha Williams", "Latoya Brown", "Shaniqua Davis"],
    },
    "zip_code": {
        "high_income": ["10001", "90210", "02101"],
        "low_income": ["60628", "90011", "77051"],
    }
}

def generate_pairs(record: dict, attribute: str) -> list[dict]:
    pairs = []
    swaps = PROTECTED_SWAPS.get(attribute, {})
    for group, values in swaps.items():
        variant = record.copy()
        variant[attribute] = values[0]
        variant["_group"] = group
        pairs.append(variant)
    return pairs
```

**`backend/engine/bias_scorer.py`**
```python
def score_disparity(predictions: list[dict]) -> dict:
    groups = {}
    for p in predictions:
        g = p["_group"]
        groups.setdefault(g, []).append(p["score"])

    avg_scores = {g: sum(v)/len(v) for g, v in groups.items()}
    max_score = max(avg_scores.values())
    min_score = min(avg_scores.values())

    return {
        "group_scores": avg_scores,
        "disparity": round(max_score - min_score, 3),
        "favored_group": max(avg_scores, key=avg_scores.get),
        "disadvantaged_group": min(avg_scores, key=avg_scores.get),
        "bias_level": "HIGH" if (max_score - min_score) > 0.15
                       else "MEDIUM" if (max_score - min_score) > 0.05
                       else "LOW",
    }
```

**`backend/main.py`**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from engine.adversarial import generate_pairs
from engine.bias_scorer import score_disparity
import pickle, pandas as pd

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.post("/stress-test")
async def stress_test(payload: dict):
    model_path = f"models/{payload['model']}_model.pkl"
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    pairs = generate_pairs(payload["record"], payload["attribute"])

    predictions = []
    for pair in pairs:
        features = pd.DataFrame([pair]).drop(columns=["_group", "name"], errors="ignore")
        score = float(model.predict_proba(features)[0][1])
        predictions.append({**pair, "score": score})

    return {
        "pairs": pairs,
        "predictions": predictions,
        "bias_report": score_disparity(predictions),
    }

@app.post("/explain-bias")
async def explain_bias(report: dict):
    import google.generativeai as genai, os
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    An AI bias audit found the following results:
    {report}

    Explain in 3 sentences what this means for real people affected by this system.
    Be direct and specific. No jargon.
    """
    response = model.generate_content(prompt)
    return {"explanation": response.text}
```

**`backend/requirements.txt`**
```
fastapi
uvicorn
scikit-learn
pandas
numpy
aif360
google-generativeai
python-multipart
```

**`backend/data/generate_biased_models.py`**
```python
"""
Intentionally train biased models on skewed historical data.
This is the POINT — we want to expose the bias, not hide it.
"""
import pandas as pd, numpy as np, pickle
from sklearn.ensemble import RandomForestClassifier

np.random.seed(42)
n = 1000

data = pd.DataFrame({
    "years_experience": np.random.randint(0, 15, n),
    "education_level": np.random.randint(1, 5, n),
    "num_skills": np.random.randint(1, 20, n),
    "gender_encoded": np.random.choice([0, 1], n),
    "name_origin": np.random.choice([0, 1, 2], n),
})

hire_prob = (
    0.3 * data["years_experience"] / 15 +
    0.3 * data["education_level"] / 4 +
    0.2 * data["num_skills"] / 20 +
    -0.1 * data["gender_encoded"] +
    -0.15 * (data["name_origin"] == 2)
)
data["hired"] = (hire_prob + np.random.normal(0, 0.1, n) > 0.4).astype(int)

X = data.drop("hired", axis=1)
y = data["hired"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

with open("models/hiring_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Biased hiring model saved.")
```

### Frontend

**`frontend/src/lib/appwrite.js`**
```javascript
import { Client, Account, Databases, ID } from "appwrite";

const client = new Client()
  .setEndpoint("https://cloud.appwrite.io/v1")
  .setProject(import.meta.env.VITE_APPWRITE_PROJECT_ID);

export const account = new Account(client);
export const databases = new Databases(client);
export { ID };

export const DB_ID = import.meta.env.VITE_APPWRITE_DB_ID;
export const COLLECTION_ID = "audit_results";
```

**`frontend/src/lib/saveAudit.js`**
```javascript
import { databases, ID, DB_ID, COLLECTION_ID } from "./appwrite";

export async function saveAuditResult(biasReport, modelName, attribute) {
  return await databases.createDocument(DB_ID, COLLECTION_ID, ID.unique(), {
    model: modelName,
    attribute,
    bias_level: biasReport.bias_level,
    disparity: biasReport.disparity,
    disadvantaged_group: biasReport.disadvantaged_group,
    timestamp: new Date().toISOString(),
  });
}
```

**`frontend/src/pages/StressTest.jsx`** and **`components/BiasScore.jsx` / `PairComparison.jsx`** — see original Phase-2 build instructions; implement when coding starts.

---

## 6. Submission Problem Statement (copy)

```
AI systems now make life-altering decisions in hiring, lending, and healthcare.
Existing fairness tools use static metrics that mask discriminatory edge cases —
a model can pass an audit and still systematically reject qualified candidates
based on a name or zip code. Organizations have no way to stress test their
models against adversarial inputs. FairLens fills this gap.
```

---

## 7. Project Deck — Slide Outline (6 slides)

1. **Hook** — "Same resume. Different name. Different fate." Two side-by-side apps, identical, one approved one rejected.
2. **Problem** — 250M+ AI hiring decisions/year US, audits measure averages, no adversarial standard.
3. **Solution** — Upload model → adversarial pairs → bias exposed → fix.
4. **Live Demo Screenshot** — `Bias: HIGH | Disparity: 23.4% | Disadvantaged: muslim_male`.
5. **Architecture** — User → Appwrite Sites (React) → Render (FastAPI + AIF360) → Gemini → Report → Appwrite DB.
6. **Impact** — Audit any AI in <5 min, no DS skill, Gemini explains plain-English.

---

## 8. Demo Video Script (2 min)

```
[0:00–0:15] HOOK
Two resumes side by side. "Meet Michael Johnson and Mohammed Al-Hassan.
Same degree, same experience, same skills. Let's see what this AI thinks."

[0:15–0:45] RUN TEST
Open FairLens. Hiring + Name. Run. Michael 71% APPROVED. Mohammed 48% REJECTED.
Big red HIGH BIAS badge.

[0:45–1:15] EXPLAIN
Click "Explain". Gemini: "Model 23% more likely to reject Muslim-sounding names
for identical qualifications. Hundreds of qualified candidates filtered before
human review."

[1:15–1:45] MITIGATION
Click "Suggest Fix". Reweighting recommendation. "Retraining with fairness
constraints reduces disparity from 23% to 3%."

[1:45–2:00] CLOSE
"FairLens turns a complex bias audit into a 60-second demo. Stress test
your AI before it impacts real people."
```

---

## 9. Build Checklist

- [ ] Generate biased hiring + loan models (`generate_biased_models.py`)
- [ ] Build FastAPI backend with `/stress-test` and `/explain-bias` endpoints
- [ ] Build React frontend with StressTest, BiasScore, PairComparison components
- [ ] Add `appwrite.js` and `saveAudit.js` lib files
- [ ] Create Appwrite project, database, `audit_results` collection
- [ ] Pre-load demo data so judges click without uploading
- [ ] Deploy backend to Render
- [ ] Deploy frontend to Appwrite Sites
- [ ] Set env vars in both dashboards
- [ ] Record demo video
- [ ] Build 6-slide deck
- [ ] Push public GitHub with clean README

---

## 10. Notes

- Intentionally biased models are the **feature**. Label them as demo models on biased historical data.
- Gemini key in `.env` only.
- Demo must work zero-upload — judges have no datasets. Pre-load everything.
- Bias reveal moment is the product. Don't bury in UI.
