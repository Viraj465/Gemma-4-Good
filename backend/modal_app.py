"""
MindfulAI — Modal Cloud Deployment
────────────────────────────────────
Deploy:   modal deploy modal_app.py
Serve:    modal serve modal_app.py   (hot-reload, temporary URL)

The GGUF model is downloaded ONCE into a Modal Volume and reused on every
subsequent request — no re-download ever again.
"""

import os
import re
import asyncio
import json
import modal

# ── Persistent volume — model lives here forever ──────────────────────────────
volume = modal.Volume.from_name("mindfulai-model-cache", create_if_missing=True)
MODEL_DIR = "/model_cache"

# ── Modal image — same deps as local backend ──────────────────────────────────
image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "sse-starlette>=1.8.2",
        "pydantic>=2.5.2",
        "huggingface-hub>=0.19.4",
        # Pre-built CPU wheel — no compiler needed
        extra_options="--extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu",
    )
    .pip_install(
        "llama-cpp-python==0.3.22",
        extra_options=(
            "--only-binary=llama-cpp-python "
            "--extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu"
        ),
    )
)

app = modal.App("mindfulai-backend", image=image)

# ── Generation config (same as local inference.py) ────────────────────────────
GEN_CONFIG = {
    "max_tokens":     128,
    "temperature":    0.65,
    "top_p":          0.9,
    "repeat_penalty": 1.05,
}
MAX_HISTORY = 20


def _clean_response(text: str) -> str:
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'#{1,3} ', '', text)
    text = re.sub(r'[-\u2014]{3,}', '', text)
    text = re.sub(r'[^\x00-\x7F]', '', text)
    text = text.strip()
    return text if text else "I'm listening."


def _format_prompt(messages: list[dict]) -> str:
    system_prompt = (
        "You are MindfulAI, an empathetic, safe, and calming mental wellness "
        "companion. You listen carefully and provide supportive, peaceful "
        "guidance. Keep responses concise and warm."
    )
    formatted = ""
    first_user = True
    for msg in messages:
        if msg["role"] == "user":
            content = msg["content"]
            if first_user:
                content = f"{system_prompt}\n\n{content}"
                first_user = False
            formatted += f"<start_of_turn>user\n{content}<end_of_turn>\n"
        elif msg["role"] == "assistant":
            formatted += f"<start_of_turn>model\n{msg['content']}<end_of_turn>\n"
    formatted += "<start_of_turn>model\n"
    return formatted


# ── FastAPI app ───────────────────────────────────────────────────────────────
def build_fastapi_app():
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse
    from pydantic import BaseModel
    from typing import Optional
    from llama_cpp import Llama

    fastapi_app = FastAPI(title="MindfulAI API")
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Model is loaded once per container (warm instance)
    _llm: Llama | None = None

    def get_llm() -> Llama:
        nonlocal _llm
        if _llm is None:
            model_path = os.path.join(MODEL_DIR, "gemma4_Q4_K_M.gguf")
            print(f"Loading model from {model_path} ...")
            _llm = Llama(
                model_path=model_path,
                n_ctx=4096,
                n_threads=os.cpu_count() or 4,
                verbose=False,
            )
            print("Model loaded!")
        return _llm

    class Message(BaseModel):
        role: str
        content: str

    class ChatRequest(BaseModel):
        messages: list[Message]
        temperature: Optional[float] = None
        max_tokens: Optional[int] = None

    @fastapi_app.get("/health")
    def health():
        return {"status": "healthy"}

    @fastapi_app.post("/api/v1/chat/stream")
    async def chat_stream(request: ChatRequest):
        """SSE streaming endpoint — same contract as local backend."""

        async def event_generator():
            try:
                llm = get_llm()
                raw = [{"role": m.role, "content": m.content} for m in request.messages]
                if len(raw) > MAX_HISTORY:
                    raw = raw[-MAX_HISTORY:]

                prompt = _format_prompt(raw)
                gen_params = {
                    **GEN_CONFIG,
                    "stop": ["<end_of_turn>", "<start_of_turn>"],
                    "stream": True,
                }
                if request.temperature is not None:
                    gen_params["temperature"] = request.temperature
                if request.max_tokens is not None:
                    gen_params["max_tokens"] = request.max_tokens

                for output in llm(prompt, **gen_params):
                    chunk = output["choices"][0]["text"]
                    if chunk:
                        yield f"event: message\ndata: {json.dumps({'chunk': chunk})}\n\n"
                        await asyncio.sleep(0.01)

                yield f"event: done\ndata: {json.dumps({'status': 'completed'})}\n\n"

            except Exception as e:
                yield f"event: error\ndata: {json.dumps({'detail': str(e)})}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    return fastapi_app


# ── Modal endpoint ─────────────────────────────────────────────────────────────
@app.function(
    volumes={MODEL_DIR: volume},
    secrets=[modal.Secret.from_name("mindfulai-hf-token")],  # HF_TOKEN stored as Modal secret
    cpu=4,
    memory=8192,   # 8 GB RAM — comfortable for 3.43 GB Q4 model
    timeout=300,   # 5 min max per request (model load + inference)
    # Keep 1 container warm so there's no cold-start delay for the first user
    # Remove this line if you want full scale-to-zero (saves credits when idle)
    # keep_warm=1,
)
@modal.concurrent(max_inputs=4)
@modal.asgi_app()
def fastapi_app():
    return build_fastapi_app()


# ── One-time model download function ─────────────────────────────────────────
@app.function(
    volumes={MODEL_DIR: volume},
    secrets=[modal.Secret.from_name("mindfulai-hf-token")],
    cpu=2,
    memory=4096,
    timeout=7200,   # 2 hours — enough for 3.43 GB download
)
def download_model():
    """
    Run once:  modal run modal_app.py::download_model
    Downloads the GGUF to the Modal Volume. Never needs to run again.
    """
    from huggingface_hub import hf_hub_download
    import shutil

    hf_token = os.environ["HF_TOKEN"]
    dest = os.path.join(MODEL_DIR, "gemma4_Q4_K_M.gguf")

    if os.path.exists(dest):
        size_gb = os.path.getsize(dest) / 1e9
        print(f"Model already cached ({size_gb:.2f} GB). Nothing to do.")
        return

    print("Downloading gemma4_Q4_K_M.gguf from HuggingFace ...")
    path = hf_hub_download(
        repo_id="Viraj0112/gemma4-finetuned-q4",
        filename="gemma4_Q4_K_M.gguf",
        token=hf_token,
        cache_dir="/tmp/hf_cache",
    )
    shutil.copy(path, dest)
    volume.commit()   # persist to volume
    print(f"Done! Model saved to {dest}")
