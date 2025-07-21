# T‑Developer CLI Command Specification v1.0

T‑Developer automates agent definition, structural classification, workflow composition, and SaaS deployment. This functionality is accessible via a CLI (Command Line Interface) designed for use by both users and external systems. This document defines the initial set of CLI commands.

---

## 1. CLI Entry Point

```bash
tdev [command] [options]
```

---

## 2. Command List

### 🧱 Tool/Agent Initialization

#### `tdev init tool`

* Create a tool based on a predefined template

```bash
tdev init tool --name GPTCallerTool --template llm-call
```

#### `tdev init agent`

* Create a single-brain agent from a template

```bash
tdev init agent --name SummarizerAgent --tool GPTCallerTool
```

---

### 🧠 Classification & Registration

#### `tdev classify`

* Analyze a Python file and classify it as Tool, Agent, or Team

```bash
tdev classify ./agents/summarizer.py
```

#### `tdev register`

* Register an agent to the AgentStore (S3 + metadata)

```bash
tdev register ./agents/summarizer.py
```

---

### 🧩 Workflow Composition & Execution

#### `tdev compose`

* Create a workflow definition (YAML or JSON)

```bash
tdev compose --name policy-flow --steps agentA,agentB
```

#### `tdev run`

* Execute a defined workflow

```bash
tdev run policy-flow-v1 --input query="Startup support for youth"
```

---

### 🚀 Service Instantiation & Deployment

#### `tdev build`

* Create a service instance from the composed workflow

```bash
tdev build --workflow policy-flow-v1
```

#### `tdev deploy`

* Deploy to Lambda or ECS

```bash
tdev deploy --service-id policy-matcher-v1 --target lambda
```

#### `tdev status`

* Check the status of a deployed service instance

```bash
tdev status policy-matcher-v1
```

---

## 3. Configuration File Structure

The CLI commands reference or generate configuration files inside the `.tdev/` directory:

```plaintext
.tdev/
 ├─ registry.json          # Registered Agent list
 ├─ workflows/             # Defined workflows
 └─ instances/             # Service instance metadata files
```

---

## 4. Planned Extensions

* `tdev explain` – Visualize structure / brain count
* `tdev edit` – Modify workflow or agent logic
* `tdev compare` – Compare structure of two workflows or agents

---

T‑Developer CLI is the primary interface enabling non-experts to design, compose, and deploy SaaS with a single command. This specification defines the foundation for all automation pipelines that follow.
