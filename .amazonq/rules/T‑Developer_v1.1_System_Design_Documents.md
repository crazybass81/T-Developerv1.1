알겠습니다. Amazon Q Developer가 T‑Developer v1.1 설계 문서를 자동 생성할 수 있도록, 제가 직접 필요한 문서의 리스트를 작성하고 각 문서를 영문으로 작성해드리겠습니다.

이 문서 세트는 API 명세서, 아키텍처 다이어그램, CI/CD 파이프라인 설계, 테스트 전략, 보안 가이드라인, IAM 정책 등 Amazon Q가 이해하고 생성 가능한 형식에 맞춰 구성하겠습니다. 완료되면 확인하실 수 있도록 정리해드릴게요.


# T‑Developer v1.1 System Design Documents

Below is a comprehensive set of system design documents for **T‑Developer v1.1**, based on the agent automation system architecture. These documents serve as inputs for Amazon Q Developer’s downstream development, providing clear specifications and guidance. The required documents include:

* **System Overview Document** – Purpose, scope, and high-level functionality of T‑Developer v1.1
* **Component Specification Document** – Details of core components (Agent Squad Orchestrator, Agno, Amazon Q Developer, Agent Core (AWS Bedrock), UI integrations)
* **API Specification** – Definitions of REST/event-driven interfaces between agents, orchestrator, tools, and frontend (with input/output schemas)
* **CI/CD Pipeline Design** – Automation process from code generation to deployment (GitHub Actions / AWS CodePipeline)
* **Agent Metadata Schema** – Structure of the agent registry entries (agent ID, purpose, inputs, outputs, tools used, etc.)
* **IAM and Security Policy Guide** – Security practices, IAM roles/permissions for agents, Q Developer, and deployment targets
* **Testing Strategy** – How generated agents/tools are automatically tested (unit tests, integration tests, EvaluatorAgent roles)
* **Deployment Architecture Diagram & Description** – Diagrams and narrative of how the system runs on AWS (Lambda, API Gateway, DynamoDB, etc.)
* **Agent Lifecycle Document** – Lifecycle of agents (creation, testing, deployment, versioning, retirement)
* **Roadmap Summary** – Phase-wise breakdown of development, key milestones, and current progress

Each document is presented in detail below.

## 1. System Overview Document

### Purpose and Scope

T‑Developer v1.1 is a **meta-agent orchestration framework** for automating software development tasks and composing SaaS applications from reusable components. The system’s purpose is to enable complex goals (from developers or end-users) to be achieved by a coordinated “squad” of specialized AI agents. It automates the workflow from understanding a request to delivering a functional deployed service, potentially generating new components on the fly to fill capability gaps.

The scope of T‑Developer includes: analyzing code or requirements, planning multi-step solutions, generating any missing tools or agents, executing workflows of agents/tools, and deploying the resulting application. It covers the **entire software lifecycle** from design and implementation to testing and deployment, with minimal human intervention.

### High-Level Functionality

At a high level, T‑Developer operates by classifying and organizing components, orchestrating agent teams, and dynamically extending its capabilities:

* **Hierarchical Component Model:** All building blocks are classified as either **Tools** (no decision logic, “0 brains”), **Agents** (single decision point, “1 brain”), or **Teams** (multi-agent assemblies, “2+ brains”). This taxonomy lets the system treat simple functions differently from complex autonomous agents or coordinated teams.
* **Agent Squad Orchestration:** A **MetaAgent Orchestrator** (also called **DevCoordinator** or SupervisorAgent) coordinates a sequence of core agents – such as Classifier, Planner, Evaluator, and Workflow Executor – to handle each user request. This orchestrator is the “central brain” ensuring the right agent does the right task at the right time.
* **Pipeline of Specialized Agents:** When a user submits a goal or code, the orchestrator triggers a pipeline: the **ClassifierAgent** determines what kind of component the input is, the **PlannerAgent** devises a plan (workflow) to achieve the goal, the **EvaluatorAgent** reviews the plan’s quality, and the **WorkflowExecutorAgent** carries out the plan step by step. Each agent has a specialized role (analysis, planning, quality-checking, execution) in this pipeline.
* **Dynamic Agent/Tool Generation:** If the system identifies that no existing component can fulfill a required functionality, it invokes **Agno (AutoAgentComposer)** to generate a new agent or tool on demand. This allows T‑Developer to **expand its capabilities autonomously**, creating new code modules based on high-level specifications.
* **Continuous Learning and Reuse:** All agents and tools are registered in a central **AgentRegistry**, so once created, they can be reused in future workflows. The system is extensible – new components can be added manually or via generation, and they become immediately available for orchestration.
* **Integration with Development & Deployment:** T‑Developer is designed to integrate into development workflows and cloud infrastructure. It can run locally (via CLI) for development, and deploy services to AWS (Lambda, ECS) for production without containerization. It also hooks into CI/CD pipelines for automated testing and deployment (detailed in the CI/CD document).

**In summary**, T‑Developer v1.1 enables a high-level “describe what you need” approach to software creation. The system translates user goals into orchestrated actions by multiple AI agents, coordinating everything from code understanding to cloud deployment. This overview has outlined the purpose (automating SaaS app development) and core functionality (multi-agent orchestration and on-demand generation) of the system. The following documents delve into specific components and design details of this architecture.

## 2. Component Specification Document

This document specifies the key components of the T‑Developer v1.1 architecture, including their roles and interactions. The core components include the **Agent Squad Orchestrator**, **Agno (Agent Generator)**, **Amazon Q Developer integration**, **Agent Core (AWS Bedrock)**, and **User Interface Integrations**. Each component is described below:

### 2.1 Agent Squad Orchestrator (MetaAgent)

**Role:** The Agent Squad Orchestrator (implemented as a MetaAgent, sometimes called **DevCoordinator** or SupervisorAgent) is the central coordinator of the system. It acts as the “brain of the operation,” controlling the flow of tasks and information among various specialized agents.

**Responsibilities:**

* Initiates and manages the end-to-end workflow for each user request. It decides **which agents or teams to invoke in what sequence** to handle the request.
* Delegates tasks to core agents: it sends code to the ClassifierAgent, goals to the PlannerAgent, tentative plans to the EvaluatorAgent, etc., and collects their outputs.
* Makes high-level decisions based on agent outputs, such as whether a plan is good enough to execute or needs refinement. For example, if the EvaluatorAgent returns a low quality score, the orchestrator can loop back to the PlannerAgent for a revised plan.
* Handles exceptions and control flow: if an agent indicates an error or missing capability, the orchestrator can choose to invoke Agno to create a new component, or adjust the workflow accordingly. It ensures errors are caught and either retried or escalated properly.
* Coordinates parallelism or team execution when applicable. (T‑Developer integrates an AWS Agent Squad framework that allows parallel agent execution and advanced routing, preparing for more complex future scenarios.) In the current design, the orchestrator primarily runs agents in sequence per the workflow, but the architecture allows concurrency if needed in future.

**Implementation:** The Orchestrator is itself an agent (MetaAgent) that embodies the logic of coordinating others. It often takes the form of a loop or sequence encoded in the **OrchestratorTeam** – a predefined team that uses the orchestrator to call the core agents in order. This means the orchestrator’s internal logic is configurable as a team workflow, enabling adjustments to the orchestration process if necessary. The orchestrator uses the AgentRegistry to look up available agents and tools at runtime, ensuring that any newly added components are considered in planning.

**Interaction Example:** A user’s request triggers the Orchestrator. The Orchestrator calls: (1) **ClassifierAgent** to interpret any provided code or context (checking registry for known components), (2) **PlannerAgent** to break down the goal using available agents, (3) **EvaluatorAgent** to score the proposed plan, and then (4) **WorkflowExecutorAgent** to execute the steps if the plan is approved. Throughout, the Orchestrator monitors outputs and can loop back or terminate as needed. This sequencing is illustrated in the orchestrator’s sequence diagram and ensures a smooth flow from user input to final result.

### 2.2 Agno – AutoAgentComposer (Agent Generator)

**Role:** **Agno** is the agent generation subsystem of T‑Developer. It automatically creates new **Agents** or **Tools** when the existing library lacks a capability for a given task. Agno’s name comes from “Agent Generator,” reflecting its function as the creative engine of the system.

**Functionality:** When invoked, Agno takes a high-level specification of a desired capability and produces ready-to-use code (and metadata) for a new agent or tool. Key aspects of its operation include:

* **Specification Intake:** Agno accepts input in either natural language or structured JSON form describing what the new component should do (goal, inputs, outputs, and any hints like tools to use). For example, a prompt *“Create an agent that scans a QR image and returns the associated username”* or an equivalent JSON spec can be provided to Agno.
* **Analysis & Planning:** Agno parses the specification to identify requirements: it figures out what steps or sub-tasks are needed and which existing tools/agents could be composed to achieve the goal. It may query the AgentRegistry to see if components with similar functionality already exist, to avoid duplication. Based on this, it devises an internal plan or template for the new agent.
* **Code Generation:** Using predefined code **templates and rules**, Agno constructs the agent’s code and metadata. It ensures the generated agent follows T‑Developer’s conventions. For instance, it will create a Python function or class with the `@agent` decorator, internal calls to necessary tools, and a proper return value. An example output might be an agent that calls two tools in sequence (first a QRCodeReaderTool, then a UserDBLookupTool) to fulfill the task. The metadata for the new agent is also generated, including its name, type, input/output fields, and the list of tools it uses.
* **Registration & Classification:** After generating code, Agno interacts with core system agents to finalize the new component. It sends the new code to the **ClassifierAgent** for validation – determining the component’s type (agent vs tool), “brain count,” and reusability tier. This classification is added to the metadata. Then Agno **registers** the new agent/tool in the AgentRegistry so it becomes immediately available for use. Agno finally returns the new component’s definition back to the orchestrator or developer that requested it.

**Integration:** Agno (implemented primarily as the **AutoAgentComposer** agent) is invoked in two scenarios:

* *On-Demand Generation:* During workflow planning, if the PlannerAgent (or orchestrator) finds a missing step, it triggers Agno to create a needed agent/tool. The orchestrator provides Agno with a spec for the missing functionality, and Agno returns a new component which is then incorporated into the workflow. This enables **just-in-time capability generation**, so the system can solve novel problems without human-added code.
* *Direct Developer Use:* Developers can explicitly call Agno via CLI commands, e.g. `tdev generate agent --name X --goal "..."`, to create new components based on their descriptions. This is useful for bootstrapping new features. The generated agent appears in the project’s codebase and registry, and can be further edited or refined if needed.

**Significance:** Agno ensures T‑Developer is not limited by its initial library of agents/tools. It systematically expands that library following best practices. The use of domain-specific generation rules and code templates guarantees consistency and quality in generated code. Agno even integrates with Amazon Q Developer for possible **code refinement** – after generation, the code can be reviewed or improved by AI (or humans) before finalization. This human/AI-in-the-loop refinement process helps maintain high code quality. In short, Agno gives T‑Developer a self-extending capability, crucial for an autonomous development system.

### 2.3 Amazon Q Developer Integration

**Role:** **Amazon Q Developer** is an AI-assisted development platform that works in tandem with T‑Developer. In the context of T‑Developer v1.1, Amazon Q Developer acts as both a **consumer of design documents** and a **partner in code generation/refinement**. It is the system that will use the specifications and documents we are generating to drive downstream development – for example, automatically producing code, documentation, or configurations based on these designs.

**Functionality:** In the T‑Developer architecture, Amazon Q Developer provides higher-level orchestration and quality assurance:

* **Documentation-Driven Development:** The comprehensive design documents (like this set) are fed into Amazon Q Developer, which can parse them and generate corresponding boilerplate code, stubs, or configuration. Essentially, Amazon Q Developer can use the system overview, component specs, API definitions, etc., as input to ensure that the implemented system matches the intended design. This might include generating service infrastructure (CloudFormation/Terraform), interface definitions, or even agent code skeletons consistent with the design.
* **Code Refinement and Review:** As noted in Agno’s integration, Q Developer may serve as an AI reviewer for code. When Agno generates new agent code, Amazon Q Developer’s models can inspect this code against best practices or known patterns, suggesting improvements or catching issues before the agent is finalized. This creates an iterative loop where initial code is refined either by AI or human developers with AI assistance, increasing reliability.
* **Orchestration and UI:** Amazon Q Developer provides a user interface and workflow engine that can trigger T‑Developer’s capabilities. For example, a developer using Amazon Q’s interface could input a high-level requirement and behind the scenes Q Developer will leverage the T‑Developer orchestrator to fulfill it. Q Developer might manage authentication, project context, or multi-step dialogues with the user, and delegate the heavy-lifting (planning, coding, testing) to T‑Developer’s agents. It essentially wraps T‑Developer in a more user-friendly front-end, making the meta-agent system accessible to developers who might not directly run CLI commands.

