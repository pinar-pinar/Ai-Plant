import os
import pickle

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "symptom_model.pkl")

def infer(text):
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        pred = model.predict([text])[0]
        probs = None
        try:
            probs = model.predict_proba([text])[0].max()
        except Exception:
            probs = None
        return {"disease_id": int(pred), "confidence": float(probs) if probs is not None else None}
    else:
        # simple keyword-based demo
        txt = text.lower()
        if "tache" in txt or "spot" in txt:
            return {"disease_id": 1, "confidence": 0.6}
        if "mildiou" in txt or "mold" in txt:
            return {"disease_id": 2, "confidence": 0.7}
        return {"disease_id": 0, "confidence": 0.4}
