import pandas as pd

# quick hacky mapping, not super scientific but works for demo

RISK_MAP = {"High": 2, "Medium": 1, "Low": 0, "Informational": 0}
CONF_MAP = {"High": 2, "Medium": 1, "Low": 0}

KEYWORDS = {
    "XSS": ["xss", "cross-site"],
    "SQLi": ["sql", "injection"],
    "CSRF": ["csrf"],
}


def keyword_flags(series: pd.Series, kw_list):
    s = series.fillna("").str.lower()
    return s.apply(lambda x: int(any(k in x for k in kw_list)))


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    X = pd.DataFrame()
    X["risk_num"] = df["risk"].map(RISK_MAP).fillna(0)
    X["conf_num"] = df["confidence"].map(CONF_MAP).fillna(0)
    for name, kws in KEYWORDS.items():
        X[f"kw_{name}"] = keyword_flags(df.get("alert", pd.Series([""]*len(df))), kws)
    X["has_param"] = df["param"].notna().astype(int) if "param" in df else 0
    X["has_attack"] = df["attack"].notna().astype(int) if "attack" in df else 0
    return X

# TODO: later try hand-labeling instead of piggybacking on ZAP risk
def derive_labels(df: pd.DataFrame) -> pd.Series:
    # Simple heuristic label for training: High/Medium -> 2/1, else 0
    return df["risk"].map({"High": 2, "Medium": 1}).fillna(0).astype(int)
