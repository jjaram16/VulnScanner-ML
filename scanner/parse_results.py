import pandas as pd

COLUMNS = [
    "risk", "confidence", "alert", "cweid", "wascid", "url", "param", "evidence", "attack",
]


def load_alerts_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Keep commonly useful fields if present
    keep = [c for c in COLUMNS if c in df.columns]
    return df[keep].copy()

