import json
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from app.schemas.chat import ChatRequest
from app.services.inference import llama_service

router = APIRouter()

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def event_generator():
        try:
            async for chunk in llama_service.generate_stream(
                messages=request.messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                # Yield in Server-Sent Events (SSE) format
                yield {
                    "event": "message",
                    "data": json.dumps({"chunk": chunk})
                }
            
            # Send done event
            yield {
                "event": "done",
                "data": json.dumps({"status": "completed"})
            }
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"detail": str(e)})
            }
            
    return EventSourceResponse(event_generator())