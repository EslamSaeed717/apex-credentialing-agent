"""FastAPI dashboard for the Sovereign Credentialing Agent."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from pathlib import Path

app = FastAPI(title="Apex Credentialing Agent", version="1.0.0")
KB = Path(__file__).parent.parent / "knowledge_base"

@app.get("/")
def root():
    return {"status": "Sovereign Agent Active", "version": "1.0.0"}

@app.get("/credentials/owned")
def get_owned():
    p = KB / "certifications" / "owned.json"
    return json.loads(p.read_text()) if p.exists() else []

@app.get("/credentials/targets")
def get_targets():
    p = KB / "certifications" / "targets.json"
    return json.loads(p.read_text()) if p.exists() else []

@app.get("/identity")
def get_identity():
    p = KB / "master_resume.json"
    return json.loads(p.read_text()) if p.exists() else {}

@app.get("/health")
def health():
    return {"status": "healthy"}
