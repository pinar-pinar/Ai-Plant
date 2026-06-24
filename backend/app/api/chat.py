from fastapi import APIRouter
from fastapi import Body
from typing import Dict
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter()

KB_PATH = os.path.join(os.path.dirname(__file__), "..", "kb", "diseases.json")
KB_PATH = os.path.normpath(KB_PATH)

with open(KB_PATH) as f:
    KB = json.load(f)

DESCS = [d["description"] + " " + " ".join(d.get("symptoms", [])) for d in KB]
VECT = TfidfVectorizer(ngram_range=(1,2), max_features=2000)
VECT.fit(DESCS)
VECT_DESCS = VECT.transform(DESCS)

@router.post("/")
def chat(body: Dict = Body(...)):
    message = body.get("message", "")
    if not message:
        return {"response": "Je n'ai pas compris votre question."}
    vec = VECT.transform([message])
    sims = cosine_similarity(vec, VECT_DESCS)[0]
    best_idx = int(sims.argmax())
    best = KB[best_idx]
    resp = {
        "disease_id": best["id"],
        "disease_name": best["name"],
        "excerpt": best.get("description", ""),
        "confidence": float(sims.max())
    }
    return {"response": resp}
