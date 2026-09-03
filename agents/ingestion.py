import json
import logging


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"ok": True, "service": "commit-analysis-agent"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/render/logs")
async def render_logs(request: Request):
    payload = await request.json()
    print({"source": "render", "payload": payload}, flush=True)
    return JSONResponse({"ok": True})