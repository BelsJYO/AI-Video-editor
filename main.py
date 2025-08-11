
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os
from typing import Optional

from app.routes import chat, edit
from app.utils.config import BACKEND_PORT, FRONTEND_URL

app = FastAPI(title="AI Video Editor", version="1.0.0")

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000", "https://*.replit.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api")
app.include_router(edit.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "AI Video Editor API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Mount static files for production (when frontend is built)
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(BACKEND_PORT))
