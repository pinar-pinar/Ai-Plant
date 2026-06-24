#!/usr/bin/env bash
set -e
echo "Starting PlantCare AI locally..."
# Backend
if [ ! -d ".venv" ]; then
  python -m venv .venv
  source .venv/bin/activate
  pip install -r backend/requirements.txt
else
  source .venv/bin/activate
fi
# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
# Serve frontend static files
cd frontend
python -m http.server 3000 &

echo "Backend running on http://localhost:8000"
echo "Frontend served on http://localhost:3000"