**Interaction with T‑Developer:** Amazon Q Developer and T‑Developer communicate through well-defined interfaces and shared resources: Q Developer can call T‑Developer’s CLI commands or API endpoints to initiate actions (classification, generation, deployment, etc.), and it can read results (logs, reports, generated code) to present back to users. Because Amazon Q Developer also orchestrates documentation and compliance, it uses the outputs of T‑Developer (like agent metadata, test results, deployment statuses) to update design docs or notify stakeholders.

In summary, Amazon Q Developer serves as the **bridge between the high-level design and the low-level implementation** within the T‑Developer ecosystem. It leverages the design documents to ensure everything is built to spec, and adds an extra layer of intelligence and user interaction above the T‑Developer core. By integrating Amazon Q Developer, the system benefits from AI-driven guidance and verification, making the autonomous development loop safer and more aligned with human intent.

### 2.4 Agent Core (AWS Bedrock)

**Role:** The Agent Core refers to the underlying AI and agent execution framework backing T‑Developer, built on **AWS Bedrock**. AWS Bedrock provides foundation model services (large language models and tools) which T‑Developer utilizes for the “intelligence” of its agents – such as natural language understanding, code generation, and decision making. In essence, AWS Bedrock is the platform that supplies the **cognitive capabilities** to T‑Developer’s agents.

**Components and Services:**

* **Foundation Models:** Many core agents (ClassifierAgent, PlannerAgent, EvaluatorAgent) rely on language models to perform their tasks. For example, the PlannerAgent likely uses an LLM to interpret a goal and break it into steps, and the EvaluatorAgent might use an LLM to reason about the quality of a plan or code. By using AWS Bedrock, T‑Developer can leverage models like Amazon Titan or other foundation models to power these agents. This integration means the heavy NLP or reasoning tasks are performed by scalable, managed AI services rather than local models.
* **AgentCore SDK:** The Agent Core includes an SDK (as indicated by internal repositories like *bedrock-agentcore-sdk-python*) that abstracts the Bedrock API for use in agents. This provides utilities for agents to easily call LLM completions, embeddings, or other AI operations. For instance, an agent can call `llm.complete(prompt)` via the Agent Core SDK, which under the hood calls an Amazon Bedrock model endpoint to get a result.
* **Decision Logic Framework:** Beyond raw AI calls, the Agent Core defines how agents structure their **decision loops** and handle state. It likely provides base classes (e.g., `Agent` class) that implement common functionality, hooking into Bedrock for any LLM-based decisions. It may also manage session context with Bedrock (for example, maintaining conversational context if needed by an agent that engages in multi-turn reasoning).

**Integration in T‑Developer:**

* The T‑Developer system delegates any non-trivial reasoning to the Bedrock-backed core. For example, when ClassifierAgent needs to determine if code is an “agent” or “tool,” it may use a Bedrock language model to analyze the code string and classify it, guided by few-shot prompts or Bedrock’s code understanding capabilities. Similarly, PlannerAgent can use a model to interpret requirements and formulate steps, which is facilitated by Bedrock’s text generation.
* By using AWS Bedrock, all AI computations are done within the AWS environment, ensuring **data security and compliance** (important for enterprise use). This avoids sending potentially sensitive code or requirements to external services – everything stays within Amazon’s managed service.
* The **Agent Core (Bedrock)** component also ensures consistency: all agents use a unified approach to call AI services. This means they can benefit from improvements at the Bedrock level (like model upgrades) without changing their high-level logic. It also means costs and performance can be centrally managed (e.g., using Bedrock’s features for scaling and monitoring model usage).

**Summary:** Agent Core (AWS Bedrock) is the substrate on which T‑Developer’s intelligent behavior runs. It provides the language understanding, reasoning, and generation capabilities that individual agents require, via a consistent API and managed infrastructure. By leveraging Bedrock, T‑Developer v1.1 can focus on orchestrating tasks and generating code, while relying on state-of-the-art AI models for the heavy lifting of intelligence.

### 2.5 User Interface Integrations (CLI & UI)

T‑Developer provides multiple integration points for developers to interact with the system: a command-line interface for direct control and a web-based UI (Agent UI Launcher) for visual interaction.

* **CLI (Command-Line Interface):** The CLI is the primary tool for developers during development and operations. It offers commands to perform most T‑Developer actions. For example:

  * Initializing new components: `tdev init agent --name MyAgent` to scaffold a new agent, or `tdev init tool ...` for a new tool.
  * Generating components with Agno: `tdev generate agent --goal "Describe task..."` triggers the auto-generation of an agent with the given goal.
  * Classifying components: `tdev classify path/to/code.py` runs the ClassifierAgent on a code file (used in CI to update metadata).
  * Testing components: `tdev test MyAgent` to run tests via the AgentTester/TestRunner agent.
  * Composing/running workflows: `tdev compose workflow.json` or `tdev run workflow-id` to execute a stored workflow definition.
  * Deployment: `tdev deploy --service-id <name> --target <env>` to deploy a composed service (workflow + agents) to a specified environment (lambda, ecs, local). Also `tdev status <service>` to check status, and `tdev rollback ...` as needed.

  The CLI ensures that developers can script and automate T‑Developer usage. It’s also what the CI/CD pipeline uses under the hood (via `tdev` commands in GitHub Actions scripts). The CLI integrates with the AgentRegistry and orchestrator directly – when a CLI command is run, it calls into the T‑Developer core library to perform the action, whether it’s local or triggering cloud operations.

* **Agent UI Launcher (Web UI):** T‑Developer includes a web-based interface that allows users to interact with agents and workflows in a more visual manner. Key features of the UI:

  * **Testing Agents:** A user can select an agent and provide input through a form, and the UI will invoke that agent (likely via an API call to a backend service running the orchestrator or agent) and show the output. This is useful for quick manual verification and demos.
  * **Workflow Visualization:** The UI can display workflows (as a sequence of steps or a graph) so the user can see which agents/tools are involved in accomplishing a goal. This helps in understanding and debugging the orchestrations that T‑Developer comes up with.
  * **Monitoring Deployed Services:** For agents or workflows that have been deployed as services, the UI can show their status, logs, and usage metrics. For example, if an agent is deployed to Lambda, the UI might show its last execution time, CloudWatch logs, and whether it’s active.
  * **Sharing Results:** The UI may allow users to share or save the outputs of agent runs or workflow executions – for collaboration or record-keeping.

  Under the hood, the UI communicates with T‑Developer’s backend via defined APIs (detailed in the API spec). It likely interacts with an API Gateway or direct calls to the orchestrator service to execute agents/workflows, and reads from data stores (DynamoDB, CloudWatch) for status and logs. The UI lowers the barrier to entry, letting less-technical users or stakeholders observe and trigger the system’s capabilities without using the CLI.

* **Future Integrations (IDE Plugins):** In addition to CLI and web UI, there are plans to integrate T‑Developer into IDEs like VS Code or AWS Cloud9. Potential features include generating agents from within the IDE (with Amazon Q’s assistance), visualizing workflows as you code, one-click deployments, and real-time feedback on agent quality or test results as you develop. These are forward-looking enhancements to further embed T‑Developer into the developer’s normal workflow.

By providing both CLI and UI, T‑Developer caters to different use cases: automation and scripting via CLI, and interactive exploration and monitoring via UI. Both interfaces are built on the same core functionalities and allow full control over the system, ensuring that developers can seamlessly adopt T‑Developer in various environments (terminal, browser, and eventually IDEs).

## 3. API Specification

This section defines the interfaces and data schemas through which various parts of T‑Developer communicate. We describe both **internal APIs** (between the orchestrator and agents/tools) and **external APIs** (between the T‑Developer system and user-facing frontends like the UI or external services). Both RESTful HTTP endpoints and event-driven interactions are considered, as appropriate.

### 3.1 Orchestrator External API (Frontend Interface)

The Orchestrator (MetaAgent) exposes an interface for clients (CLI, web UI, or Amazon Q Developer) to initiate workflows and get results. This can be implemented as a REST API or invoked via events. Key endpoints/actions include:

* **Submit Goal / Orchestrate:**
  **Endpoint:** `POST /api/orchestrate` (REST) or an equivalent event trigger (e.g., an AWS API Gateway -> Lambda event).
  **Input:** A JSON payload containing either:

  ```json
  { "goal": "Natural language description of desired outcome" }
  ```

  or a code snippet:

  ```json
  { "code": "<string of code to classify or use>" }
  ```

  Optionally, the request may include a user or project ID for context.
  **Behavior:** The orchestrator treats this as a new request. If `code` is provided, it will route to classification; if only `goal` is provided, it goes straight to planning. The orchestrator does not expect the client to specify which agents to use – it decides automatically.
  **Output:** A JSON with the final result of the orchestrated workflow. For example:

  ```json
  {
    "result": "<final output of the workflow>",
    "trace": [ /* optional execution trace or logs */ ]
  }
  ```

  If the workflow results in an artifact (like code for a new service), that might be provided as a link or reference. Errors are returned with appropriate HTTP error codes and messages.

* **Fetch Available Components:**
  **Endpoint:** `GET /api/agents` (and similarly `/api/tools`, `/api/teams`).
  **Description:** Returns the list of currently registered agents (or tools/teams) and their metadata. Useful for UI to display what building blocks exist.
  **Output:** JSON array of components, each with fields like name, type, description, etc. (see Agent Metadata Schema for field definitions).
  *(This is essentially a wrapper around the AgentRegistry’s get\_all or get\_by\_type functions.)*

* **Execute Specific Workflow:**
  **Endpoint:** `POST /api/workflows/{workflow_id}/execute`
  **Description:** Triggers execution of a predefined workflow by ID or name. The workflow must have been composed and saved previously.
  **Input:** A JSON of inputs required by the first step of the workflow. For example, if the workflow expects an input text, `{ "text": "hello world" }`.
  **Output:** Execution result JSON (similar to orchestrate output), possibly streaming logs or intermediate results if the client stays connected (alternatively, the API could immediately return a job ID and results are polled via another endpoint – but in initial design we assume synchronous execution for reasonably short workflows).

* **Deployment Requests:**
  **Endpoint:** `POST /api/deploy`
  **Description:** Deploys a composed service (workflow + agents) to a target environment.
  **Input:** JSON specifying the service/workflow to deploy and target environment, e.g.:

  ```json
  {
    "workflow_id": "policy-match-flow-v1",
    "service_id": "policy-matcher-v1",
    "target": "lambda",
    "strategy": "blue-green"
  }
  ```

  **Behavior:** The orchestrator (or a deployment agent) packages the specified workflow and its agents into a deployable artifact. It then triggers the deployment to AWS (Lambda, ECS, etc.) according to the target. This may be asynchronous – the API could return immediately with a status URL.
  **Output:** Deployment status or ID (and eventually the final status via another call or callback). For example:

  ```json
  { "status": "deploying", "service_id": "policy-matcher-v1", "deployment_id": "12345" }
  ```

  The system will later update the status (perhaps through WebSocket or polling an endpoint like `/api/services/{service_id}`) to “deployed” or “failed”, with additional info (like the AWS resource ARN).

* **Service Status & Logs:**
  **Endpoint:** `GET /api/services/{service_id}`
  **Description:** Retrieve status, configuration, and recent execution logs for a deployed service.
  **Output:** JSON including fields such as:

  ```json
  {
    "service_id": "policy-matcher-v1",
    "status": "active",
    "workflow_id": "clustered-match-flow",
    "agents": ["ScraperAgent", "ClusterAgent", "ChatAgent"],
    "deployment": {
      "type": "lambda",
      "region": "ap-northeast-2",
      "entrypoint": "handler.py::run"
    },
    "last_executed_at": "2025-07-22T06:20:31Z",
    "logs": [ /* recent log entries or link to CloudWatch */ ]
  }
  ```

  (This example mirrors the structure stored in DynamoDB for service instances.)
  The UI uses this to display service details and monitoring info.

### 3.2 Internal Agent APIs (Orchestrator <-> Agents Interfaces)

Within the system, the orchestrator and agents communicate via function calls or message-passing. Each core agent exposes a defined interface (method and data format) for the orchestrator to invoke. These can be thought of as internal APIs:

* **ClassifierAgent API:**
  *Method:* `classify(code: str) -> ClassificationResult`
  *Description:* Analyzes a given code snippet or file to determine its type (tool, agent, or team) and other metadata.
  *Input:* Source code (as text, or a reference to a file path).
  *Output:* A **ClassificationResult** object, which can be represented as JSON. For example:

  ```json
  {
    "component_type": "agent",
    "brain_count": 1,
    "reusability": "B",
    "name": "ExampleAgent",
    "description": "Short summary if extractable"
  }
  ```

  The output includes what category the component falls into and attributes like brain count and reusability tier. If the code already corresponds to a known pattern or if similar component exists, that can be noted. The orchestrator uses this result to decide next steps (e.g., store metadata in registry or avoid duplicate creation).

