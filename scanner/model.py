from __future__ import annotations
from joblib import dump, load
from sklearn.linear_model import LogisticRegression
from .features import build_features
import pandas as pd

class RiskClassifier:
    def __init__(self, model=None):# logistic regression is just a starter, could swap in RandomForest
        self.model = model or LogisticRegression(max_iter=1000)

    def fit(self, alerts_df: pd.DataFrame, labels):
        X = build_features(alerts_df)
        self.model.fit(X, labels)
        return self

    def predict(self, alerts_df: pd.DataFrame):
        X = build_features(alerts_df)
        return self.model.predict(X)

    def save(self, path: str):
        dump(self.model, path)

    @staticmethod
    def load(path: str) -> "RiskClassifier":
        return RiskClassifier(load(path))
