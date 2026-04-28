"""
Train intentionally biased hiring + loan classifiers on skewed historical data.
The bias is the FEATURE — FairLens exists to expose it, not hide it.

Run from backend/ directory:
    python data/generate_biased_models.py

Outputs:
    models/hiring_model.pkl
    models/loan_model.pkl
    data/hiring_dataset.csv
    data/loan_dataset.csv
"""

import os
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

HERE = os.path.dirname(os.path.abspath(__file__))
BACKEND = os.path.dirname(HERE)
MODELS_DIR = os.path.join(BACKEND, "models")
DATA_DIR = os.path.join(BACKEND, "data")
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

np.random.seed(42)
N = 1000

FEATURES = [
    "years_experience",
    "education_level",
    "num_skills",
    "gender_encoded",
    "name_origin",
    "zip_tier",
]


def make_population(n: int = N) -> pd.DataFrame:
    return pd.DataFrame({
        "years_experience": np.random.randint(0, 15, n),
        "education_level": np.random.randint(1, 5, n),
        "num_skills": np.random.randint(1, 20, n),
        "gender_encoded": np.random.choice([0, 1], n),       # 0=male, 1=female
        "name_origin": np.random.choice([0, 1, 2], n),       # 0=western, 1=black, 2=muslim
        "zip_tier": np.random.choice([0, 1, 2], n),          # 0=low, 1=mid, 2=high income
    })


def train_hiring() -> None:
    df = make_population()
    hire_prob = (
        0.30 * df["years_experience"] / 15
        + 0.25 * df["education_level"] / 4
        + 0.20 * df["num_skills"] / 20
        - 0.10 * df["gender_encoded"]
        - 0.15 * (df["name_origin"] == 2).astype(int)
        - 0.05 * (df["zip_tier"] == 0).astype(int)
    )
    df["hired"] = (hire_prob + np.random.normal(0, 0.08, len(df)) > 0.4).astype(int)

    X = df[FEATURES]
    y = df["hired"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    with open(os.path.join(MODELS_DIR, "hiring_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    df.to_csv(os.path.join(DATA_DIR, "hiring_dataset.csv"), index=False)
    print(f"Biased hiring model saved. Approval rate: {y.mean():.1%}")


def train_loan() -> None:
    df = make_population()
    approve_prob = (
        0.35 * df["years_experience"] / 15
        + 0.25 * df["education_level"] / 4
        + 0.10 * df["num_skills"] / 20
        - 0.05 * df["gender_encoded"]
        - 0.12 * (df["name_origin"] == 1).astype(int)
        - 0.08 * (df["name_origin"] == 2).astype(int)
        - 0.20 * (df["zip_tier"] == 0).astype(int)
    )
    df["approved"] = (approve_prob + np.random.normal(0, 0.08, len(df)) > 0.4).astype(int)

    X = df[FEATURES]
    y = df["approved"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    with open(os.path.join(MODELS_DIR, "loan_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    df.to_csv(os.path.join(DATA_DIR, "loan_dataset.csv"), index=False)
    print(f"Biased loan model saved. Approval rate: {y.mean():.1%}")


def train_college() -> None:
    df = make_population()
    admit_prob = (
        0.10 * df["years_experience"] / 15
        + 0.45 * df["education_level"] / 4
        + 0.35 * df["num_skills"] / 20
        - 0.15 * df["gender_encoded"]
        - 0.25 * (df["name_origin"] == 1).astype(int)
        - 0.20 * (df["name_origin"] == 2).astype(int)
    )
    df["admitted"] = (admit_prob + np.random.normal(0, 0.08, len(df)) > 0.5).astype(int)

    X = df[FEATURES]
    y = df["admitted"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    with open(os.path.join(MODELS_DIR, "college_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    df.to_csv(os.path.join(DATA_DIR, "college_dataset.csv"), index=False)
    print(f"Biased college admissions model saved. Approval rate: {y.mean():.1%}")


def train_housing() -> None:
    df = make_population()
    approve_prob = (
        0.20 * df["years_experience"] / 15
        + 0.10 * df["education_level"] / 4
        + 0.10 * df["num_skills"] / 20
        - 0.50 * (df["zip_tier"] == 0).astype(int)
        - 0.25 * (df["zip_tier"] == 1).astype(int)
    )
    df["approved"] = (approve_prob + np.random.normal(0, 0.05, len(df)) > 0.3).astype(int)

    X = df[FEATURES]
    y = df["approved"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    with open(os.path.join(MODELS_DIR, "housing_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    df.to_csv(os.path.join(DATA_DIR, "housing_dataset.csv"), index=False)
    print(f"Biased housing model saved. Approval rate: {y.mean():.1%}")


def train_insurance() -> None:
    df = make_population()
    approve_prob = (
        0.30 * df["years_experience"] / 15
        + 0.30 * df["education_level"] / 4
        - 0.30 * df["gender_encoded"]
        - 0.10 * (df["zip_tier"] == 0).astype(int)
    )
    df["approved"] = (approve_prob + np.random.normal(0, 0.08, len(df)) > 0.5).astype(int)

    X = df[FEATURES]
    y = df["approved"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    with open(os.path.join(MODELS_DIR, "insurance_model.pkl"), "wb") as f:
        pickle.dump(model, f)
    df.to_csv(os.path.join(DATA_DIR, "insurance_dataset.csv"), index=False)
    print(f"Biased auto insurance model saved. Approval rate: {y.mean():.1%}")


if __name__ == "__main__":
    train_hiring()
    train_loan()
    train_college()
    train_housing()
    train_insurance()
