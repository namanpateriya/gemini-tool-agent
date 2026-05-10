from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    message: str


class ToolExecutionResult(BaseModel):
    tool: str
    success: bool
    output: str


class ChatResponse(BaseModel):
    status: str
    response: str
    tools_used: List[str]
    tool_results: List[dict]
