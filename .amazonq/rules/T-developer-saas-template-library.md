# T‑Developer SaaS Template Library Specification

The `SaaS Template Library` is a structure that enables T‑Developer to manage pre-defined workflows (service compositions) as templates. These templates can be searched, selected, and cloned to quickly launch SaaS instances tailored to user goals.

---

## 1. Purpose

* Store validated workflow compositions as templates
* Enable template-based SaaS creation for specific user needs
* Allow `PlannerAgent` to use templates as recommendations
* Provide predefined combinations based on `AgentRegistry`

---

## 2. Template Definition Example

```json
{
  "id": "policy-matcher-v1",
  "title": "Policy Matching SaaS",
  "description": "Crawls *.go.kr, clusters results, and responds via chatbot",
  "workflow_id": "policy-match-flow-v1",
  "created_by": "admin",
  "agents": ["ScraperAgent", "ClusterAgent", "ChatAgent"],
  "tags": ["gov", "chat", "recommendation"],
  "input_schema": {"query": "string"},
  "output_schema": {"result": "string"},
  "created_at": "2025-07-22T01:00:00Z"
}
```

---

## 3. Storage & Retrieval Structure

* Storage: DynamoDB / S3 (`saas-templates/*.json`)
* Access via API or CLI:

  * `tdev list templates`
  * `tdev use template <id>`
* Search fields: title, tags, input/output schema, included agents

---

## 4. Integrated Components

| Component        | Role                                                |
| ---------------- | --------------------------------------------------- |
| `PlannerAgent`   | Can recommend templates based on goal similarity    |
| `EvaluatorAgent` | Assigns quality score and tracks template usage     |
| `tdev compose`   | Uses templates as presets when generating workflows |

---

## 5. CLI Integration Example

```bash
# List available templates
$ tdev list templates

# Use a template to create a new SaaS workflow
$ tdev use template policy-matcher-v1 --copy-as my-policy-matcher
```

---

## 6. Future Enhancements

* Template ranking system: Based on popularity, quality, success rate
* Auto-capture of execution profile metadata during use
* Slack message generation from templates ("shareable SaaS intro cards")
* Template PR submission via GitHub or internal team workflow

---

The SaaS Template Library acts as an “agent workflow parts marketplace,” helping T‑Developer users rapidly discover and launch executable SaaS configurations.