* **PlannerAgent API:**
  *Method:* `plan(goal: str or Spec) -> WorkflowPlan`
  *Description:* Decomposes a high-level goal or specification into a structured workflow (sequence of steps).
  *Input:* The goal can be a natural language string (e.g., “Build a tool that translates text to French and emails it”) or a structured spec object with fields like *input, output, constraints*. The PlannerAgent may also take into account a list of available components (fetched from the registry) as context.
  *Output:* A **WorkflowPlan** – essentially a JSON or YAML defining the workflow. For example:

  ```json
  {
    "steps": [
      { "agent": "TranslatorAgent", "input": "{user_text}" },
      { "agent": "EmailSenderAgent", "input": "{translation}" }
    ]
  }
  ```

  Each step references an agent/tool by name and describes how data flows (here, user\_text goes into TranslatorAgent, its output “translation” goes into EmailSenderAgent). The plan may also include metadata like an ID for the workflow, optional branching, or parallelism info. The output of PlannerAgent is critical – it’s basically the program that the orchestrator will execute.

* **EvaluatorAgent API:**
  *Method:* `evaluate(subject: WorkflowPlan or AgentCode) -> EvaluationResult`
  *Description:* Assesses the quality of a workflow plan (or possibly newly generated agent code) and provides a score and feedback.
  *Input:* Typically a WorkflowPlan (the output of PlannerAgent). Could also accept agent source code for reviewing an individual agent.
  *Output:* An **EvaluationResult** which might look like:

  ```json
  {
    "score": 91,
    "rating": "A-",
    "suggestions": [
      "The TranslatorAgent might fail on very long text, consider adding a chunking step.",
      "Add an error handling step if email fails."
    ]
  }
  ```

  The score is a numeric value (e.g., 0–100) indicating overall quality. Suggestions list potential improvements or issues. The EvaluatorAgent uses predefined criteria and possibly ML models to judge efficiency, robustness, and correctness. This feedback can be used by the orchestrator; for instance, if the score is below a threshold (say 85%), the orchestrator might invoke the PlannerAgent again with these suggestions (refinement loop). If above threshold, the plan is accepted and execution proceeds.

* **WorkflowExecutorAgent API:**
  *Method:* `execute(workflow: WorkflowPlan, inputs: dict) -> ExecutionResult`
  *Description:* Executes a given workflow step by step, invoking each specified agent/tool in turn and managing data flow.
  *Input:* A workflow definition (as produced by Planner/Evaluator) and the initial input data required for the first step. The executor also has access to the AgentRegistry to instantiate and call each agent in the plan.
  *Output:* An **ExecutionResult** containing the final output of the workflow and optionally a trace of intermediate results or any errors encountered. For example:

  ```json
  {
    "output": "Email sent to user@example.com",
    "trace": [
      { "step": 1, "agent": "TranslatorAgent", "output": "Bonjour le monde" },
      { "step": 2, "agent": "EmailSenderAgent", "output": "Success: message_id=..."}
    ]
  }
  ```

  The WorkflowExecutorAgent ensures that each agent’s output is passed as input to the next, handling any format transformations needed between steps. It also records logs or state from each step (which can be stored or returned).

* **AutoAgentComposer (Agno) API:**
  *Method:* `generate(spec: AgentSpec) -> {code: str, metadata: dict}`
  *Description:* (This is partly an internal and partly a user-facing API via CLI.) Given a specification for a new agent/tool, generate its code and metadata.
  *Input:* The AgentSpec can be:

  * **Natural language prompt** (string describing the desired agent).
  * **Structured JSON** detailing fields like `goal`, `input`, `output`, and optionally `tools` to utilize.
    *Output:* The newly created component in two forms:
  * **Code** – e.g., a Python function or class definition as a string (or as a file in the repository).
  * **Metadata** – a JSON object describing the agent (name, type, input, output, list of internal tools, etc.).
    Additionally, the component is automatically registered in the system. If this API is called via CLI, the code might be written to a local file and the metadata added to registry; if called at runtime by orchestrator, it exists in memory/DB. The orchestrator can then use the new agent immediately.
    Example output metadata:

  ```json
  {
    "name": "QRCodeResolverAgent",
    "type": "agent",
    "brain_count": 1,
    "reusability": "B",
    "input": "image",
    "output": "username",
    "tools": ["QRCodeReaderTool", "UserDBLookupTool"]
  }
  ```

  (This example corresponds to an agent that reads a QR code and looks up a user, as in Agno documentation.)

* **AgentRegistry API:** Although not an agent, the registry exposes a programmatic interface used by the orchestrator and agents:

  * `register(name: str, metadata: dict)`: Add a new component to the registry with its metadata.
  * `unregister(name: str)`: Remove a component (for deprecation or cleanup).
  * `get_instance(name: str) -> object`: Return an instance of the agent/tool class, ready to use (this dynamically imports the class and constructs it).
  * `get_all() -> dict`: Return all registry entries.
  * `get_by_type(type: str) -> list`: List all components of a given type (agent/tool/team).

  These functions aren’t REST endpoints but are invoked within the application. For instance, the PlannerAgent uses `get_by_type("agent")` to retrieve candidates for planning, and the WorkflowExecutorAgent uses `get_instance(name)` to load each agent at runtime.

### 3.3 Data Schemas and Formats

Throughout these APIs, T‑Developer uses structured data to represent components and workflows:

* **Agent/Tool Metadata Schema:** (Detailed in the Agent Metadata Schema document). In API terms, whenever an agent or tool is referenced (by name), the system can provide its metadata. The metadata includes fields like `name`, `type`, `description`, `input_schema`, `output_schema`, etc. For example, a tool’s metadata might specify input/output parameter types, which the PlannerAgent might use to ensure compatibility when chaining steps. When returning data via API (e.g., `GET /api/agents`), these metadata objects are serialized to JSON.

* **Workflow Definition Schema:** A workflow is typically represented as a JSON structure with an ordered list of steps. Each **step** may contain:

  * `agent`: The name (and optionally version) of the agent/tool to run.
  * `inputs`: Mapping of this step’s input parameters to either constants or outputs of previous steps (some format like referencing by step number or variable name).
  * (Optional) `outputs`: What to name the outputs of this step, to reference later.
  * (Optional) control flow info like `if` conditions or parallel branches (for future extension).

  In simple form:

  ```json
  {
    "id": "workflow-name-v1",
    "steps": [
      { "id": "step1", "agent": "XAgent", "input": { "param": "value or ${prev_step.output}" } },
      { "id": "step2", "agent": "YTool", "input": { "data": "${step1.result}" } }
    ]
  }
  ```

  The API will exchange workflows in this form. The Planner outputs it, the Evaluator reads/writes it (possibly annotating suggestions), and the Executor reads it.

* **Execution Logs/Trace Schema:** When returning traces or logs via APIs (like ExecutionResult or service logs), a standardized format is used. Each entry might include timestamp, step or component name, log level, and message. For trace included in an ExecutionResult, a simplified array of step results (as shown earlier) is used. For more extensive logs, the API might provide a pre-signed URL or reference to CloudWatch logs rather than raw log text.

* **Event-driven Interfaces:** In addition to REST, the system uses events:

  * *CI/CD events:* e.g., a git push triggers a GitHub Actions workflow, which in turn calls `tdev classify`, `tdev test`, etc. These are essentially command-line invocations (see the CI/CD document for YAML example), but conceptually, one could imagine an EventBridge event or SNS message triggering classification in a more cloud-native way. (Future iterations might have an event like “NewAgentAdded” that automatically triggers classification and test runs.)
  * *Slack notifications:* Not exactly an API, but the system calls out via a script or webhook to Slack after pipeline runs. The format is a message summarizing results (e.g., ✅ tests passed, 🧠 Evaluator score, 🚀 deployment success). This ensures humans are in the loop on important events.
  * *Agent-to-Agent communication:* Currently orchestrated by the orchestrator (agents don’t call each other directly except through workflows). However, if in the future agents were to emit events (e.g., an agent could push an event that triggers another agent in a reactive pattern), a lightweight pub/sub could be used. For now, direct calls via the orchestrator suffice.

Every interface in T‑Developer is designed with clarity and structure, often relying on JSON as the medium of exchange, making it compatible with Amazon Q Developer and other tools. The use of standardized schemas for metadata and workflows ensures that all components interpret data consistently. This API specification, while abstract in places (since some “APIs” are internal function calls), outlines how the system’s pieces interconnect and how external systems can drive T‑Developer’s powerful capabilities.

## 4. CI/CD Pipeline Design

T‑Developer v1.1 is tightly integrated with Continuous Integration and Continuous Deployment processes to automate quality assurance and deployment of the agents and workflows it creates. This section describes the CI/CD pipeline, using GitHub Actions as an example implementation (as in our current setup), and notes how AWS CodePipeline could provide similar functionality. The pipeline covers everything from code commit to automated testing, evaluation, and deployment.

### 4.1 Pipeline Overview and Triggers

The CI/CD pipeline is triggered on relevant version control events – for instance, when a pull request is opened or updated, or when code is pushed to the main branch. In GitHub, we configure Actions to run on PRs. For AWS CodePipeline, a source stage picking up repository changes would play a similar role.

Once triggered, the pipeline proceeds through several **stages** to ensure the integrity and quality of the T‑Developer components:

1. **Classification Stage:** Use the T‑Developer CLI to classify new or changed components. For example, run `tdev classify ./agents/**/*.py` across the repository. This invokes the ClassifierAgent on each new/modified agent or tool code file, updating their metadata in the AgentRegistry. This step ensures the registry stays current (with brain\_count, type, etc.) and catches any structural issues in the code early.
2. **Testing Stage:** Run automated tests for all components. Using `tdev test all` (or similar) will execute the TestRunner/AgentTester on the entire suite. Unit tests for each agent/tool are run, and basic integration tests (like executing simple workflows) can also be included. This stage verifies that the components behave as expected and that no regressions were introduced. Failures here will block the pipeline.
3. **Evaluation Stage:** Invoke the EvaluatorAgent on workflows to assess their quality. The CLI command `tdev evaluate ./workflows/*.json` will have the EvaluatorAgent score each workflow definition. Alternatively, Evaluator could also review new agent code for complexity or style. This stage produces a quality score and perhaps fails the pipeline if the score is below a threshold (e.g., <85/100). It acts as an **automated quality gate** beyond just tests.
4. **Security Scan Stage (if integrated):** Although not explicitly shown in the snippet, a best-practice pipeline would include static code analysis, dependency vulnerability scanning, etc. (For example, use CodeQL or Bandit for Python.) T‑Developer’s pipeline ensures that **no security vulnerabilities** are detected before deployment. In CodePipeline, this could be a Lambda or CodeBuild stage running security tests. If any high-severity issues are found, the pipeline fails.
5. **Notification Stage:** Aggregate results from the above steps and notify stakeholders. In GitHub, this can be done via PR comments or commit status checks (pass/fail). Additionally, Slack notifications are sent to a team channel with a summary. For example, a Slack message might be:

   > 📦 New Agent: `SummarizerAgent` classified as **agent**
   > ✅ Tests passed (3/3)
   > 🧠 Evaluator Score: 91 (A-)
   > 🚀 Deployed to Lambda: arn\:aws\:lambda:...
   > This informs the team in real-time of the CI outcomes and any deployment.
6. **Deployment Stage:** If all previous gates pass (classification/test/evaluation success, and optionally code review approvals), the pipeline proceeds to deployment. This may be automated for certain branches (e.g., auto-deploy to a dev/test environment on merge to main, or to production on a tag). Using `tdev deploy ...`, the pipeline will package and deploy the updated service. For instance, updating an agent might trigger redeployment of any services that use that agent. In GitHub Actions, a step can assume an AWS role and run deployment commands (or call CodeDeploy). In CodePipeline, separate deploy stages to AWS Lambda/ECS are configured.

Throughout these stages, **artifacts** like test reports or generated code can be archived. For example, test results could be stored in a DynamoDB TestRunHistory table and also exposed in the pipeline summary. This history can feed into the EvaluatorAgent for trend analysis (ensuring quality is improving over time).

### 4.2 Example GitHub Actions Workflow

Below is a simplified example of a GitHub Actions workflow implementing the above stages (from our configuration):

