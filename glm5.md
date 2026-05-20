If you are not using Gradio, it means you want a pure **API endpoint** so you can connect your own custom frontend (React, Next.js, HTML, etc.) to the HF Space backend. 

Here is the best way to do this: **`llama-cpp-python` comes with a built-in OpenAI-compatible web server.** You don't even need to write a Python app file. You just deploy the server directly via Docker, and it gives you a standard `/v1/chat/completions` endpoint.

Here is exactly how to set it up on your 2 vCPU / 16GB RAM Space for maximum speed.

### Step 1: Create a Docker Space
1. Create a new Space on Hugging Face.
2. Select SDK: **Docker** 
3. Select Hardware: **Free** (2 vCPU / 16 GB RAM).
4. Upload your `model.gguf` file into the Space repository.

### Step 2: Create the `Dockerfile`
This Dockerfile compiles the server with **OpenBLAS** math optimizations (crucial for making 2 vCPU fast) and starts the OpenAI-compatible server.

```dockerfile
FROM python:3.10-slim

# Install OpenBLAS for CPU math acceleration (makes it ~2x faster)
RUN apt-get update && apt-get install -y --no-install-recommends libopenblas-dev && rm -rf /var/lib/apt/lists/*

# Install the llama-cpp-python server WITH CPU optimizations
RUN CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" \
    pip install --no-cache-dir 'llama-cpp-python[server]==0.2.90'

WORKDIR /app

# Copy your model into the container
COPY model.gguf .

# HF Spaces expect the app to run on port 7860
EXPOSE 7860

# Start the OpenAI-compatible API server with optimal 2vCPU settings
CMD ["python", "-m", "llama_cpp.server", \
     "--model", "/app/model.gguf", \
     "--host", "0.0.0.0", \
     "--port", "7860", \
     "--n_ctx", "2048", \
     "--n_threads", "2", \
     "--n_batch", "512", \
     "--mlock"]
```
*Note: `--n_threads 2` is strictly set to match your 2 vCPU. Setting it higher will actually slow it down.*

### Step 3: Add a `README.md`
You need this in your repository so Hugging Face knows it's a Docker Space.
```markdown
---
title: My Gemma API Server
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---
```

---

### Step 4: How to connect your external site to this API

Once your Space is deployed, it will get a URL like: `https://your-username-your-space-name.hf.space`

Hugging Face Spaces **automatically allow cross-origin requests (CORS)**, so your external website can talk to it directly without any CORS errors.

#### Example 1: Connecting via JavaScript (Fetch API)
You can call it exactly like you would call OpenAI's API:

```javascript
const apiUrl = "https://your-username-your-space-name.hf.space/v1/chat/completions";

async function getGemmaResponse(userMessage) {
    const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            model: "model.gguf", // the server just needs any string here
            messages: [
                { role: "system", content: "You are a helpful assistant." },
                { role: "user", content: userMessage }
            ],
            max_tokens: 256,
            temperature: 0.7,
            stop: ["<end_of_turn>", "<eos>"] // Crucial for Gemma!
        })
    });

    const data = await response.json();
    return data.choices[0].message.content;
}

// Usage
getGemmaResponse("What is the capital of France?").then(console.log);
```

#### Example 2: Connecting via Python (OpenAI Library)
Because it's an OpenAI-compatible server, you can just use the standard OpenAI Python library and change the `base_url`:

```python
from openai import OpenAI

# Point the client to your Hugging Face Space
client = OpenAI(
    base_url="https://your-username-your-space-name.hf.space/v1",
    api_key="not-needed" # HF Spaces are public, no API key needed
)

response = client.chat.completions.create(
    model="model.gguf",
    messages=[
        {"role": "user", "content": "Write a poem about the moon."}
    ],
    max_tokens=128,
    temperature=0.7,
    stop=["<end_of_turn>", "<eos>"] 
)

print(response.choices[0].message.content)
```

### Why this is the best approach for 2 vCPU:
1. **Zero overhead**: Gradio adds overhead. The built-in `llama_cpp.server` uses `uvicorn` which is extremely lightweight.
2. **Streaming Support**: If your frontend supports it, you can add `"stream": true` to your JSON body, and the server will return Server-Sent Events (SSE). This is **critical on CPU** because it allows your user to see words appearing one by one instead of waiting 15 seconds for the whole response to finish.
3. **Standardized**: You can swap out your custom model for GPT-4 or Claude later just by changing the `base_url` and `api_key` in your frontend.