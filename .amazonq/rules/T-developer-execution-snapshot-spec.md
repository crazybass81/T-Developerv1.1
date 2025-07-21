# T‑Developer ExecutionSnapshot Specification

An `ExecutionSnapshot` is a structured record of a workflow execution event, capturing all relevant inputs, agent calls, intermediate outputs, metadata, and final results. This mechanism enables debugging, re-execution, evaluation comparison, and reproducibility within the T‑Developer platform.

---

## 1. Purpose

* Enable reproducibility and traceability of all agent-driven executions
* Support re-running workflows with identical or altered inputs
* Provide evaluation agents with historical performance context
* Serve as training data for planner/evaluator refinement

---

## 2. Snapshot Contents

| Field            | Description                                              |
| ---------------- | -------------------------------------------------------- |
| `snapshot_id`    | Unique ID for the execution snapshot                     |
| `workflow_id`    | ID of the executed workflow                              |
| `initiated_by`   | User, system, or agent name                              |
| `input`          | Initial input given to the meta/workflow agent           |
| `steps`          | List of execution steps, each with agent call and output |
| `final_output`   | The final result of the execution                        |
| `logs`           | Optional execution logs or system messages               |
| `execution_time` | Total runtime or timestamps per step                     |
| `score_metadata` | EvaluatorAgent scores attached at runtime (optional)     |
| `tags`           | Purpose or classification metadata                       |

---

## 3. Example JSON Structure

```json
{
  "snapshot_id": "snap-4839fe",
  "workflow_id": "wf-2930",
  "initiated_by": "PlannerAgent",
  "input": {
    "text": "Please generate a policy summary"
  },
  "steps": [
    {
      "agent": "SummarizerAgent",
      "input": "...",
      "output": "Summary text",
      "timestamp": "2025-07-22T12:00:01Z"
    },
    {
      "agent": "S3UploaderAgent",
      "input": "Summary text",
      "output": "s3://bucket/policy-summary.txt"
    }
  ],
  "final_output": "s3://bucket/policy-summary.txt",
  "execution_time": "2.1s",
  "score_metadata": {
    "quality_score": 0.91,
    "reuse_score": 0.85
  },
  "tags": ["policy", "summarization", "storage"]
}
```

---

## 4. Storage & Access

* Stored in `ExecutionSnapshotStore` (S3-backed or DynamoDB-backed)
* Queryable by:

  * `workflow_id`
  * `agent name`
  * `date range`
  * `tags`
* Versioned and immutable by default (append-only)

---

## 5. Use Cases

* Reproduce an error by fetching prior input and re-executing the same flow
* Debug failures by comparing snapshot steps and timestamps
* Provide `EvaluatorAgent` with history for contextual scoring
* Derive training examples for MetaAgent planning optimization

---

## 6. Integration

* Linked from `ServiceInstance`
* Written by `WorkflowExecutorAgent`
* Readable by: `PlannerAgent`, `EvaluatorAgent`, `TestRunner`

---

The `ExecutionSnapshot` model ensures that every meaningful workflow execution on T‑Developer is traceable, reproducible, and evaluable, providing a foundation for trust, learning, and optimization.
