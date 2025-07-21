# T‑Developer AgentStore API Specification

The `AgentStore` is the core interface for persisting, retrieving, and managing metadata and definitions of agents (tools, single-agent units, and teams). It acts as the operational backend for ClassifierAgent, AutoAgentComposer, EvaluatorAgent, CLI, and UI Launcher.

---

## 1. Purpose

* Central repository for all agent definitions
* Provide consistent storage and access across modules
* Support versioning, tagging, filtering, and metadata access
* Enable CLI and Web API integration

---

## 2. Core Endpoints

### POST `/agent`

* Create or register a new agent definition
* Body:

```json
{
  "name": "SummarizerAgent",
  "type": "agent",
  "brain_count": 1,
  "reusability": "high",
  "tools": ["GPTCallerTool"],
  "path": "s3://.../summarizer.py",
  "metadata": { ... }
}
```

### GET `/agent/{name}`

* Fetch agent definition by name
* Optional query: `?version=v2`

### PUT `/agent/{name}`

* Update metadata or file path
* Includes optional override for versions or reusability

### DELETE `/agent/{name}`

* Delete registered agent (soft or hard delete configurable)

### GET `/agents`

* Search or list agents
* Filters:

  * `type=tool|agent|team`
  * `reusability=high|low|A|B|C`
  * `tags=embedding,llm`
  * `brain_count>=2`

---

## 3. Schema Specification

Agent metadata schema follows the ClassifierAgent output standard:

```json
{
  "name": "QRCodeResolverAgent",
  "type": "agent",
  "path": "s3://tdev-codebase/agents/qr_resolver.py",
  "tools": ["QRCodeReaderTool", "UserLookupTool"],
  "brain_count": 1,
  "reusability": "B",
  "tags": ["auth", "qr"],
  "created_at": "2025-07-21T03:00:00Z",
  "description": "Resolves user ID from QR image"
}
```

---

## 4. Authentication & Access Control

* Auth via API key or bearer token
* Optional roles: `admin`, `contributor`, `reader`
* Some agents can be flagged `public: true`

---

## 5. Integration Points

| Component           | Purpose                                         |
| ------------------- | ----------------------------------------------- |
| `ClassifierAgent`   | Store new classification results                |
| `AutoAgentComposer` | Register newly generated agents                 |
| `EvaluatorAgent`    | Update evaluation results or reusability scores |
| `UI Launcher`       | Load agent metadata + schema for UI generation  |
| `CLI (tdev)`        | CRUD agents from developer machine              |

---

## 6. Planned Extensions

* Git-backed agent metadata history
* WebSocket push updates to connected UIs
* Multi-tenant namespace support
* Linked test cases or snapshots (`/agent/{name}/tests`)
* Version freeze and branching support

---

The AgentStore API is the backbone of operational agent orchestration across the T‑Developer platform. It ensures consistency, reuse, and visibility of modular capabilities across the agent lifecycle.
