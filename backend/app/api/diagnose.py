from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from ..ml import infer_image, infer_symptom
import shutil
import os

router = APIRouter()

@router.post("/image")
async def diagnose_image(file: UploadFile = File(...)):
    tmp_dir = "/tmp/plantcare_uploads"
    os.makedirs(tmp_dir, exist_ok=True)
    file_path = os.path.join(tmp_dir, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    try:
        res = infer_image.infer(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content=res)

class SymptomsIn:
    def __init__(self, symptoms: str = Form(...)):
        self.symptoms = symptoms

@router.post("/symptoms")
async def diagnose_symptoms(symptoms: str = Form(...)):
    try:
        res = infer_symptom.infer(symptoms)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return JSONResponse(content=res)
