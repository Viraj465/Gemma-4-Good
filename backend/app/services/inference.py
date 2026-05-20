import os
from urllib.parse import urlsplit

import httpx
from dotenv import load_dotenv

# Load .env from backend root
load_dotenv()


def _normalize_endpoint_url(endpoint_url: str | None) -> tuple[str | None, str | None]:
    if not endpoint_url:
        return None, "LIGHTNING_ENDPOINT_URL is not configured."

    endpoint_url = endpoint_url.strip().strip("\"'")
    if not endpoint_url:
        return None, "LIGHTNING_ENDPOINT_URL is empty."

    parsed = urlsplit(endpoint_url)

    if parsed.path.rstrip("/").endswith("/predict"):
        return endpoint_url, None

    if parsed.path.rstrip("/").endswith("/web-ui"):
        return None, (
            "LIGHTNING_ENDPOINT_URL is a Lightning Studio web UI URL. "
            "Use the public API URL for port 8000 and include /predict."
        )

    return endpoint_url.rstrip("/") + "/predict", None


def _extract_response_text(data) -> str:
    if isinstance(data, str):
        return data

    if not isinstance(data, dict):
        return ""

    for key in ("response", "output", "text", "generated_text"):
        value = data.get(key)
        if isinstance(value, str):
            return value
        if isinstance(value, dict):
            nested = _extract_response_text(value)
            if nested:
                return nested

    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            message = first.get("message")
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                return message["content"]
            if isinstance(first.get("text"), str):
                return first["text"]

    return ""


class LlamaService:
    def __init__(self):
        self.endpoint_url, self.config_error = _normalize_endpoint_url(os.getenv("LIGHTNING_ENDPOINT_URL"))
        if self.config_error:
            print(f"WARNING: {self.config_error}")

    def load_model(self):
        """
        Backward-compatible no-op for older startup code.
        In the Lightning setup, the model is loaded by the remote inference server.
        """
        print("LlamaService is configured for remote inference; skipping local model load.")

    async def generate_stream(self, messages: list, temperature: float | None = None, max_tokens: int | None = None):
        """
        Calls the Lightning AI LitServer endpoint.
        The current server.py implementation is non-streaming, 
        so we return the full response in one go while maintaining the stream interface.
        """
        if self.config_error:
            yield f"Error: {self.config_error}"
            return

        # Convert message objects to simple dicts for the JSON payload
        raw_messages = [{"role": m.role, "content": m.content} for m in messages]
        payload = {"messages": raw_messages}
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    self.endpoint_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                data = response.json()
                full_text = _extract_response_text(data)

                if full_text:
                    yield full_text
                else:
                    print(f"Lightning AI returned no text. Response JSON: {data}")
                    yield "I'm listening."

            except Exception as e:
                print(f"Error calling Lightning AI: {e}")
                yield f"Error: Could not connect to the inference server. {str(e)}"

llama_service = LlamaService()
