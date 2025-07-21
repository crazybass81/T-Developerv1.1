# T‑Developer Workflow Definition Specification

T‑Developer workflows define goal-oriented execution flows composed of multiple tools and agents. This document outlines the structure specification, definition format, execution logic, and practical usage.

---

## 1. Purpose

* Connect agent-level functionalities into a unified service execution flow
* Support static/dynamic flows, branching, and conditional logic
* Enable traceable and reproducible SaaS compositions

---

## 2. Workflow Definition Spec (JSON)

```json
{
  "id": "policy-match-flow-v1",
  "description": "Crawl policies → Cluster → Chat response",
  "inputs": {
    "query": "string"
  },
  "steps": [
    {
      "id": "scrape",
      "agent": "ScraperAgent",
      "input_from": "query",
      "output_to": "raw_policies"
    },
    {
      "id": "cluster",
      "agent": "ClusterAgent",
      "input_from": "raw_policies",
      "output_to": "grouped_policies"
    },
    {
      "id": "chat",
      "agent": "ChatAgent",
      "input_from": "grouped_policies",
      "output_to": "final_response"
    }
  ],
  "outputs": {
    "result": "final_response"
  }
}
```

---

## 3. Key Fields

| Field         | Description                                               |
| ------------- | --------------------------------------------------------- |
| `id`          | Workflow identifier (include version if applicable)       |
| `description` | Summary of the workflow's purpose and function            |
| `inputs`      | Structure of input values received from the user          |
| `steps`       | List of agent execution steps (sequential or conditional) |
| `input_from`  | Source input (prior step’s output or initial inputs)      |
| `output_to`   | Key where this step’s output is saved                     |
| `outputs`     | Final output returned from the workflow                   |

---

## 4. Execution Logic

The `WorkflowExecutorAgent` (or an external orchestrator) executes the workflow using the following logic:

1. Save initial `inputs` into execution context
2. Execute `steps` in sequence, saving each output to context
3. After all steps are complete, extract `outputs` from context and return result

> Advanced controls like failure handling, retry, and conditional branching can be supported via DSL extensions or future `condition` fields.

---

## 5. Extension Options

* `condition`: Conditional execution (e.g., `if input.language != "ko" then translate`)
* `parallel`: Indicates steps should run in parallel (`parallel: true`)
* `tool`: Tools can also be used in steps just like agents
* `workflow_ref`: Reference to a sub-workflow (recursive execution supported)

---

## 6. Storage and Location

* Version-controlled via Git (`/flows/policy-match-flow-v1.json`)
* Metadata stored in DynamoDB (author, date, version, etc.)
* Optionally uploaded to S3 as lightweight cache

---

## 7. Example Workflow IDs

* `summarize-translate-flow-v1`
* `agent-onboarding-flow-v1`
* `llm-api-call-and-log-flow`

---

The T‑Developer workflow definition schema allows declarative composition of agent execution flows and supports a reproducible, flexible SaaS orchestration environment via extensible DSLs and step logic.
