from fastapi import APIRouter
import json
import os

router = APIRouter()
KB_PATH = os.path.join(os.path.dirname(__file__), "..", "kb", "diseases.json")
KB_PATH = os.path.normpath(KB_PATH)

with open(KB_PATH) as f:
    KB = json.load(f)

@router.get("/")
def list_diseases():
    return KB

@router.get("/{disease_id}")
def get_disease(disease_id: int):
    for d in KB:
        if d["id"] == disease_id:
            return d
    return {"error": "Not found"}
