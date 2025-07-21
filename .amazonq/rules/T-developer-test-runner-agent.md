# T‑Developer TestRunnerAgent Specification

The `TestRunnerAgent` is responsible for executing test suites associated with agents and tools in the T‑Developer ecosystem. It serves as a bridge between the defined `AgentTestSuite` and the runtime environments where validation, regression, or CI/CD testing takes place.

---

## 1. Purpose

* Automatically execute test cases defined in AgentTestSuites
* Enable version-aware, CI-integrated testing pipelines
* Collect and report execution results with detailed metrics
* Trigger workflows for validation upon agent publication or update

---

## 2. Responsibilities

| Capability          | Description                                             |
| ------------------- | ------------------------------------------------------- |
| `load_test_suite`   | Load the test cases for the specified agent and version |
| `execute_case`      | Run individual test case, capture result                |
| `aggregate_results` | Summarize results across test cases                     |
| `record_results`    | Save pass/fail logs, metrics, and error details         |
| `trigger_webhook`   | Optional Slack or HTTP integration for reporting        |

---

## 3. Input Schema

```json
{
  "agent_name": "SummarizerAgent",
  "version": "1.2.0",
  "mode": "full", // or "single",
  "case_index": 0, // optional if single test case
  "output_format": "json"
}
```

---

## 4. Output Schema

```json
{
  "agent_name": "SummarizerAgent",
  "version": "1.2.0",
  "total": 10,
  "passed": 9,
  "failed": 1,
  "failures": [
    {
      "index": 3,
      "description": "Long paragraph truncation",
      "expected": "Short summary...",
      "actual": "Too long...",
      "strict": true
    }
  ],
  "duration": "4.3s"
}
```

---

## 5. Integration Points

* `AgentTestSuite`: Source of test case definitions
* `AgentVersionManager`: Triggers test runs on version publish
* `SlackNotifier` or `WebhookAgent`: Reports failures or results
* `EvaluatorAgent`: Reads recent test history for reliability scoring

---

## 6. Execution Modes

| Mode      | Description                                              |
| --------- | -------------------------------------------------------- |
| `full`    | Run all test cases for the agent and version             |
| `single`  | Run a specific test case (used for debugging or replay)  |
| `dry_run` | Load test cases and validate structure without execution |

---

## 7. Storage & Logging

* Results are appended to `TestRunHistoryStore`
* Can optionally be attached to ExecutionSnapshot metadata
* Logged via CLI, UI, or Slack

---

The `TestRunnerAgent` is essential to maintain trust and stability within T‑Developer. It empowers maintainers to verify agents at scale, avoid regressions, and drive automation across development and deployment.
