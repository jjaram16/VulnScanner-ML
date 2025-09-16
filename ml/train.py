import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from scanner.features import derive_labels
from scanner.model import RiskClassifier

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--alerts", required=True)
    p.add_argument("--model", default="./ml/model.pkl")
    args = p.parse_args()

    df = pd.read_csv(args.alerts)
    y = derive_labels(df)
# NOTE: stratify=y so it doesn't break if most are "low"
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, random_state=42, stratify=y)

    clf = RiskClassifier().fit(X_train, y_train)
    preds = clf.predict(X_test)

    acc = accuracy_score(y_test, preds)
    print(f"Accuracy: {acc:.3f}")
    print(classification_report(y_test, preds))

    clf.save(args.model)
    print(f"Saved model to {args.model}")
    # TODO: save accuracy somewhere for reports?