```yaml
name: T-Dev CI
on: [pull_request]
jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
      - name: Classify Components
        run: tdev classify "./**/*.py"       # Step 1: Classification:contentReference[oaicite:110]{index=110}
      - name: Run Unit Tests
        run: tdev test all                   # Step 2: Testing:contentReference[oaicite:111]{index=111}
      - name: Evaluate Workflows
        run: tdev evaluate ./workflows/*.json  # Step 3: Evaluation:contentReference[oaicite:112]{index=112}
      - name: Security Scan
        run: bandit -r tdev/agents           # Step 4: Static security analysis (example)
      - name: Deploy to AWS (Dev)
        if: ${{ success() && github.ref == 'refs/heads/main' }}
        run: tdev deploy --service-id myservice-v2 --target lambda
      - name: Notify Slack
        if: ${{ always() }}
        run: ./scripts/slack_notify.sh "Pipeline result: $STATUS"  # Step 5: Notification:contentReference[oaicite:113]{index=113}
```

Key things to note:

* The `if: success()` condition ensures deployment only runs if earlier steps succeeded and we are on the main branch. This prevents deploying code that hasn’t passed tests or that is just in a PR review. We often gate production deployment behind manual approval (described below).
* The Slack notification runs `always()` to send a message even if earlier steps fail, so that a failure triggers an alert.

### 4.3 Quality Gates and Approvals

The CI/CD pipeline incorporates multiple **quality gates** to ensure only high-quality agents and workflows get deployed. These include:

* **Automated Gates:** Test pass rate must be 100%. Evaluator score must exceed a threshold (e.g., 85). Security scan must have 0 critical issues. If any of these conditions aren’t met, the pipeline stops and marks the build as failed.
* **Manual Approval Options:** For critical services or production deployment, an extra human approval can be required even if all automated checks pass. For example, using GitHub’s review system – the PR must be approved by a tech lead before merge. In an AWS CodePipeline, one can insert a Manual Approval action before the deploy stage. We also envision Slack-based approvals (e.g., a Slack message with “Approve” button) as an extension.
* **Environmental Promotion:** The pipeline could deploy to a staging environment automatically, but require manual promotion to production. This allows testing the deployed agents in a safe environment. For instance, after a successful deployment to a “dev” Lambda, a team member triggers promotion to “prod” via a CLI or UI command, or by approving a CodePipeline prompt.

These measures ensure that T‑Developer’s autonomous generation is kept in check by rigorous testing and oversight, aligning with DevSecOps best practices.

### 4.4 Deployment Automation

When the pipeline reaches deployment, the process differs slightly based on target:

* **AWS Lambda Deployment:** The pipeline uses the CLI or AWS SDK to package the service code into a zip, upload to S3, and update/create a Lambda function. The memory/timeout and other settings might be configured via parameters or included in the package. This is ideal for event-driven, stateless services – which many agent workflows are, since they execute and return a result without persistent state.
* **AWS ECS (Docker) Deployment:** For long-running or more complex services, the pipeline builds a Docker image containing the T‑Developer runtime and the specific agents/workflow for the service. It then pushes to Amazon ECR and updates an ECS service (perhaps a Fargate task). This is suited for services that need to maintain state in memory or handle continuous traffic beyond the short duration allowed by Lambda.
* **Local/Development Deployment:** In CI, this isn’t applicable, but developers can use `tdev deploy --target local` to register the service on their local machine for testing. The pipeline documentation notes this mainly for dev/test use.

Each deployed service is recorded in a **Service Instance Metadata store** (DynamoDB) with details like service ID, version, and deployment type. The pipeline is responsible for updating this record post-deployment (for instance, after deploying, it might call `tdev status service-id` or an API to confirm and log the new deployment ARN).

### 4.5 AWS CodePipeline Consideration

If using AWS CodePipeline instead of GitHub Actions, the structure remains similar:

* A **Source stage** hooked to CodeCommit or GitHub triggers on changes.
* A **Build/Test stage** (using CodeBuild) runs a buildspec that essentially executes the same steps: install dependencies, run `tdev classify`, `tdev test`, `tdev evaluate`. Logs from CodeBuild can be sent to CloudWatch for analysis.
* An **Approval stage** (optional) can pause the pipeline for a human to review results.
* A **Deploy stage** uses CloudFormation or CodeDeploy to push the Lambda or ECS changes (we could have a CloudFormation template for deploying an agent service, which gets parameters like S3 artifact or image URI). Alternatively, CodeBuild can assume a role and run our CLI deploy commands directly.

Using CodePipeline could be beneficial for deeper AWS integration (IAM-managed, visible in AWS console, etc.), but the logic remains aligned with what’s described for GitHub Actions.

### 4.6 Pipeline Output and Feedback

As pipeline runs are completed, results feed back into the development cycle:

* Developers are notified immediately of failures (with logs to diagnose, e.g., test failure output or evaluation suggestions). This allows quick iteration on improving the agent or workflow.
* The EvaluatorAgent’s score provides a quantitative metric for improvements. If an agent’s score is low, developers (or Amazon Q Developer’s AI) might revisit the design or let Agno refine the code.
* The historical data of pipeline runs (tests and scores stored in the TestRunHistory and possibly version control tags) can be mined to see progress over time and ensure that adding new capabilities doesn’t degrade existing ones (e.g., ensuring no regressions).
* By automating deployment on successful passes, T‑Developer shortens the cycle from code generation to having that code live in a cloud environment where it can be further tested or used by end users. This rapid deployment ability is crucial for an AI-driven development system – it enables quick feedback from real executions.

In summary, the CI/CD pipeline of T‑Developer v1.1 is designed to catch issues early, enforce quality standards, and speed up the delivery of new AI-generated capabilities. It transforms what could be risky (AI writing code) into a controlled process where every change is validated by tests and evaluations. Through integration with popular tools like GitHub Actions (and extendable to CodePipeline), it fits naturally into modern DevSecOps workflows, providing confidence that T‑Developer’s autonomous agents are reliable and secure before they go live.

## 5. Agent Metadata Schema

The Agent Metadata Schema defines how agents (and other components like tools and teams) are described and stored in the T‑Developer **AgentRegistry**. Every agent has an associated metadata record capturing its identity, purpose, interfaces, and relationships. This structured metadata is crucial for discovery (so the Planner can find appropriate agents), for correctness (making sure inputs/outputs align when composing workflows), and for governance (tracking versions, owners, etc.). Below we outline the schema fields for an agent’s metadata and provide an example.

### 5.1 Metadata Fields for Agents

Each agent’s metadata is a JSON object with the following key fields:

