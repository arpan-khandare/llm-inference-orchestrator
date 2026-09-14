from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import ollama
from pydantic import BaseModel



app = FastAPI(title = "LLM Inference Orchestrator", description = "A simple FastAPI application to orchestrate LLM inference requests.", version = "1.0.0")

class PromptRequest(BaseModel):
   prompt: str
   
async def generate_token(prompt: str):
   response = ollama.generate(model = "llama3:8b", prompt = prompt, stream = True)
   for chunk in response:
      yield f"data: {chunk['response']}\n\n"

@app.post("/generate")
async def generate_endpoint(request: PromptRequest):
   return StreamingResponse(generate_token(request.prompt), media_type="text/event-stream")