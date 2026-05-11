import json
import os

from evaluation.evaluator import (
    run_evaluation
)

BASE_DIR = os.path.dirname(__file__)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "optimization_report.json"
)


class PromptOptimizer:

    def __init__(self):

        self.recommendations = []

    def analyze_failures(
        self,
        results
    ):

        failures = []

        for result in results["details"]:

            if not result["passed"]:

                failures.append(result)

        for failure in failures:

            self.generate_recommendation(
                failure
            )

        return failures

    def generate_recommendation(
        self,
        failure
    ):

        recommendation = {
            "test_id": failure["id"],
            "recommendations": []
        }

        if not failure[
            "tool_selection_pass"
        ]:

            recommendation[
                "recommendations"
            ].append(
                (
                    "Improve tool selection "
                    "prompt clarity"
                )
            )

        if not failure[
            "keyword_pass"
        ]:

            recommendation[
                "recommendations"
            ].append(
                (
                    "Improve final response "
                    "grounding"
                )
            )

        if not failure[
            "response_pass"
        ]:

            recommendation[
                "recommendations"
            ].append(
                (
                    "Improve Gemini response "
                    "generation reliability"
                )
            )

        self.recommendations.append(
            recommendation
        )

    def save_report(self):

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.recommendations,
                f,
                indent=2
            )


def optimize():

    results = run_evaluation()

    optimizer = PromptOptimizer()

    failures = (
        optimizer.analyze_failures(
            results
        )
    )

    optimizer.save_report()

    print("\n============================")
    print(" OPTIMIZATION REPORT ")
    print("============================")

    print(
        f"Total Failures: "
        f"{len(failures)}"
    )

    if failures:

        print(
            "\nRecommendations:"
        )

        for recommendation in (
            optimizer.recommendations
        ):

            print(
                f"\nTest ID: "
                f"{recommendation['test_id']}"
            )

            for item in (
                recommendation[
                    "recommendations"
                ]
            ):

                print(f"- {item}")

    else:

        print(
            "No optimization required."
        )


if __name__ == "__main__":

    optimize()
