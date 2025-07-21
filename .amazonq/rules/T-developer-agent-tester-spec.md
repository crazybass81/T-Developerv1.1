# T‑Developer AgentTesterAgent Specification

The `AgentTesterAgent` performs automated testing on a single Tool or Agent. It verifies correct behavior by comparing actual outputs against expected input-output pairs or snapshot-based validations. This enables independent testing prior to system integration and supports CI automation.

---

## 1. Key Features

* Execute test cases for a specific Tool or Agent
* Validate response against expected outputs
* Support snapshot-based output comparison
* Return failure diagnostics and logs

---

## 2. Input Format

### Direct Output Comparison:

```json
{
  "target": "SummarizerAgent",
  "input": "This document is for testing.",
  "expected_output": "This is a test document."
}
```

### Snapshot Comparison:

```json
{
  "target": "GPTCallerTool",
  "input": "Hello",
  "snapshot": "snapshots/gptcaller_hello.out"
}
```

---

## 3. Output Example

### On Success:

```json
{
  "status": "pass",
  "diff": null,
  "duration_ms": 1321,
  "log": "Output matched expected value."
}
```

### On Failure:

```json
{
  "status": "fail",
  "diff": "Expected 'Summary', got 'This is the summary.'",
  "duration_ms": 1789,
  "log": "Mismatch detected at sentence level."
}
```

---

## 4. Internal Execution Flow

```plaintext
1. Load target Tool or Agent from AgentRegistry
2. Execute: result = run(input)
3. Compare result with expected_output or snapshot file
4. Generate diff if mismatch exists
5. Return test result (JSON) + logs
```

---

## 5. Usage Scenarios

* Execute via CLI: `tdev test agent_name`
* Integrate into CI pipelines (e.g., GitHub Actions)
* Run prior to classification or evaluation stages

---

## 6. Planned Extensions

* Schema-driven test case mutation
* Batch execution with multi-case JSON (`cases.json`)
* Slack notifications on test failure
* Test coverage tracking and report generation

---

AgentTesterAgent ensures component-level quality assurance across the T‑Developer ecosystem, enabling test-driven development and secure deployment of agents and tools.
