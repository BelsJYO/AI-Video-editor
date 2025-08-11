from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from app.routes import chat, edit
from app.utils.config import BACKEND_PORT, FRONTEND_URL

app = FastAPI(title="AI Video Editor", version="1.0.0")

# CORS middleware for development and production
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
frontend_dist_path = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(frontend_dist_path):
    app.mount("/", StaticFiles(directory=frontend_dist_path, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(BACKEND_PORT))
