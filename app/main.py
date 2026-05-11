from fastapi import FastAPI

from app.schemas import (
    ChatRequest
)

from app.service import (
    AgentService
)

app = FastAPI(
    title="Gemini Tool Agent",
    description=(
        "Lightweight Gemini-powered "
        "AI tool agent"
    ),
    version="1.0.0"
)


@app.get("/")
def health():

    return {
        "status": "running",
        "provider": "Google Gemini"
    }


@app.post("/chat")
def chat(
    request: ChatRequest
):

    result = (
        AgentService.process_message(
            request.message
        )
    )

    return result
