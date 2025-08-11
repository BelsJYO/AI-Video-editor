import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.routes import chat, edit
from app.utils.config import BACKEND_PORT, FRONTEND_URL

# Detect environment (defaults to development)
ENV = os.getenv("ENV", "development")

# Set allowed origins
if ENV == "production":
    allowed_origins = [FRONTEND_URL]
else:
    allowed_origins = [
    "http://localhost:3000",
    "https://*.replit.dev",
    "https://probable-pancake-9v5r57qxr7xf6xp-3000.app.github.dev"
]
    # Detect GitHub Codespaces URL
    if "CODESPACE_NAME" in os.environ and "GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN" in os.environ:
        codespaces_url = f"https://{os.environ['CODESPACE_NAME']}-3000.{os.environ['GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN']}"
        allowed_origins.append(codespaces_url)

app = FastAPI(title="AI Video Editor", version="1.0.0")

# Apply CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
@app.get("/hello")
def hello_test():
    return {"message": "Hello from backend!", "status": "ok"}


# Serve frontend in production
frontend_dist_path = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(frontend_dist_path) and ENV == "production":
    app.mount("/", StaticFiles(directory=frontend_dist_path, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(BACKEND_PORT))
