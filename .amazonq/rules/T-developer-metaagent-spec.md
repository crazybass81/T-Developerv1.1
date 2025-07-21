# T‑Developer MetaAgent Specification

A `MetaAgent` is a high-level agent composed of other agents—especially ClassifierAgent, PlannerAgent, EvaluatorAgent, and WorkflowExecutorAgent. It acts as an orchestrating brain that governs the end-to-end flow of SaaS generation, from classification to planning, evaluation, and execution. While each individual agent performs a narrow, specialized task, the MetaAgent coordinates them into a coherent, autonomous development loop.

---

## 1. Purpose

* Orchestrate and unify core system agents into a single intelligent controller
* Enable autonomous SaaS generation and composition workflows
* Provide API endpoints or CLI integration to trigger end-to-end flows

---

## 2. Core Components

| Component               | Description                                               |
| ----------------------- | --------------------------------------------------------- |
| `ClassifierAgent`       | Analyzes uploaded Python files and classifies components  |
| `PlannerAgent`          | Composes agents into workflows based on purpose           |
| `EvaluatorAgent`        | Scores workflows or agents on quality/cost/suitability    |
| `WorkflowExecutorAgent` | Executes workflows with support for logs, retries, status |

Optional submodules:

* `AgentStoreAdapter`
* `SlackNotifier`
* `TestRunner`

---

## 3. Control Flow

1. **Input**: Developer prompt, SaaS goal, or Python file
2. **Classification**: Call `ClassifierAgent`
3. **Planning**: Invoke `PlannerAgent` with component set
4. **Evaluation**: Call `EvaluatorAgent` for fitness scoring
5. **Execution**: Launch `WorkflowExecutorAgent`
6. **Result**: Return service instance ID, logs, cost estimate

---

## 4. Definition Example

```json
{
  "name": "AutoOrchestratorAgent",
  "type": "meta-agent",
  "sequence": ["ClassifierAgent", "PlannerAgent", "EvaluatorAgent", "WorkflowExecutorAgent"],
  "input_schema": {
    "source": "python_file | goal_string"
  },
  "output_schema": {
    "service_instance_id": "string",
    "logs": "string",
    "score": "float"
  }
}
```

---

## 5. Use Cases

* Trigger full SaaS generation from goal prompt
* Auto-generate workflows and evaluate them for quality
* Integrate with CLI command: `tdev build full` or `tdev auto`.

---

## 6. Integration

* `AgentStore`: Retrieves and persists agent/module definitions
* `SlackNotifier`: Reports results to dev channel
* `DevSecOps`: Can trigger builds and tests after planning phase
* `UI Launcher`: Visual orchestration and monitoring interface (future)

---

## 7. Future Extensions

* Support for multi-MetaAgent comparison (benchmarking strategies)
* MetaAgent versioning and subgraph branching
* Partial override: allow swapping a Planner or Evaluator dynamically
* Chain of MetaAgents for incremental composition pipelines

---

A MetaAgent is a strategic orchestrator that makes T‑Developer autonomous. It unifies otherwise modular components into intelligent, self-guiding software builders.
