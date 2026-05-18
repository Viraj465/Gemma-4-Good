from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as chat_router
from app.services.inference import llama_service

app = FastAPI(
    title="MindfulAI API",
    description="FastAPI backend for GGUF mental wellness chatbot",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the React Native app (or web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    import asyncio
    loop = asyncio.get_event_loop()
    # Load model in a thread so it doesn't block the event loop
    # The Space will show as "starting" until this completes (~30s on HF internal network)
    print("Startup: downloading and loading model...")
    await loop.run_in_executor(None, llama_service.load_model)
    print("Startup: model ready — accepting requests")

app.include_router(chat_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"status": "MindfulAI backend is running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": llama_service.llm is not None
    }