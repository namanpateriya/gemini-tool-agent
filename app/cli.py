import argparse
import json

from app.service import (
    AgentService
)

parser = argparse.ArgumentParser(
    description="Gemini Tool Agent"
)

parser.add_argument(
    "--message",
    help="Message for the AI agent"
)

args = parser.parse_args()


def pretty_print(result):

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )


if args.message:

    result = (
        AgentService.process_message(
            args.message
        )
    )

    pretty_print(result)

else:

    parser.print_help()
