import time
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openrouter import ChatOpenRouter

load_dotenv()
from langsmith import traceable


class Decision(BaseModel):
    urgent: bool = Field(
        description="Whether the issue requires immediate attention"
    )

    team: Literal["infra", "billing", "general"] = Field(
        description="Team that should handle the issue"
    )

    severity: float = Field(
        description="Severity from 0.0 to 1.0"
    )


llm = ChatOpenRouter(
    model="openrouter/free",
    temperature=0
)

structured_llm = llm.with_structured_output(Decision)


@traceable(
    name="LLM Decision",
    project_name="JEV-vs-LLM"
)
def run_llm(user_input: str):

    start = time.perf_counter()

    result = structured_llm.invoke(
        f"""
        Analyze this support/incident request:

        {user_input}

        Determine:

        1. Is it urgent?
        2. Which team should handle it?
           - infra: deployments, availability, incidents
           - billing: payments, invoices, subscriptions
           - general: everything else

        3. Give a severity score between 0 and 1.
        """
    )

    latency = time.perf_counter() - start

    return {
        "urgent": result.urgent,
        "team": result.team,
        "severity": result.severity,
        "latency": latency,
    }


if __name__ == "__main__":

    input_text = (
        "The deploy failed twice and customers are "
        "seeing 500s. Can someone look now?"
    )

    result = run_llm(input_text)

    print("\nLLM RESULT")
    print("-----------")
    print("Urgent:", result["urgent"])
    print("Team:", result["team"])
    print("Severity:", result["severity"])
    print(f"Latency: {result['latency']:.3f}s")