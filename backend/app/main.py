from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as chat_router
from app.services.inference import llama_service

app = FastAPI(
    title="MindfulAI API",
    description="FastAPI backend for GGUF mental wellness chatbot",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("Startup: LlamaService initialized (using remote inference)")

app.include_router(chat_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "MindfulAI backend is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "remote_endpoint_configured": llama_service.endpoint_url is not None,
        "remote_endpoint_error": llama_service.config_error
    }
