# T‑Developer PlannerAgent Specification

The `PlannerAgent` is responsible for interpreting user inputs or service requests and determining which agents should be combined, and in what order, to achieve the given goal. It automatically generates a workflow definition and serves as the core inference module powering T‑Developer's autonomous SaaS composition system.

---

## 1. Key Functions

* Analyze user goals or commands (natural language, YAML, CLI, etc.)
* Query the AgentRegistry to identify candidate Tools, Agents, and Teams
* Divide the task into modular functional steps
* Generate JSON or YAML-based workflow definitions

---

## 2. Input Examples

### Form A: Natural Language Prompt

```text
Build a policy recommendation system for young entrepreneurs
```

### Form B: Structured Specification

```json
{
  "goal": "Summarize a document and upload to cloud",
  "inputs": ["document"],
  "output": "s3_url"
}
```

---

## 3. Output Example

Generated workflow definition (JSON):

```json
{
  "id": "summarize-upload-flow-v1",
  "inputs": {"doc": "string"},
  "steps": [
    {"id": "summarize", "agent": "SummarizerAgent", "input_from": "doc", "output_to": "summary"},
    {"id": "upload", "agent": "S3UploaderAgent", "input_from": "summary", "output_to": "s3_url"}
  ],
  "outputs": {"result": "s3_url"}
}
```

---

## 4. Internal Logic Flow

```plaintext
1. Parse input → extract goal / analyze keywords
2. Decompose into functions: input → processing → output
3. Search for suitable agents per function (based on AgentRegistry)
4. Assemble into workflow (define agent order and input/output mapping)
5. Return workflow object or save as file
```

---

## 5. Dependencies

* `AgentRegistry`: Used to find agents by name, description, input/output
* `LLM (optional)`: Can assist in goal decomposition or input summarization
* Callable via `tdev compose` CLI command

---

## 6. Future Enhancements

* Workflow optimization: minimize number of agents, prefer tools first
* Performance hints: support for tags like "fast", "low-cost"
* Agent version hints (e.g., `SummarizerAgent@v2`)
* Link with EvaluatorAgent for evaluation-feedback loop

---

The PlannerAgent serves as T‑Developer’s central automation brain that determines “what SaaS should be composed to achieve a given goal.”
