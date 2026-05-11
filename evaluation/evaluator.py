import json
import os
import time
from collections import defaultdict

from app.service import AgentService
from app.tools.memory import MemoryTool

BASE_DIR = os.path.dirname(__file__)

TEST_FILE = os.path.join(
    BASE_DIR,
    "test_cases.json"
)


class EvaluationMetrics:

    def __init__(self):

        self.total_cases = 0
        self.passed_cases = 0

        self.tool_selection_pass = 0
        self.keyword_match_pass = 0
        self.response_generation_pass = 0

        self.category_metrics = defaultdict(
            lambda: {
                "total": 0,
                "passed": 0
            }
        )

    def summary(self):

        overall_accuracy = (
            self.passed_cases
            / self.total_cases
        ) * 100 if self.total_cases else 0

        tool_accuracy = (
            self.tool_selection_pass
            / self.total_cases
        ) * 100 if self.total_cases else 0

        keyword_accuracy = (
            self.keyword_match_pass
            / self.total_cases
        ) * 100 if self.total_cases else 0

        response_accuracy = (
            self.response_generation_pass
            / self.total_cases
        ) * 100 if self.total_cases else 0

        return {
            "total_cases": self.total_cases,
            "passed_cases": self.passed_cases,
            "overall_accuracy": round(
                overall_accuracy,
                2
            ),
            "tool_accuracy": round(
                tool_accuracy,
                2
            ),
            "keyword_accuracy": round(
                keyword_accuracy,
                2
            ),
            "response_accuracy": round(
                response_accuracy,
                2
            ),
            "category_breakdown": dict(
                self.category_metrics
            )
        }


def load_test_cases():

    with open(
        TEST_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def setup_memory(case):

    MemoryTool.clear()

    memories = case.get(
        "setup_memory",
        []
    )

    for memory in memories:

        MemoryTool.store(memory)


def validate_tool_selection(
    expected_tools,
    actual_tools
):

    expected_set = set(
        expected_tools
    )

    actual_set = set(
        actual_tools
    )

    return expected_set == actual_set


def validate_keywords(
    expected_keywords,
    response
):

    response = (
        response.lower()
        if response else ""
    )

    for keyword in expected_keywords:

        if keyword.lower() not in response:

            return False

    return True


def validate_response_exists(
    response
):

    if not response:
        return False

    if response.startswith(
        "error:"
    ):
        return False

    return len(response.strip()) > 3


def evaluate_case(case):

    setup_memory(case)

    start_time = time.time()

    result = AgentService.process_message(
        case["message"]
    )

    latency = round(
        time.time() - start_time,
        2
    )

    actual_tools = result.get(
        "tools_used",
        []
    )

    response = result.get(
        "response",
        ""
    )

    tool_selection_pass = (
        validate_tool_selection(
            case["expected_tools"],
            actual_tools
        )
    )

    keyword_pass = (
        validate_keywords(
            case["expected_keywords"],
            response
        )
    )

    response_pass = (
        validate_response_exists(
            response
        )
    )

    overall_pass = (
        tool_selection_pass
        and keyword_pass
        and response_pass
    )

    return {
        "id": case["id"],
        "category": case["category"],
        "message": case["message"],
        "passed": overall_pass,
        "latency_seconds": latency,
        "tool_selection_pass": (
            tool_selection_pass
        ),
        "keyword_pass": keyword_pass,
        "response_pass": response_pass,
        "expected_tools": (
            case["expected_tools"]
        ),
        "actual_tools": actual_tools,
        "response": response
    }


def run_evaluation():

    cases = load_test_cases()

    metrics = EvaluationMetrics()

    detailed_results = []

    print(
        "\n============================"
    )
    print(
        " GEMINI TOOL AGENT EVALUATION "
    )
    print(
        "============================\n"
    )

    for case in cases:

        metrics.total_cases += 1

        category = case["category"]

        metrics.category_metrics[
            category
        ]["total"] += 1

        result = evaluate_case(case)

        detailed_results.append(result)

        if result["passed"]:

            metrics.passed_cases += 1

            metrics.category_metrics[
                category
            ]["passed"] += 1

        if result[
            "tool_selection_pass"
        ]:
            metrics.tool_selection_pass += 1

        if result[
            "keyword_pass"
        ]:
            metrics.keyword_match_pass += 1

        if result[
            "response_pass"
        ]:
            metrics.response_generation_pass += 1

        print(
            f"Test: {result['id']}"
        )

        print(
            f"Category: {result['category']}"
        )

        print(
            f"Passed: {result['passed']}"
        )

        print(
            f"Latency: "
            f"{result['latency_seconds']}s"
        )

        print(
            f"Expected Tools: "
            f"{result['expected_tools']}"
        )

        print(
            f"Actual Tools: "
            f"{result['actual_tools']}"
        )

        print(
            f"Response: "
            f"{result['response']}"
        )

        print(
            "--------------------------------"
        )

    summary = metrics.summary()

    print("\n============================")
    print(" EVALUATION SUMMARY ")
    print("============================")

    print(
        f"Total Cases: "
        f"{summary['total_cases']}"
    )

    print(
        f"Passed Cases: "
        f"{summary['passed_cases']}"
    )

    print(
        f"Overall Accuracy: "
        f"{summary['overall_accuracy']}%"
    )

    print(
        f"Tool Accuracy: "
        f"{summary['tool_accuracy']}%"
    )

    print(
        f"Keyword Accuracy: "
        f"{summary['keyword_accuracy']}%"
    )

    print(
        f"Response Accuracy: "
        f"{summary['response_accuracy']}%"
    )

    print("\nCategory Breakdown:")

    for category, values in (
        summary[
            "category_breakdown"
        ].items()
    ):

        print(
            f"- {category}: "
            f"{values['passed']}/"
            f"{values['total']}"
        )

    return {
        "summary": summary,
        "details": detailed_results
    }


if __name__ == "__main__":

    run_evaluation()
