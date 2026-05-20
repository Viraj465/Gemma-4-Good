# MindfulAI

MindfulAI is a mobile mental wellness companion built with Expo and React Native. It gives users a calm chat interface where they can share how they are feeling and receive supportive, empathetic responses from a fine-tuned Gemma-family language model.

The app is split into a mobile frontend, a lightweight FastAPI backend, and a remote inference server. The backend is designed to run on Hugging Face Spaces and proxy chat requests to a Lightning AI API endpoint.

> MindfulAI is not a replacement for professional mental health care, diagnosis, emergency support, or crisis services.

## Features

- Calm React Native chat experience for emotional check-ins
- Streaming-style assistant responses over Server-Sent Events
- Local chat state managed with Zustand
- Markdown rendering for assistant messages
- FastAPI backend with CORS and health endpoints
- Remote model inference through a Lightning AI public API endpoint
- Hugging Face Spaces Docker deployment for the backend proxy

## Architecture

```text
Expo / React Native app
        |
        | POST /api/v1/chat/stream
        v
FastAPI backend on Hugging Face Spaces
        |
        | POST LIGHTNING_ENDPOINT_URL
        v
Lightning AI inference server
        |
        v
Fine-tuned Gemma GGUF model
```

## Tech Stack

**Mobile app**

- Expo
- React Native
- Expo Router
- NativeWind / Tailwind CSS
- Zustand
- react-native-markdown-display

**Backend**

- Python 3.12
- FastAPI
- sse-starlette
- httpx
- Pydantic
- Hugging Face Spaces Docker runtime

**Model and training artifacts**

- Fine-tuned Gemma model
- GGUF quantized model format
- Training/data tooling references: `transformers`, `accelerate`, `bitsandbytes`, `unsloth`, `trl`, `datasets`

## Repository Structure

```text
.
|-- MindfulAI/                 # Expo React Native mobile app
|   |-- app/                   # Expo Router screens
|   |-- components/            # Reusable UI components
|   |-- services/api.ts        # Backend streaming client
|   `-- store/useChatStore.ts  # Chat state
|-- backend/                   # FastAPI backend for HF Spaces
|   |-- app/api/routes.py      # Chat streaming route
|   |-- app/services/inference.py
|   |-- app/main.py
|   |-- Dockerfile
|   `-- requirements.txt
|-- data.json                  # Fine-tuning / conversation data artifact
|-- generate_data.py           # Data generation script
|-- info.txt                   # Training dependency notes
`-- LICENSE
```

## Prerequisites

- Node.js and npm
- Expo CLI through `npx expo`
- Python 3.12+
- A deployed Lightning AI inference endpoint
- A Hugging Face Space for the backend

## Mobile Setup

```bash
cd MindfulAI
npm install
npm run start
```

Then open the app in Expo Go, Android emulator, iOS simulator, or web depending on your environment.

The mobile app currently points to the deployed backend in:

```ts
MindfulAI/services/api.ts
```

Update `API_BASE` there if you deploy your own backend Space.

## Backend Setup

Create a Python environment and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Set the Lightning endpoint:

```bash
LIGHTNING_ENDPOINT_URL=https://your-lightning-api-url/predict
```

Run locally:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 7860
```

Health check:

```bash
curl http://localhost:7860/health
```

Expected shape:

```json
{
  "status": "healthy",
  "remote_endpoint_configured": true,
  "remote_endpoint_error": null
}
```

## Lightning AI Endpoint

The backend expects `LIGHTNING_ENDPOINT_URL` to be the public API endpoint for your Lightning server, not the Studio web UI URL.

Use:

```text
https://your-public-lightning-port-url/predict
```

Do not use:

```text
https://lightning.ai/.../web-ui?port=8000
```

If your Lightning server runs on port `8000`, expose port `8000` from Lightning API Builder, copy the generated public API URL, and append `/predict` if it is not already included.

## Hugging Face Spaces Deployment

The backend is Docker-ready. Deploy the `backend/` folder as a Hugging Face Docker Space.

Required Space variable/secret:

```env
LIGHTNING_ENDPOINT_URL=https://your-public-lightning-port-url/predict
```

The Space runs:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 7860
```

## API

### `GET /`

Returns a simple status payload.

### `GET /health`

Returns backend health and Lightning endpoint configuration state.

### `POST /api/v1/chat/stream`

Streams chat chunks as Server-Sent Events.

Request body:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "I am feeling really sad today."
    }
  ],
  "temperature": 0.7,
  "max_tokens": 128
}
```

SSE events:

```text
event: message
data: {"chunk":"I'm sorry you're feeling this way..."}

event: done
data: {"status":"completed"}
```

## Model Notes

The project uses a fine-tuned Gemma model intended for supportive mental wellness conversations. The quantized model reference in project notes is:

```text
Viraj0112/gemma4-finetuned-q4
```

The local files `data.json`, `generate_data.py`, `info.txt`, and `LLM.ipynb` relate to dataset creation, training, or experimentation.

## Safety Notes

MindfulAI should respond with calm, supportive language, but it should not be treated as clinical care. For users in danger, crisis, self-harm risk, or medical emergency, the app should direct them to local emergency services or trusted crisis support resources.

## License

This project is licensed under the terms in [LICENSE](LICENSE).
