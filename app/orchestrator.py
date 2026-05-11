import json

from app.config import (
    MAX_TOOL_ITERATIONS
)

from app.tools.registry import (
    get_tool,
    list_tools
)

from app.utils.gemini_client import (
    GeminiClient
)

from app.utils.logger import (
    get_logger
)

logger = get_logger(__name__)

client = GeminiClient()


class ToolOrchestrator:

    def __init__(self):

        self.available_tools = list_tools()

    def build_tool_selection_prompt(
        self,
        user_message: str
    ):

        return f"""
You are an AI orchestration agent.

Your job is to decide whether tools are needed.

Available tools:
{json.dumps(self.available_tools, indent=2)}

Rules:
- Respond ONLY in valid JSON
- Do not include markdown
- Do not explain reasoning
- If no tools required, return empty tools array
- Use concise tool inputs

Output format:
{{
  "tools": [
    {{
      "tool": "tool_name",
      "action": "optional_action",
      "input": "tool_input"
    }}
  ]
}}

User message:
{user_message}
"""

    def parse_tool_plan(
        self,
        response
    ):

        if response["status"] != "success":

            return {
                "success": False,
                "tools": [],
                "error": response.get(
                    "message",
                    "tool planning failed"
                )
            }

        data = response.get("data", {})

        tools = data.get("tools", [])

        if not isinstance(tools, list):

            return {
                "success": False,
                "tools": [],
                "error": (
                    "tools must be a list"
                )
            }

        return {
            "success": True,
            "tools": tools
        }

    def execute_tool(
        self,
        tool_payload
    ):

        tool_name = tool_payload.get("tool")

        action = tool_payload.get(
            "action"
        )

        tool_input = tool_payload.get(
            "input"
        )

        logger.info(
            f"Executing tool: {tool_name}"
        )

        tool_meta = get_tool(tool_name)

        if not tool_meta:

            return {
                "tool": tool_name,
                "success": False,
                "output": (
                    "unknown tool"
                )
            }

        tool = tool_meta["tool"]

        try:

            # Calculator Tool
            if tool_name == "calculator":

                result = tool.execute(
                    tool_input
                )

            # Memory Tool
            elif tool_name == "memory":

                if action == "store":

                    result = tool.store(
                        tool_input
                    )

                else:

                    result = tool.retrieve(
                        tool_input
                    )

            # File Reader Tool
            elif tool_name == "file_reader":

                result = tool.execute(
                    tool_input
                )

            else:

                result = {
                    "success": False,
                    "output": (
                        "unsupported tool"
                    )
                }

            return {
                "tool": tool_name,
                "success": result.get(
                    "success",
                    False
                ),
                "output": result.get(
                    "output"
                )
            }

        except Exception as e:

            logger.error(
                f"Tool execution failed: {e}"
            )

            return {
                "tool": tool_name,
                "success": False,
                "output": str(e)
            }

    def generate_final_response(
        self,
        user_message,
        tool_results
    ):

        prompt = f"""
You are a conversational AI assistant.

User message:
{user_message}

Tool execution results:
{json.dumps(tool_results, indent=2)}

Generate a concise conversational response.
Use tool outputs where relevant.
"""

        return client.generate(prompt)

    def run(
        self,
        user_message: str
    ):

        if (
            not user_message
            or not user_message.strip()
        ):

            return {
                "status": "error",
                "response": (
                    "empty message"
                ),
                "tools_used": [],
                "tool_results": []
            }

        logger.info(
            "Starting orchestration"
        )

        planning_prompt = (
            self.build_tool_selection_prompt(
                user_message
            )
        )

        planning_response = (
            client.generate_json(
                planning_prompt
            )
        )

        parsed_plan = (
            self.parse_tool_plan(
                planning_response
            )
        )

        if not parsed_plan["success"]:

            return {
                "status": "error",
                "response": (
                    parsed_plan["error"]
                ),
                "tools_used": [],
                "tool_results": []
            }

        planned_tools = (
            parsed_plan["tools"]
        )

        # Prevent excessive loops
        planned_tools = planned_tools[
            :MAX_TOOL_ITERATIONS
        ]

        tool_results = []

        tools_used = []

        for tool_payload in planned_tools:

            result = self.execute_tool(
                tool_payload
            )

            tool_results.append(result)

            if result["success"]:

                tools_used.append(
                    result["tool"]
                )

        final_response = (
            self.generate_final_response(
                user_message,
                tool_results
            )
        )

        return {
            "status": "success",
            "response": final_response,
            "tools_used": tools_used,
            "tool_results": tool_results
        }
