from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import auth, stream

app = FastAPI(
    title="NeuralOps API",
    description="Backend for Autonomous Multi-Agent Intelligence Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(stream.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "NeuralOps API Engine Operational"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
