import os
import re
import asyncio
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

# Load .env from backend root
load_dotenv()

# Verify required env var at startup
_HF_TOKEN = os.getenv("HF_TOKEN")
if not _HF_TOKEN:
    raise EnvironmentError("Missing required env var: HF_TOKEN. Add it to backend/.env")

# ── Generation config (ported from the torch/transformers script) ─────────────
GEN_CONFIG = {
    "max_tokens":     512,
    "temperature":    0.65,
    "top_p":          0.9,
    "repeat_penalty": 1.05,   # maps to repetition_penalty in transformers
    # no_repeat_ngram_size=3 has no direct llama-cpp equivalent — omitted
}

MAX_HISTORY_MESSAGES = 20   # trim after 20 turns (matches script's [-20:])


def _clean_response(text: str) -> str:
    """
    Apply the same post-processing as the original torch script:
      - strip bold/italic markers (**)
      - strip heading markers (##)
      - strip horizontal rules (--- / ——)
      - strip non-ASCII characters
    """
    text = re.sub(r'\*+', '', text)          # remove ** / *
    text = re.sub(r'#{1,3} ', '', text)      # remove ## headings
    text = re.sub(r'[-\u2014]{3,}', '', text)  # remove --- / ———
    text = re.sub(r'[^\x00-\x7F]', '', text)   # strip non-ASCII
    text = text.strip()
    return text if text else "I'm listening."


class LlamaService:
    def __init__(self):
        self.llm = None
        self.model_path = None
        self._history: list[dict] = []   # persisted across requests on this instance

    def load_model(self):
        """
        Downloads gemma4_Q4_K_M.gguf from the private HF repo (authenticated)
        and loads it into llama-cpp. On HF Spaces the model is already on HF
        infrastructure so the download is ~10-15 seconds (internal network).
        On subsequent requests within the same container it's already loaded.
        """
        repo_id  = os.getenv("MODEL_REPO_ID",  "Viraj0112/gemma4-finetuned-q4").strip()
        filename = os.getenv("MODEL_FILENAME",  "gemma4_Q4_K_M.gguf").strip()

        # Check local container cache first (avoids re-download within same run)
        local_cache = os.path.join("/app/model_cache", filename)
        if os.path.exists(local_cache):
            print(f"Model found in container cache: {local_cache}")
            self.model_path = local_cache
        else:
            print(f"Downloading '{filename}' from '{repo_id}' (HF internal network — fast) ...")
            self.model_path = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                token=_HF_TOKEN,
                local_dir="/app/model_cache",   # cache inside container
            )
            print(f"Model saved to: {self.model_path}")

        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=4096,
            n_threads=os.cpu_count() or 4,
            verbose=False,
        )
        print("Model loaded successfully!")

    def _format_prompt(self, messages: list[dict]) -> str:
        """
        Gemma instruction-tuned chat template:
          <start_of_turn>user\n{content}<end_of_turn>\n
          <start_of_turn>model\n{content}<end_of_turn>\n

        The system prompt is prepended to the first user turn (Gemma has no
        dedicated system role).
        """
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

        # Open the model response turn
        formatted += "<start_of_turn>model\n"
        return formatted

    async def generate_stream(self, messages: list, temperature: float | None = None, max_tokens: int | None = None):
        """
        Streams token-by-token response from the Gemma GGUF model.
        Applies GEN_CONFIG params from the original torch script.
        Lazily loads the model on first call.
        """
        if not self.llm:
            self.load_model()

        # Build message dicts compatible with _format_prompt
        raw_messages = [{"role": m.role, "content": m.content} for m in messages]

        # Trim history to MAX_HISTORY_MESSAGES (matches the script's [-20:] logic)
        if len(raw_messages) > MAX_HISTORY_MESSAGES:
            raw_messages = raw_messages[-MAX_HISTORY_MESSAGES:]

        prompt = self._format_prompt(raw_messages)

        # Allow per-request overrides; fall back to GEN_CONFIG defaults
        gen_params = {
            **GEN_CONFIG,
            "stop": ["<end_of_turn>", "<start_of_turn>"],
            "stream": True,
        }
        if temperature is not None:
            gen_params["temperature"] = temperature
        if max_tokens is not None:
            gen_params["max_tokens"] = max_tokens

        # Accumulate the full response so we can clean it before yielding
        full_response = ""
        for output in self.llm(prompt, **gen_params):
            chunk = output["choices"][0]["text"]
            if chunk:
                full_response += chunk
                # Yield raw chunks for live streaming feel
                yield chunk
                await asyncio.sleep(0.01)

        # NOTE: If you prefer cleaned output only (no markdown artefacts mid-stream),
        # swap to accumulate-then-clean mode instead:
        #   cleaned = _clean_response(full_response)
        #   for char in cleaned:
        #       yield char
        #       await asyncio.sleep(0.005)


llama_service = LlamaService()