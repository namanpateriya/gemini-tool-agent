import re

from app.utils.logger import get_logger

logger = get_logger(__name__)


class CalculatorTool:

    name = "calculator"

    description = (
        "Performs deterministic mathematical calculations."
    )

    @staticmethod
    def execute(expression: str):

        if not expression or not expression.strip():

            return {
                "success": False,
                "output": "empty expression"
            }

        try:

            expression = expression.lower().strip()

            # Handle percentage format
            percent_match = re.search(
                r"(\d+)%\s+of\s+(\d+)",
                expression
            )

            if percent_match:

                percent = float(
                    percent_match.group(1)
                )

                value = float(
                    percent_match.group(2)
                )

                result = (percent / 100) * value

                return {
                    "success": True,
                    "output": str(result)
                }

            # Safe math cleanup
            safe_expression = re.sub(
                r"[^0-9\.\+\-\*\/\(\) ]",
                "",
                expression
            )

            result = eval(
                safe_expression,
                {"__builtins__": {}},
                {}
            )

            return {
                "success": True,
                "output": str(result)
            }

        except Exception as e:

            logger.error(
                f"Calculator execution failed: {e}"
            )

            return {
                "success": False,
                "output": str(e)
            }
