from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, diagnose, chat, diseases

app = FastAPI(title="PlantCare AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(diagnose.router, prefix="/api/diagnose", tags=["diagnose"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(diseases.router, prefix="/api/diseases", tags=["diseases"])

@app.get("/")
async def root():
    return {"message": "PlantCare AI backend"}
