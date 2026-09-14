import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI(title = "LLM Inference Orchestrator")

# Mock LLM streamer function to simulate asynchronous token streaming
async def mock_llm_streamer(prompt: str):
   dummy_response = f"Processiong prompt: '{prompt}'..."
   words = dummy_response.split() + [
      "Streaming", "tokens", "asynchronously", "from", "your", "FastAPI", "inference", "orchestrator!"
   ]

   for word in words:
      # Format as Server-Sent Event (SSE) message
      yield f"data: {word}\n\n"
      await asyncio.sleep(0.15)  # Simulates real-time LLM token output delay

@app.get("/api/v1/chat/stream")
async def stream_llm_response(prompt: str):
   return StreamingResponse(
      mock_llm_streamer(prompt),
      media_type="text/event-stream"
   )