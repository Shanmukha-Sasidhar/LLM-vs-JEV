import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = "https://openrouter.ai/api/alpha/decisions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

def run_jev(user_input):

    payload = {
        "model": "typesafe/jev-1.13",

        "state": user_input,

        "questions": {

            "urgent": {
                "type": "noul",
                "instructions": (
                    "Does this issue need immediate attention?"
                ),
            },

            "team": {
                "type": "choice",
                "instructions": (
                    "Which team should handle this issue?"
                ),
                "criteria": {
                    "infra": (
                        "Deployments, availability, "
                        "servers and on-call incidents."
                    ),
                    "billing": (
                        "Payments, invoices and subscriptions."
                    ),
                    "general": (
                        "General customer support issues."
                    ),
                },
            },

            "severity": {
                "type": "score",
                "instructions": (
                    "How severe is the impact?"
                ),
                "criteria": [
                    "Cosmetic.",
                    "Degraded for some users.",
                    "Full outage.",
                ],
            },
        },
    }

    start = time.perf_counter()

    response = requests.post(
        URL,
        headers=HEADERS,
        json=payload,
        timeout=60,
    )

    latency = time.perf_counter() - start

    response.raise_for_status()

    result = response.json()

    return result, latency


if __name__ == "__main__":

    text = (
        "The deploy failed twice and customers are "
        "seeing 500s. Can someone look now?"
    )

    result, latency = run_jev(text)

    print("\nJEV RESULT")
    print("=" * 40)

    print(result)

    print(f"\nLatency: {latency:.3f} seconds")