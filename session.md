# MindfulAI: Project Overview & Architecture

## Project Overview
MindfulAI is an empathetic, safe, and calming mental wellness companion application. The goal is to provide users with a mobile application that listens carefully and offers supportive, peaceful guidance. The project utilizes a fine-tuned, quantized large language model running on an efficient cloud server, paired with a modern React Native frontend.

**Github Repo:** [https://github.com/Viraj465/Gemma-4-Good](https://github.com/Viraj465/Gemma-4-Good)
**HF Model:** [Viraj0112/gemma4-finetuned-q4](https://huggingface.co/Viraj0112/gemma4-finetuned-q4)

## Architecture
The application is split into a mobile frontend and a serverless backend API:
- **Frontend (Mobile App):** Built with React Native and Expo. It handles user interactions, manages local chat state, and streams responses from the API.
- **Backend (API Server):** A FastAPI service running on Modal Cloud. It loads a quantized version of the LLM and streams generation results back to the client using Server-Sent Events (SSE).

## Model Stack
- **Base / Fine-tuned Model:** Gemma 4 (Quantized to Q4_K_M format).
- **Training/Quantization Stack:** `transformers`, `accelerate`, `bitsandbytes`, `unsloth`, `trl`, `datasets`.
- **Inference Engine:** `llama-cpp-python` (CPU-optimized wheel) which allows efficient CPU-based execution of the GGUF model format.
- **Serving:** FastAPI with `sse-starlette` for streaming outputs.

## Deployment Workflow
The backend is designed for serverless, cost-efficient deployment on Modal:
1. **Model Caching:** A one-time script (`modal run modal_app.py::download_model`) fetches the `gemma4_Q4_K_M.gguf` file from HuggingFace and stores it securely in a persistent Modal Volume (`mindfulai-model-cache`).
2. **Backend Deployment:** Using `modal deploy modal_app.py`, the FastAPI app is deployed into a serverless Modal container with Debian, Python 3.12, and the `llama-cpp-python` dependencies installed.
3. **Frontend:** The Expo/React Native app is built locally and can be tested using `expo start`, connecting seamlessly to the Modal API URL.

## Learnings
- **Efficient Inference:** Using GGUF and `llama-cpp-python` on CPU cores allowed for a significant cost reduction compared to maintaining a persistent GPU server. The 3.43 GB Q4 quantized model comfortably fits within an 8 GB RAM container.
- **Streaming UI:** Implementing SSE across a React Native environment provided a snappier, more engaging user experience by rendering text as it generates, avoiding long pauses.
- **Cold-Start Optimization:** By maintaining a warm container (`keep_warm=1`) or caching the model directly into a persistent volume, latency on the first request was heavily mitigated.

## Technical Decisions
- **Modal Cloud:** Chosen for the backend because it easily handles volume mounts (for the heavy GGUF model) and auto-scales with concurrent request handling, making it a perfect fit for a low-cost LLM API.
- **NativeWind & Expo:** Allowed rapid UI development for the mobile app using standard Tailwind CSS classes while benefiting from Expo's modern routing (`expo-router`).
- **Zustand:** Elected for frontend state management due to its minimal boilerplate and direct, robust store mechanics compared to Redux or Context API.
- **System Prompt Formatting:** A strict chat formatting scheme was enforced in the backend (`<start_of_turn>`, `<end_of_turn>`) alongside regex cleaning to ensure the model output remains safe, clean, and conversational without hallucinated markup.