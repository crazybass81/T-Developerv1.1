# T‑Developer Team Structure Specification

A `Team` is a higher-order executable unit composed of two or more decision-capable agents. Each agent performs a distinct role, and the team is coordinated by a controller or branching logic that orchestrates execution. This structure is used when generating complex SaaS systems or representing role-based workflows.

---

## 1. Purpose

* Define composite structures requiring two or more decision functions
* Group independent agents into a single logical unit
* Provide PlannerAgent with a structure it can recommend and compose
* Manage execution flow via an internal `controller`

---

## 2. Components

| Component       | Description                                                                |
| --------------- | -------------------------------------------------------------------------- |
| `agents`        | List of agents included in the team                                        |
| `controller`    | The upper-level agent responsible for branching, selecting, and sequencing |
| `strategy`      | Execution strategy: sequential, conditional, or parallel                   |
| `input_schema`  | Input format for the team                                                  |
| `output_schema` | Output format from the team                                                |

---

## 3. Definition Example

```json
{
  "name": "ReportHandlingTeam",
  "type": "team",
  "controller": "DispatcherAgent",
  "agents": ["SummarizerAgent", "ConverterAgent", "FallbackAgent"],
  "strategy": "conditional",
  "input_schema": {
    "input": "string"
  },
  "output_schema": {
    "result": "string"
  }
}
```

---

## 4. Classification Rules

* If the ClassifierAgent detects ≥2 decision points + controller → classify as team
* PlannerAgent may recommend a team structure based on user intent
* EvaluatorAgent may assess the quality of a team in terms of accuracy, cost, or robustness

---

## 5. Execution Strategies

### Strategy: `conditional`

* Executes a different agent based on input condition (e.g. if "report" → use summarizer)

### Strategy: `sequential`

* Executes agents in a predefined order

### Strategy: `parallel`

* Executes all agents in parallel → merges or selects results based on policy

---

## 6. Integration & Storage

* Stored in `AgentStore` with type=`team`
* Executed via `WorkflowExecutorAgent`
* Configurable per-agent version via `AgentVersionManager`

---

## 7. Future Extensions

* Recursive team structure support (teams within teams)
* Hybrid teams with external SaaS APIs as agents
* Real-time collaboration visualization via Slack/API
* Interruptible or observable execution control

---

The `Team` is a foundational abstraction within the T‑Developer platform that enables high-complexity, modular SaaS orchestration based on role and execution strategy.
