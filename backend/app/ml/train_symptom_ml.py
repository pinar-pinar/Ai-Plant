import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import json


def train(kb_json, out_path="../models/symptom_model.pkl"):
    with open(kb_json) as f:
        data = json.load(f)
    texts = [d.get("symptoms_text", d.get("description", "")) for d in data]
    labels = [d["id"] for d in data]
    X_train, X_val, y_train, y_val = train_test_split(texts, labels, test_size=0.2, random_state=42)
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), max_features=5000)),
        ("clf", RandomForestClassifier(n_estimators=200, random_state=42))
    ])
    pipeline.fit(X_train, y_train)
    with open(out_path, "wb") as f:
        pickle.dump(pipeline, f)
    print("Symptom model saved to", out_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb_json", default="../kb/diseases.json")
    parser.add_argument("--out", default="../models/symptom_model.pkl")
    args = parser.parse_args()
    train(args.kb_json, args.out)
