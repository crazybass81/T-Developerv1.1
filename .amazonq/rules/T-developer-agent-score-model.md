# T‑Developer AgentScoreModel Specification

The `AgentScoreModel` is an evaluation model that quantifies the reliability of a specific agent version based on factors such as test results, reusability, and execution quality. This model is referenced by components like the `EvaluatorAgent` and `AgentVersionManager`, and is used for auto-deployment decisions, prioritization, and user recommendations.

---

## 1. Purpose

* Quantify performance and stability per agent version
* Detect potential regressions
* Provide criteria for automatic deployment approval
* Recommend trustworthy agents to users

---

## 2. Input Factors

| Field                 | Description                                                    |
| --------------------- | -------------------------------------------------------------- |
| `test_result_history` | Aggregated pass/fail data from `TestRunHistoryStore`           |
| `execution_snapshots` | Real user execution data with quality scores (optional)        |
| `reuse_count`         | Number of times the agent is included in workflows or executed |
| `failure_rate`        | Failure rate from tests and executions (weighted by recency)   |
| `recency_weight`      | Weight factor for recent history                               |

---

## 3. Output Schema

```json
{
  "agent_name": "SummarizerAgent",
  "version": "1.3.0",
  "score": {
    "quality": 0.92,
    "stability": 0.87,
    "reusability": 0.93,
    "final_score": 0.91
  },
  "evaluated_at": "2025-07-24T03:00:00Z"
}
```

---

## 4. Scoring Algorithm (Default)

```plaintext
quality = pass_rate(last 5 test runs) * 0.7 + average_execution_quality * 0.3
stability = 1 - failure_rate (last 3 days)
reusability = normalized reuse_count score
final_score = quality * 0.5 + stability * 0.25 + reusability * 0.25
```

* Scoring weights can be adjusted based on agent type or context

---

## 5. Integration Points

| Component             | Usage                                                      |
| --------------------- | ---------------------------------------------------------- |
| `AgentVersionManager` | Approves deployment if score exceeds threshold             |
| `PlannerAgent`        | Prioritizes agents by reliability when composing workflows |
| `AgentUI`             | Displays score breakdown to users                          |
| `EvaluatorAgent`      | Compares with execution snapshot scores                    |

---

## 6. Extensible Dimensions

* Incorporate user feedback-based signals
* Add efficiency score (e.g., latency, resource cost)
* Train domain-specific weighting rules

---

The `AgentScoreModel` plays a central role in evaluating agents beyond test pass rates, combining practical usability, reliability, and adoption data. This score drives both automated decisions and user trust across the T‑Developer ecosystem.