* **`name`** (string): The unique identifier of the agent. Typically a descriptive name in CamelCase (e.g., `"SummarizerAgent"`). This name is used as the key in the AgentRegistry and how other components refer to the agent.
* **`type`** (string): The component type. For agents, this is always `"agent"`. (Tools would have `"tool"`, teams `"team"`.)
* **`description`** (string): A human-readable description of the agent’s purpose. This should briefly state what the agent does. For example: `"Agent that summarizes text using an LLM"`. This helps developers (and AI planners) understand when to use this agent.
* \*\*`class_path``** (string): The Python import path for the agent’s implementation class or function:contentReference[oaicite:130]{index=130}:contentReference[oaicite:131]{index=131}. For instance, `"tdev.agents.summarizer.SummarizerAgent"`. This allows the registry to dynamically load the agent code. (In some contexts, the field is just called `"class"\`).
* **`brain_count`** (integer): Number of decision points in the agent. By definition this is 1 for an agent (since an agent has a single decision loop), but still stored for completeness and for distinguishing from tools (0) or teams (2+). It might also be used in planning to gauge complexity.
* **`reusability`** (string): The reuse tier or category of the agent. In T‑Developer’s convention, “A” means highly reusable (typically tools), “B” for standard agents, “C” or lower for more specialized or less reusable components. This field can guide the Planner to prefer more reusable agents when possible.
* **`input_schema`** (object): A schema defining the expected input for the agent. This can be a simple description or a JSON Schema. At minimum it could include a type or description of the input data (e.g., `"string"` or a structured object). If the agent takes multiple inputs, this schema enumerates them. For example:

  ```json
  "input_schema": {
      "text": "string"
  }
  ```

  might indicate the agent expects a text string input. This helps validate at composition time that upstream outputs match this format.
* **`output_schema`** (object): A schema for the agent’s output. Similar to input\_schema, it defines the type/structure of what the agent returns. E.g., `{"summary": "string"}` for a summarizer. This allows the Planner to chain outputs to inputs (the Planner will match, for example, that one agent’s output “summary” can feed into another expecting a “text” input). If the output is a simple scalar or string, a shorthand can be used.
* **`tools`** (array of strings, optional): The list of internal tools (or even other agents) that this agent uses in its implementation. This is especially relevant for agents that orchestrate tools. For example, an agent that translates text might list `["TranslatorTool"]` if internally it calls that tool. This field is automatically populated by the ClassifierAgent or Agno when analyzing code. It’s useful for understanding dependencies and for the registry to know relationships (e.g., could auto-generate an agent->tool dependency graph).
* **`tags`** (array of strings, optional): Keywords or categories for easier searching and grouping of agents. For instance, tags might include domains (`"NLP", "finance"`) or capabilities (`"generator", "crawler"`). Tags help both developers and AI components filter agents by context.
* **`version`** (string or object, optional): The version of the agent. This might appear as `"version": "1.0.0"` following semantic versioning. In the registry JSON, versions might be managed differently (see below), but including a version here indicates the version of this metadata/implementation. The system uses semantic versioning for code changes and simple numeric versions for references in workflows.
* **`path`** (string, optional): Storage location of the agent’s code, if applicable. For example, if code is stored on S3 or Git, this could be an S3 URI (`"s3://tdev-codebase/agents/AgentName.py"`). In local development, this might not be needed (the class\_path suffices), but in a distributed system, it’s useful to pinpoint where the code lives.
* **`author`** / **`owner`** (string, optional): The creator or maintainer of the agent. Not mentioned in earlier docs, but likely a field to consider for organizational use (could be a username or team name).
* **`created_at`** (timestamp, optional): When the agent was created (or last updated). Useful for auditing and cleanup of stale components.
* **`status`** (string, optional): e.g., “stable”, “experimental”, “deprecated” to indicate readiness for use. Newly generated agents might start as “experimental” until they pass certain quality gates.

For **Tool** metadata, many fields overlap but differ slightly:

* `brain_count` = 0 always.
* `reusability` = "A" (high) for tools.
* Tools typically have no internal `tools` list (they don’t use other tools, they are atomic), and might have a simpler `class_path` (could be a function).
* Input/output schema are very important for tools (since they are functional).
  Teams would have `brain_count >= 2`, and might have a list of member agents instead of tools.

### 5.2 Registry Storage Format

In the actual AgentRegistry (which may be a JSON file `.tdev/registry.json` in local mode, or stored in DynamoDB in cloud mode), the metadata is stored under the agent’s name as key. For example:

```json
{
  "EchoAgent": {
    "type": "agent",
    "class": "tdev.agents.echo_agent.EchoAgent",
    "brain_count": 1,
    "reusability": "B"
  },
  "EchoTool": {
    "type": "tool",
    "class": "tdev.tools.echo_tool.echo_tool",
    "brain_count": 0,
    "reusability": "A"
  }
}
```



This sample shows a minimal set of fields – in practice, we would also see `description`, schemas, etc., if they were provided. The registry focuses on essential info needed at runtime (type, class path) and may omit some developer-facing fields (like input/output descriptions) to keep it lightweight. However, a more complete registry entry would be:

```json
"SummarizerAgent": {
  "type": "agent",
  "class": "tdev.agents.summarizer.SummarizerAgent",
  "brain_count": 1,
  "reusability": "B",
  "description": "Agent that summarizes text using an LLM",
  "input_schema": { "text": "string" },
  "output_schema": { "summary": "string" },
  "tools": ["GPTCallerTool"],
  "tags": ["NLP", "summarization"],
  "version": "1.0.0"
}
```

This is not a direct excerpt but a representative structure combining details from various docs (Agents guide, Tool spec, etc.).

In DynamoDB (cloud mode), the structure might be slightly different to allow multiple versions. The **Versioning and Change Control** document indicates that the registry can store multiple versions of each agent under a versions list. For example:

```json
{
  "name": "SummarizerAgent",
  "versions": [
    {
      "id": "v1",
      "path": "s3://.../summarizer_v1.py",
      "created": "2024-11-01",
      "status": "stable",
      "description": "Basic summarizer based on GPT-3.5"
    },
    {
      "id": "v2",
      "path": "s3://.../summarizer_v2.py",
      "status": "experimental",
      "description": "Long-document summarizer using GPT-4"
    }
  ]
}
```



In this schema, top-level `name` is separate and each version has its own metadata subset. The AgentRegistry API would then resolve a default (like the latest stable version) unless a specific version is requested. For the scope of this document, we’ll focus on single-version metadata as that’s how v1.1 primarily operates (with versioning being an emerging feature).

### 5.3 Example: QRCodeResolverAgent Metadata

To solidify, consider the **QRCodeResolverAgent** that Agno generated in a prior example. Its metadata as created by Agno was:

```json
{
  "name": "QRCodeResolverAgent",
  "type": "agent",
  "brain_count": 1,
  "reusability": "B",
  "input": "image",
  "output": "username",
  "tools": ["QRCodeReaderTool", "UserDBLookupTool"],
  "path": "s3://tdev/agents/qr_resolver.py",
  "class": "agents.qr_resolver.QRCodeResolverAgent"
}
```



A few notes on this:

* The schema uses `"input": "image"` as shorthand for input type, and `"output": "username"` for output type. In many cases, we translate that into input\_schema/output\_schema for consistency (e.g., input could be `{ "image": "ImageData" }` or similar). But Agno’s quick metadata here is capturing the essence: it takes an image and produces a username.
* The `tools` array clearly lists it depends on two tools (one to read QR codes, one to look up in a user database).
* The `path` and `class` indicate where the code lives and how to import it. This agent presumably was saved to S3 (since this might have been generated outside of a local filesystem).
* It doesn’t explicitly list `description` or `tags` here, but ideally one would add `"description": "Agent that scans a QR image and returns the associated username"` for completeness, and perhaps a tag like `"ComputerVision"`.

### 5.4 Usage of Metadata

* **During Planning:** The PlannerAgent queries the registry for agents that have certain capabilities. It might filter by tags or by checking input/output schemas. For example, if a step needs something that outputs a "username", it can look for any agent or tool whose output\_schema matches that (e.g., QRCodeResolverAgent above would match).
* **During Execution:** The WorkflowExecutorAgent uses the metadata to instantiate the agent classes. It looks up by name, gets the class path, and loads the class to create an object. It might also use metadata like input\_schema to format inputs properly (though usually that’s handled by the orchestrator logic).
* **In the UI/Documentation:** The metadata feeds into documentation (like listing all agents and their descriptions) and UIs where you might choose an agent by name to run. The Agent UI Launcher can display an agent’s expected input fields by reading input\_schema and can show a tooltip from description. This makes the system more transparent.
* **Maintenance:** With metadata in a structured form, one can easily build tooling around it – e.g., find all agents that use a deprecated tool, or all components authored by a certain person, etc.

The agent metadata schema thus acts as a **contract** for each agent’s capabilities and requirements. By rigorously defining these fields and storing them in a central registry, T‑Developer ensures that automated composition (by Planner/Evaluator) and execution can happen reliably. It also aids Amazon Q Developer or any other consumer in reasoning about the system’s components. All new agents/tools must have a metadata record (generated automatically by classification or provided by developers), ensuring nothing becomes a black box in the orchestration process.

## 6. IAM and Security Policy Guide

Security is paramount in T‑Developer’s design, given its ability to execute code, deploy services, and access various resources. This guide outlines the Identity and Access Management (IAM) roles, permissions, and general security practices employed by T‑Developer v1.1. It covers how agents and services are permissioned, how Amazon Q Developer’s interactions are secured, and what policies govern deployment targets.

### 6.1 IAM Roles for Agents and Services

Each deployed agent or composed service in AWS runs under a specific IAM role following the **principle of least privilege**. This means:

* When T‑Developer deploys a workflow to AWS Lambda, it creates or uses an IAM **execution role** for that Lambda function. This role’s policy only allows the minimal actions that the function’s agents/tools need. For example, if the service uses an S3UploaderTool, the role will have permission only to `PutObject` on the specific S3 bucket needed – and nothing more.
* Similarly, for ECS deployments, each task runs under a task role with limited access (for instance, access to only certain secrets or APIs required by the agents).
* These roles are defined either via templated policies or (in future) via an automated analysis of the agent’s code. A planned enhancement is **automatic IAM policy generation**: T‑Developer will inspect what AWS SDK calls a generated agent might make and suggest an IAM policy allowing those and no others. This ensures even AI-generated code doesn’t accidentally get more access than necessary.

For the T‑Developer orchestrator itself (if running in AWS), a separate IAM role is used which allows it to coordinate the system:

* The orchestrator’s role might need broad read access to the DynamoDB tables (AgentRegistry, WorkflowStore, etc.), permission to invoke Lambda (to trigger agent execution or deployment tasks), and perhaps to write to CloudWatch Logs and Metrics (for logging and monitoring).
* If Amazon Q Developer calls T‑Developer via an API Gateway + Lambda, that Lambda (which hosts orchestrator logic) has an IAM role with these orchestrator permissions.

**Agent vs Service Roles:** There is a distinction between *development-time roles* and *runtime roles*:

* Development/CI roles: For example, the GitHub Actions runner or CodePipeline uses an IAM role to deploy resources. That role must have rights to create/update Lambda functions, ECS services, CloudWatch logs, etc. This is a highly privileged role but only used in the context of deployment automation.
* Runtime roles: As described, each runtime component (Lambda function for an agent service, ECS task) has a tightly scoped role (e.g., no ability to create new resources, only to use what’s needed for functioning).

### 6.2 Secrets Management

T‑Developer integrates with AWS Secrets Manager (and Parameter Store) to handle API keys and other sensitive information. Key practices include:

* **No Hard-Coded Secrets:** Agents or tools that require credentials (for example, a GitHubTool needing a token, or a DB access string) do not have them in code or config. Instead, they reference a secret by name. At deployment, the Lambda or container is given access to that secret via IAM policy (Secrets Manager uses resource-based policies and IAM conditions to allow specific principals to fetch certain secrets).
* **Secure Retrieval:** When an agent runs that needs a secret, it calls a utility (possibly provided by the Agent Core SDK) to retrieve it from Secrets Manager. This fetch is encrypted in transit and the secret is decrypted only in memory.
* **No Logging of Secrets:** Agents are written to avoid printing secrets. T‑Developer’s logging guidelines and the EvaluatorAgent’s checks include ensuring that no sensitive info appears in logs or Slack notifications. For instance, if an agent does fail due to an auth error, the error message would be generic and not include the actual key.
* **Rotation:** Although not automated in v1.1, integrating AWS Secrets Manager’s rotation policies or providing a manual way to update secrets without changing code is recommended.

By centralizing secrets, we ensure that if Amazon Q Developer or any user wants to, say, rotate an API key, they can update it in one place rather than editing agent code.

### 6.3 Access Control and Multi-Tenancy

If T‑Developer is used by multiple users or teams (multi-tenant scenario, e.g., in Amazon Q’s context), we implement access control:

* Each user might have an isolated `.tdev` environment or namespace in the AgentRegistry and WorkflowStore, such that they can only see and deploy their own agents. IAM roles could be parameterized by user/project, limiting data access.
* Amazon Q Developer likely authenticates the user and then communicates with T‑Developer’s API using the user’s identity or a scoped token. The system should verify this token and ensure the user is authorized to perform the requested action (e.g., only a project owner can deploy a service for that project).
* Actions like generating code or deploying might be logged with the user’s ID for audit trail.

### 6.4 Security in the CI/CD Pipeline

The pipeline has built-in security measures:

* **Quality Gates for Security:** The pipeline does not proceed to deployment if any security test fails. This includes static analysis (looking for dangerous code patterns), dependency vulnerability scans, and ensuring no secrets are accidentally included in the code. The EvaluatorAgent is also tasked to consider security in its scoring rubric – e.g., flag if an agent uses an API call without proper error handling or if a tool writes to disk unsafely.
* **Approval for Sensitive Deployments:** As noted, manual approval can be required for production. Only specific privileged users (e.g., a lead or SRE) can approve those stages. This reduces the chance that a malicious or flawed AI-generated code gets deployed widely without a human glance.
* **Principle of Least Privilege for Pipeline:** The CI runner itself (whether GitHub or CodePipeline) runs under limited permissions. For example, if using OIDC to assume an AWS role, that role only allows specific actions needed (deploying to certain resources). We avoid using overly broad credentials in CI.

### 6.5 Monitoring and Audit

All actions and changes in T‑Developer are logged for auditability:

* **Deployment Logs:** Every deployment (automated or manual) is recorded with who triggered it and when. For example, CloudTrail logs for the AWS API calls, or internal logs that note “Deployed Service X version Y by user Z”.
* **Agent Changes:** Because agents and workflows are version-controlled (in Git), we have an audit trail of changes. Additionally, the system could log whenever an agent is generated by Agno or removed from the registry.
* **CloudWatch Alarms:** For deployed services, CloudWatch Metrics and Alarms can be set (e.g., if a service errors out or exceeds certain usage, it triggers an SNS notification). Security alarms (like multiple failures possibly indicating misuse) could notify administrators.
* **Audit Trail in Registry:** The AgentRegistry or a parallel log keeps track of important events: agent created, updated, promoted to stable, deprecated. This is important in case we need to investigate an incident (e.g., “who authorized creation of this agent that opened up an S3 bucket globally?”).

### 6.6 Compliance and Best Practices

T‑Developer’s design follows general cloud security best practices:

* **Least Privilege:** Already discussed for IAM – agents get minimal permissions. Also internally, the orchestrator only has access to what it needs (for instance, if the orchestrator doesn’t need to directly query a customer database, it won’t have credentials for it).
* **Isolation:** If an agent runs untrusted code (maybe code generation could theoretically produce unsafe code), it’s run in sandboxed environments (the Lambda or container). Resource limits (memory, timeout) and possibly deterministic execution flags are used to prevent runaway processes or abuse.
* **Data Encryption:** Any data at rest, such as agent code stored in S3 or metadata in DynamoDB, is encrypted at rest by AWS (KMS-managed keys, etc.). In transit, all communication uses HTTPS (API calls, etc.). There’s no transmission of sensitive data in plaintext.
* **Secrets Handling:** As noted, Secrets Manager is used and access to it is controlled via IAM. Only the roles that need a given secret have decrypt privileges, and those secrets are not shared broadly.
* **No Personal Data in Logs:** If agents process user data (for example, if used in a customer support scenario), we ensure logs and metadata do not inadvertently store personal data. Logs may contain IDs or references, but sensitive content can be filtered or redacted.
* **Periodic Reviews:** The security configuration (IAM policies, open ports on containers, etc.) should be periodically reviewed. As T‑Developer evolves, new agents that interact with different services might require updated policies, which should go through a security review phase.

By implementing the above, T‑Developer aims to be secure by design even as it generates new code and makes changes automatically. **Amazon Q Developer’s environment** adds an extra layer: since Q Developer will orchestrate and possibly generate parts of the system, its access to T‑Developer is also controlled. For instance, Q Developer might have an IAM role that can invoke the orchestrator’s APIs but not directly manipulate infrastructure, ensuring a clear separation of concerns and audit trails for what Q Developer triggers.

In conclusion, security in T‑Developer v1.1 is enforced at multiple layers – code, pipeline, deployment – to mitigate risks inherent in automated code generation and execution. IAM roles confine what each part can do, secrets are properly managed, and strong oversight (automated and human) is in place for any critical actions. This ensures that while T‑Developer brings agility and automation, it does not compromise on the safety and compliance expected in an enterprise environment.

## 7. Testing Strategy

Testing is crucial in T‑Developer’s pipeline to guarantee that both human-written and AI-generated components behave correctly and reliably. The testing strategy for T‑Developer v1.1 spans multiple levels: from unit tests for individual tools/agents, to integration tests for workflows, to automated evaluations using AI (the EvaluatorAgent acting as a “QA engineer”). This section outlines how tests are created and executed, and how the system ensures quality through testing.

### 7.1 Unit Testing of Agents and Tools

Every agent and tool should have associated unit tests that validate its core functionality in isolation. The process is as follows:

* **Test Generation:** For AI-generated agents, T‑Developer will in future auto-generate basic test cases. Even in v1.1, after Agno creates a new agent, a developer or Amazon Q Developer could supply a simple test input and expected output (if known). For example, if a TranslatorAgent was generated, a test might feed `"hello"` and expect `"bonjour"` (if using a deterministic mapping for test purposes).
* **Manual Tests:** Developers can write tests manually, especially for more complex logic. These are typically placed in a `tests/` directory, e.g., using Python’s `unittest` or `pytest`. For instance, `tests/test_summarizer_agent.py` might create an instance of SummarizerAgent and assert that summarizing a short paragraph returns a shorter text. Tools can be tested by directly calling their function or class.
* **AgentTesterAgent:** T‑Developer includes an **AgentTesterAgent** (or similar TestRunnerAgent) that can run a basic battery of tests on a given agent automatically. `tdev test MyAgent` uses this. By default, it might run the agent with some sample inputs (perhaps from the agent’s docstring or predetermined samples). The AgentTesterAgent ensures even without custom tests, each agent can at least execute with a nominal input and produce an output of the correct type. This catches issues like missing dependencies or syntax errors in agent code outside of a workflow context.
* **CI Execution:** As described in CI/CD, `tdev test all` runs all tests in an automated fashion. Under the hood, it likely runs through any custom tests and also runs the AgentTester for each component. Results are collected: any failing test will fail the pipeline.

The emphasis in unit tests is on correctness of logic and edge cases:

* Ensuring tools return expected data formats (e.g., a tool that should return a URL returns a valid URL string).
* Ensuring agents handle edge cases (maybe empty input, or if a tool returns an error code, the agent reacts gracefully).
* Performance can be considered (if an agent should complete within certain time for a test input, though that’s usually not strict in unit tests).

### 7.2 Integration Testing of Workflows

Beyond individual components, **integration tests** validate that multiple agents and tools work together in workflows as intended.

* **Workflow Test Cases:** For key workflows (especially those that are intended for deployment), we maintain test definitions. This could be as simple as providing a known input to the orchestrator and verifying the final output. For example, if there is a workflow to handle a support request, an integration test might simulate a sample request from a user and check that the composed response contains certain expected phrases or data.
* **Automated Workflow Execution in CI:** The CI pipeline’s evaluation stage can double as an integration test. When we run `tdev evaluate ./workflows/*.json`, besides scoring, we might also execute the workflow in a dry-run or test mode to see if it completes. Alternatively, a separate step can run `tdev run workflow.json --test-input "..."` to verify execution. If a workflow fails to execute (exception in some agent), the test should catch that and flag the pipeline.
* **End-to-End in Staging:** For workflows meant to deploy as SaaS, deploying them to a staging environment and running an end-to-end test is critical. This might be part of a nightly build or separate QA phase. For instance, after deploying `policy-matcher-v1` to a dev stage, run an automated script that calls the API (via API Gateway endpoint or CLI) with sample input and assert on the output. This ensures the deployment configuration (IAM, environment variables, etc.) is also correct.

Integration tests focus on:

* Data flow correctness: Does the output of Agent A properly feed into Agent B? Are the intermediate results as expected?
* Workflow logic: If there are any conditional branches or loops (in advanced cases), do they work?
* System-level concerns: Check that the orchestrator correctly handles if one step fails (maybe simulate a failure of a tool and see if orchestrator logs or error messages are appropriate).
* Timing/Performance: A workflow test might measure that it finishes within X seconds for a given input (especially if running in Lambda with timeouts).

### 7.3 Automated Quality Evaluation (EvaluatorAgent)

The **EvaluatorAgent** serves as an automated testing mechanism in its own right – but instead of checking specific outputs, it assesses overall quality attributes. This is like having an AI code reviewer or QA engineer:

* **Static Analysis and Best Practices:** EvaluatorAgent may inspect the code of new agents for issues like large complexity, lack of comments, potential security risks, etc., and incorporate that into its score.

* **Dynamic Evaluation:** It can examine the results of test runs or even run additional test scenarios in a simulated manner. For example, Evaluator might have knowledge of common pitfalls and ask “what if input is null?” and ensure the agent handles it (either by analyzing code or by quick sandbox tests).

* **Scoring Model:** The EvaluatorAgent likely uses a model (could be an LLM or a trained regression model) that considers test results, code analysis, and possibly performance metrics to produce a single score. For instance:

  * All unit tests passed: +50 points.
  * Code adheres to style and has comments: +10.
  * No security flags: +10.
  * Edge case coverage seems good: +10.
  * Efficiency: handles large input in test within acceptable time: +10.
  * If any minor issues or suggestions, maybe deduct a few points.

  The output, like “91 (A-)” in the Slack example, gives a high-level summary of quality. In CI, if this score is below threshold, the pipeline can be configured to fail or at least warn.

* **Improvement Suggestions:** Importantly, EvaluatorAgent doesn’t just score; it provides suggestions. These suggestions are a form of “test result” – indicating where the agent or workflow could be improved. Examples: “The plan doesn’t handle when the database is down – consider adding a retry,” or “The output might be too verbose; maybe apply a filter.” These are fed back to developers or to Agno for potential auto-refinement.

By treating evaluation as part of testing, T‑Developer ensures that even aspects not covered by deterministic tests (like readability, maintainability, robustness) are checked.

### 7.4 Regression Testing and Continuous Evaluation

As new agents are added and existing ones evolve, we maintain a regression test suite:

* All previously passing tests (unit and integration) must continue to pass. The versioning system helps here: if SummarizerAgent v2 is introduced, we ensure tests for v1 still pass on v1 (if we are maintaining it) and new tests pass on v2.
* Workflows that were working in the past are periodically re-tested (especially if underlying agents changed). The TestRunnerAgent can run through a suite of important workflows on a schedule and log their success/failure in the TestRunHistory. The Evaluator or a monitoring agent can detect if a formerly working workflow now fails, and alert accordingly.
* **Performance Regression:** We may track metrics like execution time or cost (especially for LLM calls) per agent version. Significant slowdowns or cost increases could be flagged. While not implemented in v1.1, this is a future testing aspect (making sure a new version of an agent is not only functionally correct but also efficient).

### 7.5 Testing Roles of Specialized Agents

A few agents in T‑Developer are themselves part of the testing strategy:

* **AgentTesterAgent:** As mentioned, it’s a specialized agent to test other agents. It might have a knowledge base of simple tests (like if an agent declares its input/output types, AgentTesterAgent might automatically test type mismatches or run the agent with a trivial input to see if it crashes).
* **TestRunnerAgent:** In CI (as seen in architecture diagrams), a TestRunnerAgent is triggered by GitHub Actions. It runs tests and stores results in a TestRunHistoryStore (DynamoDB). This indicates test results themselves are kept for analysis – perhaps the EvaluatorAgent retrieves historical pass rates or failure patterns from this store to adjust scoring or to help decide version promotions.
* **EvaluatorAgent:** Acts like an automated UAT (User Acceptance Testing) and code review agent.
* Possibly a future **FuzzTesterAgent** or similar could generate random inputs to test robustness (not explicitly in v1.1, but the architecture could accommodate an agent that stress-tests other agents).

### 7.6 Developer in the Loop

While a lot of testing is automated, the developer remains in the loop for writing nuanced tests and reviewing AI-driven evaluations:

* If the EvaluatorAgent suggests an improvement, a developer decides if it warrants a code change or if it’s an acceptable risk.
* Developers can add new tests whenever a bug is found (standard practice: write a test that reproduces the bug, then fix the bug).
* Amazon Q Developer might assist by turning natural language bug reports or requirements into test cases or by pointing out missing tests based on documentation. For instance, if design docs say an agent should handle UTF-8 input, Q Developer could ensure a test exists for that.

In summary, T‑Developer’s testing strategy is **multi-layered**:

* **Unit tests** ensure each piece works on its own.
* **Integration tests** ensure the pieces work together.
* **AI evaluation** ensures quality aspects beyond the scope of explicit tests.
* All tests run automatically in CI/CD, preventing regressions from moving forward.
* The system even leverages specialized internal agents to conduct and manage testing, eating its own dogfood (using agents to test agents).

This comprehensive strategy is vital because T‑Developer generates new software components automatically; testing and evaluation provide the safety net and feedback loop that keep this autonomous development both effective and trustworthy.

## 8. Deployment Architecture Diagram and Description

The deployment architecture of T‑Developer describes how the system’s components are deployed on AWS and how they interact at runtime. It covers the flow from code and configuration to running services, and the infrastructure (Lambda, ECS, DynamoDB, API Gateway, etc.) that supports T‑Developer and its generated applications. The diagram below illustrates the key elements of this architecture:

&#x20;*Deployment architecture of T‑Developer v1.1 on AWS (components and data flows).*

In the above diagram, we see how T‑Developer packages and runs agents and workflows in various environments, and how state and logs are managed. The diagram can be explained in a stepwise flow:

1. **Source Artifacts – Code, Workflow, Config:** On the left, we have the inputs that define a service:

   * **Agent Code (S3 or Git):** The actual implementation code for all agents and tools. In a cloud deployment scenario, once code is tested, it might be stored in S3 buckets or a Git repository. For example, when using AWS CodePipeline, a build step could bundle agent code into a zip and push to S3.
   * **Workflow Definition:** The JSON/YAML that describes the workflow of how agents/tools work together (for a particular service or task). These could be stored in a version-controlled store (like S3 or Git) or in the T‑Developer Workflow Store (DynamoDB or files).
   * **Configuration (Parameters):** Any additional config for the service, such as environment-specific parameters, feature flags, or user-defined settings. These might come from a config file or a parameters store. For instance, an agent that calls an API might have a configurable API endpoint or key (which would be referenced via Secrets Manager).

   These three are combined to create a **Service Instance Definition**.

2. **Service Instance Definition:** This is a manifest that brings together the code, workflow, and config for a deployable service. It could be a structured document (JSON) that lists:

   * The workflow ID and version,
   * References to all agents (and their versions) that form that workflow,
   * Configuration like memory requirements, timeouts, etc., and
   * A unique service identifier (e.g., “policy-matcher-v1”).
     The Service Instance Definition is stored (for record and reuse) and then used to drive deployment.

3. **AgentRegistry (DynamoDB):** The agent metadata registry is shown to the side, indicating that the registry is consulted during this process. When composing the Service Definition, the system queries the registry to fill in details (like class paths or latest versions of agents to include). At deployment time, the registry is also updated to mark which agents are used in which service (not explicitly shown, but metadata may include usage info). In the cloud, the registry likely resides in a DynamoDB table for fast access by the orchestrator and deployment functions.

4. **Deployment Orchestrator:** The **Deployment** box represents the process of deploying the service instance to the target environment. This could be the T‑Developer CLI or a deployment agent in the pipeline taking the Service Definition and performing:

   * For **AWS Lambda:** Packaging code and dependencies into a deployment package (zip), uploading to S3 (if not already), and using AWS Lambda APIs to create/update a Lambda function. The Lambda’s handler would typically be a small shim (for example, calling the T‑Developer Workflow Executor with the right workflow on invocation). In the Service Definition’s metadata, an entrypoint like `"handler.py::run"` is noted, which tells Lambda which function to execute on trigger.
   * For **AWS ECS:** Building a Docker image if needed, pushing to ECR, and updating an ECS service or task definition. The container would likely run a lightweight web server or worker that on start loads the necessary agents and waits for input (e.g., listens on an HTTP port if it’s a web service, or processes messages from a queue if event-driven).
   * For **Local CLI Execution:** “Deployment” in this context just means registering it locally – essentially moving the workflow definition to a known location and being able to execute it via `tdev run`. No AWS infra is involved here, but the diagram includes it as a possible execution target (useful for dev/testing or running on an on-prem server).

   The deployment orchestrator takes care of selecting the right target based on the Service Definition’s specified target type and initiating the appropriate deployment steps.

5. **Execution Environments (Lambda, ECS, CLI):** Once deployed, the service can run in one of three environments (as drawn in parallel in the diagram):

   * **AWS Lambda Function:** The service is running as one or more Lambda functions. Typically one function per service. It can be invoked via API Gateway (for synchronous HTTP requests), or triggered by events (like an S3 event, or manually via CLI). Lambda is suited for short-lived execution of workflows on demand.
   * **AWS ECS (Container):** The service is running as a container, possibly behind a load balancer if it’s a web service, or as a long-running processing agent. ECS allows more memory/CPU and longer runtime for heavy or persistent tasks. For example, if an agent needed to maintain a large in-memory index, ECS might be chosen.
   * **Local CLI Execution:** The service can also be “executed” locally for testing. In this case, it’s not a continuously running process but executed when commanded via the CLI.

   Notably, T‑Developer supports multiple coexistence: some services might be on Lambda, others on ECS, depending on their nature.

6. **State Storage (DynamoDB):** To maintain state between invocations or steps, especially for long workflows or multi-step transactions, the system uses DynamoDB (or another database) as **state storage**. For example:

   * If a workflow needs to pause (say waiting for a human approval or an external event), the current state (which step was last executed, intermediate data) could be saved in DynamoDB, keyed by an execution ID. A subsequent invocation (or a resume event) can pick up from that state.
   * Even for stateless operations, DynamoDB might store transient data like caching results or maintaining idempotency tokens.
   * The Service Instance metadata (status, last execution time, etc.) is also kept in DynamoDB tables, as mentioned earlier.
   * If ECS tasks need to share state with Lambdas or with the orchestrator, DynamoDB (or occasionally S3/Redis depending on performance needs) is the go-to solution given its fully-managed and scalable nature.

7. **Execution Logs (CloudWatch):** All runtime logs from agents and workflows are directed to **Amazon CloudWatch Logs**. Each Lambda function automatically logs to CloudWatch. For ECS, the logs can route to CloudWatch via the Log Driver. These logs include:

   * Step-by-step execution details, which agent produced what output, any warnings or exceptions.
   * System logs like execution start/stop, resource usage if any.
     CloudWatch Logs allow developers to troubleshoot and also the monitoring system to trigger alerts on certain log patterns (e.g., if many errors occur).
     Additionally, CloudWatch Metrics might be collected (like count of executions, average duration, etc.) for performance monitoring.

8. **Monitoring & Alerts:** Though not explicitly labeled in the diagram, monitoring components listen to the Execution Logs and State:

   * CloudWatch Alarms could be set on error rates or on specific custom metrics (like “workflow success rate”).
   * An external Monitoring agent or AWS Lambda might aggregate logs and send notifications. For instance, if an error occurs in a deployed service, an SNS topic can send a message which is then forwarded to Slack or email for the team.
   * Amazon Q Developer could also tap into these metrics/logs to inform developers through its UI if something is failing frequently.

9. **UI and API Gateway:** On the left (User interactions) not explicitly drawn above, but in the earlier architecture diagrams, we saw:

   * A **UI (Agent UI Launcher)** calls the orchestrator or deployed services. Likely, API Gateway endpoints exist for each deployed service’s Lambda so that the UI can invoke them via HTTP.
   * The CLI can invoke local or remote services. For remote (cloud) deployment, the CLI might call an API Gateway or use AWS SDK (e.g., `aws lambda invoke` under the hood).
   * The orchestrator itself, if hosted in AWS (perhaps as a Lambda behind an API Gateway for Q Developer usage), follows a similar pattern: the user’s request goes to an API Gateway endpoint which triggers the orchestrator lambda.

   In summary, the user (or Amazon Q front-end) interacts via API endpoints, which route to either orchestrator or specific service lambdas.

### Deployment Example Flow:

To illustrate, consider deploying a new “PolicyMatcher” service:

* The developer composes a workflow `policy-match-flow-v1.json` and has agents ready. They run `tdev deploy --service-id policy-matcher-v1 --target lambda`.
* T‑Developer generates a Service Instance Definition that includes `policy-match-flow-v1` workflow and the agents (e.g., `ScraperAgent`, `MatcherAgent`, `ResponderAgent`) with their code references.
* It stores this definition in S3 and in DynamoDB (for tracking).
* It packages the code for those agents (maybe they reside in the repo, so package those files and the runtime) and uploads to S3. Then calls AWS Lambda CreateFunction with that package.
* A new Lambda function `policy-matcher-v1` is created with an IAM role that lets it access a specific DynamoDB table (to fetch any needed data) and maybe an S3 bucket if needed.
* The Service metadata is saved: `service_id = policy-matcher-v1, status = active, created_at = ..., deployment.type = lambda, region = ..., entry_input_type = "text", output_type = "response"` etc..
* The CLI or UI can now invoke this service’s API (through an API Gateway mapping to the lambda’s handler).
* When invoked, say with input “Find policies for youth startups”, the Lambda function internally loads the workflow and agent classes (from the package or possibly fetches latest from registry if dynamic, though likely uses packaged code for consistency). It then executes step by step (likely within that single Lambda invocation, assuming it’s quick).
* It writes logs to CloudWatch for each step. If it needs to store partial results or if it goes beyond one invocation (not typical for Lambda unless orchestrator intentionally splits), it could use DynamoDB.
* It returns the final result to the caller (API Gateway returns to UI).
* Meanwhile, all this is logged and if any exception occurred, it would be visible in logs and possibly trigger an alert.

This deployment architecture ensures **scalability** (Lambda/ECS handle scaling out under load), **fault isolation** (each service is independent in its function or container), and **manageability** (with centralized logging and state tracking). It also supports versioning – when a new version of a service is deployed (say v2), it can be deployed alongside the old (blue/green or canary as described in Integration & Deployment doc).

### AWS Services Summary:

* **API Gateway:** front-door for orchestrator and any web-exposed agent services.
* **AWS Lambda:** runs ephemeral compute for orchestrator and stateless services.
* **AWS ECS (Fargate or EC2):** runs containerized services that need longer or stateful runtime.
* **Amazon S3:** stores code artifacts and possibly workflow files (versioned storage of definitions).
* **AWS DynamoDB:** key storage for AgentRegistry, WorkflowStore, Service metadata, and execution state that must persist between steps or track history. Also used for TestRunHistory.
* **AWS CloudWatch Logs & Metrics:** captures logs and custom metrics for executions, provides monitoring and alerting.
* **AWS SNS / Slack integration:** for sending out notifications (could be via SNS -> Lambda that posts to Slack, or direct webhooks configured in the pipeline).
* **AWS Secrets Manager:** (Though not pictured, part of security) provides secure storage of secrets, which Lambdas or containers fetch at runtime as needed.

The **Deployment Architecture Diagram** combined with this description provides a complete view of how T‑Developer operates in a cloud environment, transforming defined agents and workflows into live services, and maintaining all the necessary infrastructure (compute, storage, logging) to support them.

## 9. Agent Lifecycle Document

The Agent Lifecycle Document describes the stages an agent (or tool) goes through in T‑Developer v1.1 – from its inception to retirement. This includes creation (either manual or via generation), testing and validation, deployment into workflows or services, versioning over time, and eventual deprecation or replacement. Understanding this lifecycle ensures that agents are managed in a sustainable, organized way as the system evolves.

### 9.1 Creation of Agents

Agents can be created in two primary ways: **manually by a developer** or **automatically by Agno (AutoAgentComposer)**.

* **Manual Creation:** A developer identifies the need for a new agent. Using the CLI, they can initialize a scaffold:

  ```bash
  tdev init agent --name MyAgent:contentReference[oaicite:215]{index=215}
  ```

  This creates a new file (e.g., `tdev/agents/my_agent.py`) with a template class inheriting from `Agent`, including a placeholder `run()` method. The developer fills in the logic inside `run`, possibly using existing tools via the registry as needed. They also add a docstring and type hints to define the agent’s behavior and I/O clearly.

  Once implemented, the developer registers the agent:

  ```bash
  tdev register tdev/agents/my_agent.py:contentReference[oaicite:219]{index=219}
  ```

  This command loads the agent class, creates its metadata (using the ClassifierAgent to determine type and properties), and adds it to the AgentRegistry. Programmatically, one could do the same by calling registry APIs in Python, but CLI is simpler.

* **Automatic Generation (Agno):** The Planner or developer requests a new agent via:

  ```bash
  tdev generate agent --name NewAgent --goal "Description of what it should do":contentReference[oaicite:222]{index=222}
  ```

  or providing a spec JSON. Agno then follows the steps as described in the Component Spec: analyze, generate code and metadata, and automatically register the agent in the registry. The new agent’s code is saved either in memory or to a file (`.tdev/generated/` or similar). The ClassifierAgent runs as part of this to assign brain\_count, etc., to the metadata.

  After generation, typically a developer reviews the code (possibly with Amazon Q Developer’s aid) and may run some initial tests on it.

Regardless of creation method, at the moment of registration, the agent acquires an initial **version** (implicitly v1 or 1.0.0).

* For manual agents, the developer might set a version in the metadata or code (somewhere in AgentMeta or class attribute).
* For Agno, the first generated artifact is version 1 (Agno could tag it as such). The system uses semantic versioning for code changes and simple numeric version IDs (v1, v2) for referencing in workflows.

### 9.2 Testing & Validation

Once created, an agent enters a testing phase:

* **Immediate Smoke Test:** The developer can run `tdev test MyAgent` to do a quick check using AgentTesterAgent. If this fails (for example, the agent code has a syntax error or it crashes on a basic input), they will fix the issues and possibly iterate.
* **Writing Unit Tests:** The developer writes targeted tests for the agent’s logic. For instance, if MyAgent should return a sorted list given an input list, they test that behavior with various cases. These tests are added to the repository.
* **CI Validation:** When the code is pushed or a PR is opened, the CI pipeline classifies the new agent (updating registry), runs all tests (including new ones for MyAgent), and runs the EvaluatorAgent. The new agent must pass all tests and likely get a decent evaluator score to be considered stable. If not, the developer addresses the feedback (e.g., add missing test cases, optimize code if Evaluator flagged inefficiency, etc.) and pushes updates.

During this validation period, the agent’s status might be considered "experimental". It’s effectively in a staging area until it proves itself via tests. The AgentRegistry can have a field like `status: experimental` for new agents, which could prevent Planner from using them in critical workflows unless explicitly allowed.

If the agent is generated by Agno, this phase might involve more iteration:

* The EvaluatorAgent suggestions could feed into a refine step (in future using `tdev refine` as noted in Agno plans).
* Human review might catch logical errors that tests missed, prompting tweaks to the agent.

### 9.3 Deployment and Usage

After an agent is validated, it is ready to be used in workflows and possibly deployed as part of services:

* **Integration into Workflows:** The PlannerAgent will now consider the new agent when planning tasks related to its function. The agent’s metadata (especially its `tags` and `input/output_schema`) makes it discoverable for relevant goals. Developers can also manually compose workflows including the agent. For example, adding MyAgent as a step in an existing workflow JSON.
* **Service Deployment:** If the agent is part of a workflow that is deployed as a service, it gets deployed too. There isn’t a one-to-one deployment of every agent (unless an agent is itself the entrypoint of a service). Usually, multiple agents together form a deployed application. However, one could deploy a single agent as a microservice: e.g., deploy SummarizerAgent as a Lambda that can be invoked via API with text input. This might be done for heavily reused agents.
* **Version Promotion:** Initially, an agent is version 1 (v1). As it gets used and passes real-world testing, it can be marked "stable" and that version might be published for consumption. If using semantic versioning, one might tag it `1.0.0` release after initial tests are done.
* **Documentation:** At deployment/usage time, documentation should be written or generated for the agent (if not already). This includes updating any **Agent Registry documentation** (like an internal wiki of available agents), and possibly generating markdown from the agent’s docstring for the knowledge base. Amazon Q Developer might assist by taking the metadata and code to produce a neat documentation page.

### 9.4 Versioning and Evolution

Agents are rarely static; they improve or change over time. T‑Developer’s versioning strategy:

* **Semantic Versioning:** Code changes to an agent follow X.Y.Z versioning. For example, a backward-compatible enhancement (like improving algorithm without changing interface) increments the minor version (1.1.0), whereas a breaking change (changing input/output schema or behavior significantly) would increment the major version (2.0.0).
* **Registry and Workflows with Versions:** The AgentRegistry can store multiple versions of an agent. Workflows explicitly reference a specific version to ensure consistency. For instance, a workflow might say “use SummarizerAgent\@v1”. If SummarizerAgent v2 is released with a new feature, existing workflows still use v1 until updated intentionally. This avoids surprise breakages.
* **Promotion to Stable:** New versions might be deployed as “beta” or “experimental”. Using *AgentVersionManager* (a conceptual component), the system might automatically promote a version to stable if it meets criteria: all tests pass, Evaluator score high, and no regressions found. Only then does it mark it as the default for new workflows.
* **Dependency Tracking:** Agents might depend on specific versions of tools. The system tracks these dependencies. If a tool MyTool v2 comes out and MyAgent was built against MyTool v1, the EvaluatorAgent or version manager might flag to test MyAgent with the new tool before promoting that tool globally.
* **Release Notes:** For important agent version updates, the team writes release notes (maybe captured in a CHANGELOG). This is especially needed if major changes occur. Amazon Q Developer could help aggregate these (since it has all design docs, it might auto-summarize what changed between versions by reading diffs).

### 9.5 Deployment and Runtime Lifecycle

Once agents are part of deployed services, their lifecycle includes runtime considerations:

* **Monitoring in Production:** The performance and errors of agents are monitored via CloudWatch. If an agent in a service errors frequently or behaves sub-optimally (like taking too long), it might indicate the need for a fix or improvement (triggering a new version cycle in development).
* **Hot Patching:** In some cases, minor changes (patch version) can be deployed quickly if a bug is found. T‑Developer’s pipeline supports quick rollouts of patches (1.0.1, 1.0.2, etc.) with the same testing rigor on each.
* **Rollback:** If a new agent version or new agent causes issues in production, rollback strategies are in place. For example:

  * Rollback an agent version: The AgentVersionManager can force workflows to use the previous stable version (since it’s still in the registry). E.g., if SummarizerAgent v2 fails, switch references back to SummarizerAgent v1 for all workflows where applicable.
  * Rollback a service: If the issue is broader (maybe the workflow logic), `tdev rollback --service-id X --to v1` can redeploy the previous workflow version.
  * Emergency disable: In worst case, an agent could be “disabled” in the registry (flagged so that orchestrator won’t use it at all), until fixed.

The lifecycle ensures traceability:

* The **audit logs** tie agent versions to deployments and issues. If something goes wrong, we can trace it to “Agent Y version 2.3.0 caused this”.
* The **Git history** preserves code changes for each version, so one can inspect differences and run blame analysis.

### 9.6 Retirement (Deprecation) of Agents

Over time, some agents or tools become obsolete – perhaps a better agent supersedes it, or the feature is no longer needed.

* **Deprecation Policy:** We mark an agent as deprecated in the registry (status = deprecated). That signals to developers and the PlannerAgent to avoid using it for new plans. The agent remains available to support older workflows if needed.

* **Phased Out:** If no workflows use the agent anymore (or we have migrated all workflows to a newer agent), the agent can be fully retired. We then:

  * Remove it from registry via `unregister(name)`. (The entry might still remain in version history storage for audit, but it’s no longer active.)
  * Archive its code (keep in Git but maybe move to an archive folder or branch).
  * Remove tests related to it (if it’s fully gone).

* **Backward Compatibility:** If an agent is deprecated due to a better approach, often a compatibility shim or an alias might be kept for a while. For example, if “OldTranslatorAgent” is replaced by “NewTranslatorAgent”, the Planner might be instructed to use the new one, but if a workflow explicitly asked for OldTranslatorAgent, we either keep it functioning or update that workflow.

* **Retiring Tools/Services:** If a low-level tool is retired (say an API is no longer supported), any agent using it either gets updated to a new tool or that agent is also deprecated. So retirement can cascade if not managed – hence T‑Developer likely uses the dependency info in metadata to find what is impacted by a retirement.

* **Retention of History:** Even after retirement, logs and historical data are kept as per retention policy. For example, previous stable versions are retained indefinitely in the repository and registry backups. This means even years later, if someone needs to know what a retired agent did, the info is accessible.

### 9.7 Continuous Improvement and Evolution

The lifecycle isn’t just one-way; agents can re-enter cycles:

* If new requirements emerge, an existing agent might be enhanced (new version). Then it goes through testing, deployment, etc., again.
* If an agent’s performance is not satisfactory, it might be slated for improvement (e.g., use a more advanced model). That’s a new development cycle.
* Sometimes, AI improvements (like a new LLM via Bedrock) could allow simpler agents to replace complex ones. In such a case, you might generate a new agent and deprecate an older complex workflow.

T‑Developer’s orchestration is meant to make these transitions smooth:

* Workflows can mix agent versions (though usually use one version at a time per agent).
* A new agent can be introduced and the PlannerAgent can gradually start using it for new tasks, while old workflows keep using old agents until explicitly migrated (kind of like AB testing or canary usage of new agents in orchestrations).

In conclusion, the lifecycle of an agent in T‑Developer covers **birth (design & generation)**, **adolescence (testing & refinement)**, **adulthood (deployment & stable use)**, and eventually **retirement**. At each stage, there are checks and balances: human oversight, automated testing, version control, and monitoring. This ensures that as the library of agents grows (and possibly autonomously evolves), it remains reliable and manageable, with a clear record of how each agent came to be and how it has been used.

## 10. Roadmap Summary

T‑Developer v1.1 is part of a larger multi-phase roadmap aimed at progressively increasing the system’s autonomy, capabilities, and integration. This section provides a summary of the roadmap, including past phases, key milestones achieved, current status, and planned next steps. It references prior research and development milestones, particularly the transition from Phase 2 to Phase 3, which is the context of v1.1.

### 10.1 Phase Overview

* **Phase 1: Foundation (Initial Development)** – *Goal:* Build core functionality for individual agent and tool creation manually.
  *Timeframe:* (Hypothetical early stage, likely in v1.0)
  *Key Achievements:* Established the basic architecture and taxonomy (Tools vs Agents vs Teams). Developed initial set of core agents (Classifier, Planner, etc.) by hand. Confirmed that an orchestrator could execute a simple predefined workflow (but orchestrator might have been rudimentary). This phase was more manual development of core capabilities and no automatic generation yet.

* **Phase 2: Manual Core Development & Basic Orchestration** – *Goal:* Solidify core agents and orchestrator logic without generation, prepare for automation.
  *Timeframe:* (Pre-v1.1, leading up to current)
  *Key Achievements:*

  * Implemented stable versions of core agents: EchoAgent, ClassifierAgent, PlannerAgent, etc., all written manually.
  * OrchestratorTeam established to coordinate a fixed sequence of these agents for a user request.
  * Basic CLI tools (`tdev` commands) created for manually registering and composing agents.
  * Ensured the system can handle end-to-end scenarios by using existing agents (no on-demand creation).
  * **Milestone:** Achieved a working pipeline where a user input goes through classification, planning, and execution using only pre-built components (but might struggle if something is missing, as generation was not yet present).
  * Documentation and design for the next phase (how to integrate generation and more dynamic assembly) was prepared.

* **Phase 3: Orchestrated Team Assembly & Autonomous Generation (Current, v1.1)** – *Goal:* Introduce automated agent/tool generation (Agno) and advanced orchestration for dynamic team formation.
  *Timeframe:* (Current phase, T‑Developer v1.1 corresponds to entering Phase 3)
  *Key Achievements (so far):*

  1. **Agno Implementation:** Designed and implemented the AutoAgentComposer (Agno) subsystem to generate new agents/tools from specifications. This included building subcomponents like spec parsing, template library, etc., and integrating Agno as an agent that the orchestrator can call. *Status:* ✅ Completed.
  2. **Conversion to Generated Components:** Applied Agno to existing components – essentially “rebootstrapping” core agents by generating their code from spec to validate Agno’s effectiveness. Many Phase 2 agents (EchoAgent, PlannerAgent, etc.) were re-specified and re-generated to ensure consistency and to populate the registry with Agno-generated versions. *Status:* ✅ Completed (core agents now have Agno-generated implementations).
  3. **MetaAgent Orchestrator Enhancement:** Implemented the MetaAgent orchestrator (SupervisorAgent) to coordinate core agents in a loop with possible refinement. This was an upgrade from any simpler orchestration in Phase 2 – now the orchestrator can dynamically decide to loop back or trigger generation if needed. OrchestratorTeam updated to use this MetaAgent structure. *Status:* ✅ Completed.
  4. **CLI and Tooling updates:** Added CLI commands to leverage new capabilities, e.g., `tdev generate` for Agno, `tdev orchestrate` to run the orchestrator on a user goal in one command. Documentation was updated for these new commands. *Status:* ✅ Completed.
  5. **Agent Squad Framework Integration:** Integrated with AWS Agent Squad to allow more complex orchestrations (parallel tasks, etc.) to set the stage for the future. *Status:* ✅ Completed foundational integration (we can now treat orchestrations more flexibly; actual parallelism usage might come later).

  *Current Progress:* The foundation for autonomous team assembly is laid. We have a system that can generate new components on the fly and orchestrate multiple specialized agents to solve tasks. T‑Developer v1.1 marks the achievement of these capabilities. We are now in the early Phase 3, focusing on leveraging and refining them.

### 10.2 Key Milestones and Achievements

* **Automated Agent Generation (Agno):** Achieved the ability for the system to expand itself. This is a pivotal milestone – T‑Developer can now handle requests beyond its initial programming by creating new tools/agents as needed. For example, if asked to integrate with a QR code service and none exists, it can generate one (as demonstrated by QRCodeResolverAgent).
* **Dynamic Orchestration Loop:** The orchestrator can now iterate (with evaluation feedback) until an optimal solution is found. In Phase 2, orchestrations might have been one-pass; now we have a feedback loop via EvaluatorAgent and possibly multiple planning attempts, which improves outcome quality.
* **End-to-End Automation Pipeline:** With CI/CD integration and testing strategies implemented, from code generation to deployment can be largely automated. A PR with a new agent triggers classification, tests, evaluation, and if all good, that agent can be deployed in a new service without human intervention beyond code review.
* **Deployment & DevOps Integration:** Support for deploying to AWS (Lambda/ECS) directly from T‑Developer workflows was established (like the `tdev deploy` functionality and underlying Infrastructure-as-Code). This closes the loop from idea to running cloud service in potentially minutes.
* **Documentation & Knowledge Base:** The project compiled comprehensive documentation (architecture docs, specs like this set). This ensures that as more people (or AI like Amazon Q Developer) work with T‑Developer, they have a clear map of how it works and can build on it.

### 10.3 Next Steps (Phase 3 Continued and Phase 4 Outlook)

The transition to Phase 3 identified some next-focus areas. These form the immediate roadmap moving forward:

1. **Full Workflow Testing:** Now that the orchestrated team assembly is in place, perform extensive end-to-end tests of various complex workflows. This will likely involve creating scenario-based tests (maybe using real-world-like tasks) to ensure the orchestrator + agents + agno can handle them. This solidifies reliability.
2. **Advanced Team Composition:** Develop more complex team structures and patterns. For example, implementing hierarchical teams (teams composed of teams), or specialized squads for different domains (a web-scraping mini-squad, a data-analysis mini-squad, etc.). Also exploring parallel executions within a workflow (since the Agent Squad framework allows it).
3. **Dynamic Agent Generation in Planning:** Rigorously test and refine the PlannerAgent’s ability to invoke Agno on the fly. Ensure that when a missing piece is identified, the spec generation for that piece is optimal, and that multiple new agents can be generated in one go if needed. Possibly introduce constraints so it doesn’t over-generate or attempt to create agents if not necessary.
4. **Deployment Integration (Complete Cycle):** By end of Phase 3, connect the orchestrated teams to actual live deployment targets seamlessly. This means a user could say “create and deploy an app that does X”, and T‑Developer will not only generate the agents and workflow but also deploy it to cloud and provide an endpoint. Some of this is done, but focus here is making it robust and perhaps one-command from goal to deployed service.
5. **Monitoring and Feedback for Deployed Services:** Add mechanisms to feed production usage data back into T‑Developer’s improvement loop. For example, if a deployed service’s EvaluatorAgent (as a runtime monitor) notices certain patterns (like frequent user errors or slow responses), it could trigger an improvement process – maybe flag for developer or even auto-adjust parameters. Essentially closing the loop from production monitoring to planning adjustments.

Looking slightly further (Phase 4 and beyond, though not formally in the prompt, we can extrapolate):

* **Phase 4: Scaling and Generalization** – *Goal:* Scale T‑Developer to handle more complex projects and possibly multiple orchestrators/organizations. Potential focuses:

  * Integration with more AI capabilities (like using different foundation models via Bedrock for specialized tasks).
  * Improved human-AI collaboration features: e.g., a feature where a human can intervene in the planning or evaluation in real-time (a feedback UI where human accepts or rejects Evaluator suggestions).
  * Multi-modal inputs/outputs: not just text, but perhaps orchestrating agents on images, audio (some tools exist for that, but making it a standard).
  * Enhanced learning: The system could learn from past deployments which solutions worked best and reuse those patterns (some form of meta-learning).
  * **Key Milestone**: Possibly a marketplace or registry of community-contributed agents that T‑Developer can pull from, making it an open ecosystem.

* **Phase 5: Fully Autonomous DevOps** – The vision might be to reach a state where given a high-level product requirement, T‑Developer (with Amazon Q Developer) can create a production-ready system with minimal human assistance. This would involve advanced validation (maybe formal verification for critical components), compliance checks, and self-optimization.

### 10.4 Current Progress Recap

As of v1.1 (mid Phase 3):

* We have successfully moved from a manual, static system (Phase 2) to a dynamic, self-improving system (Phase 3). The **transition summary** documented the completion of tasks enabling this.
* The team has checked off critical items like implementing Agno and MetaAgent orchestrator, which were prerequisites to call Phase 3 truly begun.
* The present focus is on stabilization: ensuring all these new capabilities work reliably together, hence the emphasis on thorough testing and incremental rollout (perhaps starting with non-critical use cases before using T‑Developer for mission-critical deployments).

The roadmap emphasizes an iterative enhancement approach: each phase builds on the last, delivering new autonomy and requiring rigorous validation. The **progress so far is promising** – T‑Developer v1.1 demonstrates a working prototype of an autonomous development assistant that can generate and deploy software. The upcoming milestones aim to refine this prototype into a robust platform that can be widely adopted (especially internally via Amazon Q Developer, and eventually possibly beyond).

### 10.5 Summary of Milestones

To summarize key milestones and their status:

* **v1.0:** Basic multi-agent orchestration (manual agents, no gen) – *Completed.*
* **v1.1:** Automated generation (Agno) and orchestrator with feedback – *Completed.* (This delivery)
* **v1.2 (Planned):** End-to-end deployment from spec to cloud in one flow, with full test coverage – *In Progress.* (Likely to incorporate Next Steps 1-5 above)
* **v2.0 (Future):** Possibly represents achieving a level of fully autonomous “idea to app” capability, having incorporated learning from v1.x series, and scaling up to more complex applications.

All in all, the roadmap shows a clear trajectory toward increasing automation, intelligence, and reliability. With each phase’s accomplishments and upcoming tasks outlined, Amazon Q Developer and the team can align their efforts and measure progress. The current progress from prior research indicates we are on track – the foundation is set, and now it’s about polishing and expanding upon it to reach the next breakthrough in autonomous software development.
