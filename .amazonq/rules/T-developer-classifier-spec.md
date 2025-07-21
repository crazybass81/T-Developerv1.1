# T‑Developer ClassifierAgent Specification

The `ClassifierAgent` in T‑Developer analyzes Python files to automatically classify them as a Tool, Agent, or Team. This classification is based on structural complexity, the number of decision-making points ("brains"), and reusability, forming a core foundation for SaaS auto-composition.

---

## 1. Overview

**Input**:

* Python file path or code string

**Output** (JSON metadata):

```json
{
  "name": "SummarizerAgent",
  "type": "agent",
  "brain_count": 1,
  "reusability": "high",
  "path": "s3://tdev-codebase/agents/summarizer.py"
}
```

---

## 2. Classification Criteria

| Condition                                     | Classified As   |
| --------------------------------------------- | --------------- |
| No decision-making logic                      | Tool            |
| One decision-making point                     | Agent           |
| Two or more decision points, no coordinator   | Composite Agent |
| Two or more decision points with coordination | Team            |

**Decision logic ("brain") is identified via:**

* Branching structures like `if`, `match`, `try/except`, `switch`
* Conditional logic based on LLM responses
* Internal routing among tools or agents

---

## 3. Analysis Process

1. Parse Python source code into AST
2. Extract conditional logic inside `run()` or core functions
3. Detect nested agent/tool calls (coordination patterns)
4. Count distinct "brains" and analyze call hierarchy
5. Generate classification and metadata

---

## 4. Examples

### Example 1: Tool

```python
@tool
def s3_uploader(data: str):
    upload_to_s3(data)
```

No decisions → Classified as Tool

### Example 2: Agent

```python
@agent
def summarize(text: str):
    if len(text) > 1000:
        text = text[:1000]
    return call_gpt("Summarize this:", text)
```

One decision → Agent

### Example 3: Team

```python
@agent
def planner(input):
    if "report" in input:
        return summarizer.run(input)
    elif "json" in input:
        return converter.run(input)
    else:
        return fallback.run(input)
```

Three decisions, coordinating sub-agents → Team

---

## 5. Output Metadata Example

```json
{
  "name": "ReportPlanner",
  "type": "team",
  "brain_count": 3,
  "reusability": "low",
  "agents": ["SummarizerAgent", "ConverterAgent"],
  "path": "s3://tdev-codebase/teams/planner.py"
}
```

---

## 6. Notes

* Reusability is inferred from brain count, number of dependencies, and external API usage
* If AST analysis is insufficient, LLM-based code reasoning may supplement
* Output is stored in AgentStore or DynamoDB

---

## 7. Future Extensions

* Classify decision-making types (e.g., rule-based vs LLM-based)
* Visualize brain structure as a decision tree
* Add predictive reusability scoring

---

This specification defines a foundational component for T‑Developer’s autonomous structure classification and SaaS composition system.
