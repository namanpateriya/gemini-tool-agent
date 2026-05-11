from app.tools.calculator import (
    CalculatorTool
)

from app.tools.memory import (
    MemoryTool
)

from app.tools.file_reader import (
    FileReaderTool
)

TOOLS = {
    "calculator": {
        "tool": CalculatorTool,
        "description": (
            CalculatorTool.description
        )
    },

    "memory": {
        "tool": MemoryTool,
        "description": (
            MemoryTool.description
        )
    },

    "file_reader": {
        "tool": FileReaderTool,
        "description": (
            FileReaderTool.description
        )
    }
}


def get_tool(tool_name: str):

    return TOOLS.get(tool_name)


def list_tools():

    return {
        name: meta["description"]
        for name, meta in TOOLS.items()
    }
