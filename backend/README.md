# Backend README

This backend provides core APIs for PlantCare AI.

To run locally:

1. Create a venv and install requirements:

   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt

2. Start the server:

   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

APIs:
- POST /api/auth/signup
- POST /api/auth/login
- POST /api/diagnose/image (multipart file)
- POST /api/diagnose/symptoms (form field `symptoms`)
- POST /api/chat (JSON {message: ...})
- GET /api/diseases

Models should be placed in backend/app/models/ as `cnn_model.pt` and `symptom_model.pkl`.
