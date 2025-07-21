# T‑Developer WorkflowExecutorAgent Specification

The `WorkflowExecutorAgent` interprets defined workflows into executable, step-by-step flows. It executes each defined step, manages input/output contexts, and returns the final result. This is the core runtime engine for all T‑Developer workflows. It is invoked via the `tdev run` command or directly from a PlannerAgent or RouterAgent.

---

## 1. Responsibilities

* Interpret workflow definitions (JSON/YAML)
* Sequentially execute each step
* Invoke the corresponding agent per step
* Manage input/output context across steps
* Return the final output and execution trace

---

## 2. Input / Output

### Input

```json
{
  "workflow_id": "policy-match-flow-v1",
  "inputs": {
    "query": "Startup support for youth"
  }
}
```

### Output

```json
{
  "result": "This policy targets young entrepreneurs...",
  "trace": [
    {"step": "scrape", "status": "success"},
    {"step": "cluster", "status": "success"},
    {"step": "chat", "status": "success"}
  ]
}
```

---

## 3. Internal Execution Flow

```plaintext
1. Load workflow definition (from S3 or local path)
2. Initialize context with initial inputs
3. For each step:
   - Identify agent name
   - Extract inputs from context
   - Execute agent.run(input)
   - Store output back into context
4. Return the final value defined in `outputs`
```

---

## 4. Module Structure

```python
class WorkflowExecutorAgent:
    def __init__(self, registry):
        self.agent_registry = registry  # Maps agent name → instance

    def run(self, workflow_id: str, inputs: dict) -> dict:
        workflow = self.load_workflow(workflow_id)
        context = inputs.copy()
        trace = []

        for step in workflow["steps"]:
            agent = self.agent_registry[step["agent"]]
            agent_input = context[step["input_from"]]
            result = agent.run(agent_input)
            context[step["output_to"]] = result
            trace.append({"step": step["id"], "status": "success"})

        return {
            "result": context[workflow["outputs"]["result"]],
            "trace": trace
        }
```

---

## 5. Error Handling and Retry (Basic)

* Wrap each step in `try/except` block
* Log failures to trace
* Future support: conditional branching and fallback strategies

---

## 6. Planned Extensions

* Add support for branching (`if`) and looping (`loop`) fields
* Send results to external channels (e.g., Slack notifications)
* Upload full execution logs to CloudWatch or external LogStore

---

This agent is the execution backbone of all workflows in T‑Developer. It is the bridge that turns agent composition into working SaaS services.
