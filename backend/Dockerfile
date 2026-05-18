FROM python:3.12-slim

WORKDIR /app

# HF Spaces runs as a non-root user — pre-create cache dir with open perms
RUN mkdir -p /app/model_cache && chmod 777 /app/model_cache

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    fastapi>=0.104.1 \
    "uvicorn[standard]>=0.24.0" \
    sse-starlette>=1.8.2 \
    pydantic>=2.5.2 \
    huggingface-hub>=0.19.4 \
    python-dotenv>=1.0.0

# Build from source — latest version for Gemma 4 architecture support
RUN CMAKE_ARGS="-DGGML_NATIVE=OFF" pip install --no-cache-dir llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

COPY . .

# HF Spaces requires port 7860
EXPOSE 7860

# MODEL_REPO_ID, MODEL_FILENAME, HF_TOKEN come from Space Secrets
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]