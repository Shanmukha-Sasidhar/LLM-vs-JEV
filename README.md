# JEV vs LLM

A simple project comparing **JEV and an LLM for decision-making** using the same input.

The project asks both models to determine:

- Whether an issue is urgent
- Which team should handle it
- How severe the issue is

JEV uses **Noul, Choice, and Score**, while the LLM uses structured output.

## Example Output

### JEV

```text
Urgency: 0.97
Team: infra
Confidence: 1.0
Severity: 1.61 / 2
Latency: 1.655s
```

### LLM

```text
Urgent: True
Team: infra
Severity: 0.9 / 1
Latency: 2.890s
```

In this test, both models selected **infra**, while JEV returned additional probabilities and confidence information.
