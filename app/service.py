from app.orchestrator import (
    ToolOrchestrator
)

from app.utils.logger import (
    get_logger
)

logger = get_logger(__name__)

orchestrator = ToolOrchestrator()


class AgentService:

    @staticmethod
    def process_message(
        message: str
    ):

        logger.info(
            "Processing user message"
        )

        result = orchestrator.run(
            message
        )

        return result
