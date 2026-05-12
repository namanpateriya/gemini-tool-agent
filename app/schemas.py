from pydantic import (
    BaseModel,
    Field
)

from typing import (
    List,
    Optional
)


class ChatRequest(BaseModel):

    message: str = Field(
        min_length=1,
        max_length=2000
    )


class ToolExecutionResult(BaseModel):

    tool: str
    success: bool
    output: str


class ChatResponse(BaseModel):

    status: str
    response: str

    confidence: float

    tools_used: List[str]

    tool_results: List[dict]


class ToolPlan(BaseModel):

    tool: str

    action: Optional[str] = None

    input: str
