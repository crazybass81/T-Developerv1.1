좋습니다. EC2 환경에서 Python 기반으로 작업하고, `.md` 포맷의 문서로 관리하는 것을 기준으로:

* T-Developer를 Tool/Agent 조합 기반 메타 시스템으로 구성하는 데 필요한 **추가 문서 목록**을 작성하고,
* 최소 인프라 구성을 위한 실행 순서 및 **작업 지시서**를 `.md` 문서 형식으로 생성하겠습니다.

준비가 완료되면 문서 초안을 공유드릴게요.


# T-Developer Minimal Infrastructure Work Plan

## Additional Documentation Files to Create

* **ARCHITECTURE.md** – Provides an updated high-level overview of T-Developer’s meta-agent architecture. This document will explain how the system is composed of multiple Agents and Tools (e.g. Classifier, Planner, Workflow Executor, etc.) orchestrated by a central Meta-Agent. It will also describe how components interact (Registry, workflows, storage) and the EC2 deployment context.
* **AGENTS.md** – Describes the role of **Agents** in the system and guidelines for adding new agents. It will list core agent types (e.g. ClassifierAgent, PlannerAgent, EvaluatorAgent, WorkflowExecutorAgent) and explain their responsibilities. This guide will include instructions on creating a new agent class (implementing the base Agent interface, defining input/output schema, etc.) and how agents are registered in the system.
* **TOOLS.md** – Provides a similar guide for **Tools**, which are modular components an agent can use (e.g. an LLM caller, SlackNotifier, etc.). It will outline how to implement new tools and how they differ from agents. This doc ensures that developers can easily add tools by following a template and updating the registry with tool metadata.
* **WORKFLOWS.md** – A guide to creating and managing **workflow definitions**. It will explain the format (YAML/JSON) of a workflow file, including fields like workflow ID, inputs, sequence of steps with agent names, and outputs. It will also describe how to compose a workflow (manually or via a PlannerAgent) and how workflows are executed by the Workflow Executor.
* **CLI\_USAGE.md** – Documentation for the command-line interface. It will list all `tdev` commands, their options, and examples (e.g. how to initialize an agent/tool, classify a file, register an agent, compose a workflow, run a workflow, run tests, etc.). This helps users understand how to interact with T-Developer’s functionality through the CLI.
* **CONTRIBUTING.md** – Developer contribution guidelines. This will include coding conventions, directory structure overview, and a checklist for adding new components. In particular, it will reference **AGENTS.md** and **TOOLS.md** for adding new functionality and emphasize updating the Agent Registry and documentation whenever a new agent/tool is added.

*(These documentation files will ensure that future contributors and users have clear guidance on the system’s architecture and how to extend it. Each file’s content aligns with the system’s design, making it easier to onboard new agents/tools and maintain consistency.)*

## Implementation Phases and Task Breakdown

Below is a phase-wise plan to bootstrap the minimal infrastructure of T-Developer. Each phase focuses on setting up core components or features in a logical sequence. Each task includes a description of the work, the target location in the project, the expected outcome, and the rationale.

### Phase 1: Project Structure and Initialization

1. **Initialize Repository Structure**
   **Description:** Create the base project layout. Define a Python package (e.g. `tdev/`) with sub-packages for core components, agents, tools, etc. Set up essential files like `setup.py` or `pyproject.toml` (for package configuration), an empty `README.md` (to be expanded later), and a `requirements.txt` for dependencies. Include a `tests/` directory for future unit tests.
   **Directory Path:** Project root (`/`) – will contain top-level folders: `tdev/`, `tdev/agents/`, `tdev/tools/`, `tdev/core/`, `tdev/workflows/`, `tests/`, `docs/`.
   **Expected Output:** A skeletal repository structure with directories and empty `__init__.py` files, ready to hold code. For example:

   ```plaintext
   T-Developer/
    ├─ tdev/
    │   ├─ __init__.py
    │   ├─ core/
    │   ├─ agents/
    │   ├─ tools/
    │   ├─ workflows/
    ├─ tests/
    ├─ docs/ (for new documentation files)
    ├─ README.md
    ├─ requirements.txt
   ```

   **Rationale:** Establishes a organized foundation for the codebase so that subsequent components can be added in logical locations. A clear layout improves maintainability and makes it easier to navigate the project as it grows.

2. **Set Up Configuration and Environment**
   **Description:** Prepare configuration scaffolding and environment setup. Create a sample environment config (e.g. a `.env.example` if needed for API keys, etc.) and a basic configuration module. Also create a placeholder for a local configuration directory (named `.tdev/`) which will store runtime metadata (like the agent registry and workflows). This may involve updating `.gitignore` to exclude `.tdev/` since it will be generated data.
   **Directory Path:** Project root for config files; a runtime config directory `.tdev/` (to be created when running commands).
   **Expected Output:** Configuration files and directories ready for use. For example, a `.tdev/` directory structure with placeholders:

   ```plaintext
   .tdev/  
     ├─ registry.json        (to store registered agents/tools)  
     ├─ workflows/           (to store workflow definition files)  
     └─ instances/           (to store service instance metadata)  
   ```

   as defined in the CLI spec. Also, basic config handling code (e.g., `tdev/core/config.py`) to load environment variables or default settings.
   **Rationale:** Even in a minimal skeleton, defining where and how configuration and metadata will be stored is important. The `.tdev` directory will mirror the structure needed for agent registry and workflow files, allowing the CLI and other components to find these resources in a consistent location. This sets the stage for persisting agent metadata and workflow definitions.

### Phase 2: CLI Scaffolding

1. **Implement CLI Entry Point**
   **Description:** Create a command-line interface entry script (e.g. `tdev/cli.py`) using a library like Click or argparse. Define the main `tdev` command and subcommands as outlined in the CLI specification. Initially stub out the following commands with placeholder functionality:

   * `tdev init agent/tool` – prints a message or creates a simple template file for a new agent or tool.
   * `tdev classify <file>` – placeholder that just logs classification (e.g. always returns “agent” for now).
   * `tdev register <file>` – stub that adds an entry to `registry.json` with dummy metadata.
   * `tdev compose --name X --steps A,B` – creates a dummy workflow file in `.tdev/workflows/`.
   * `tdev run <workflow-id>` – invokes the workflow executor (to be implemented later) on a given workflow.
   * (Future commands like `build`, `deploy`, `status` can be listed but will just echo “Not implemented” for now.)
     Each command should be wired into the CLI parser so that running `tdev <command>` calls the appropriate function.
     **Directory Path:** `tdev/cli.py` (or a `tdev/cli/` module) for CLI implementation; plus an entry in setup (console\_scripts) if packaging.
     **Expected Output:** A working CLI interface where `tdev --help` lists available subcommands, and each stubbed command can be invoked without errors. For example, `tdev init agent --name MyAgent` might create `agents/my_agent.py` with a simple class template, or simply confirm the input. `tdev compose --name demo-flow --steps A,B` would generate `.tdev/workflows/demo-flow.yaml` (with placeholder content).
     **Rationale:** The CLI is the primary interface for users to interact with T-Developer. Even as a skeleton, having the command structure in place allows testing the workflow of the system end-to-end. Stubbing the functionality ensures that as other components (registry, executor, etc.) are implemented, they can be hooked into these commands. This also lays the groundwork for automation pipelines, as external systems or developers can start using `tdev` commands immediately (even if results are dummy initially).

2. **CLI Command: Initialization Templates**
   **Description:** Implement the `tdev init` subcommands to bootstrap new components. For `tdev init tool`, generate a boilerplate Python file in `tdev/tools/` (e.g. `gptcaller_tool.py`) using a basic template (class definition inheriting from Tool base, placeholder `run()` method). For `tdev init agent`, similarly generate a file in `tdev/agents/` with a class inheriting from Agent base (to be created in Phase 3) and possibly include reference to a tool if provided (`--tool` option) in the template. The templates can be very simple, just enough to show structure.
   **Directory Path:** `tdev/cli.py` for logic, writing files into `tdev/tools/` or `tdev/agents/`. Include template files or strings within the CLI module or under a `templates/` directory.
   **Expected Output:** Users can run initialization commands to create new stub agents/tools. For example, `tdev init agent --name SampleAgent` creates `tdev/agents/sample_agent.py` with content like:

   ```python
   from tdev.core.agent import Agent  
   class SampleAgent(Agent):  
       def run(self, input_data):  
           # TODO: implement agent logic  
           return None  
   ```

   These files will also be reflected in the project structure.
   **Rationale:** Automating the creation of new agent/tool files ensures consistency and lowers the barrier for adding components. It also reinforces the intended structure (developers see the template and fill in logic). This aligns with the meta-agent design goal of allowing dynamic extension – even at skeleton stage, we demonstrate how new modules are added systematically.

3. **CLI Command: Workflow Composition & Execution (Stub)**
   **Description:** Implement the `tdev compose` and `tdev run` commands in stub form. `tdev compose --name <flow> --steps <A,B,...>` will assemble a very basic workflow definition file (e.g. YAML or JSON) listing the given steps in order. For now, assume each step corresponds to an agent name provided. The output file (e.g. `.tdev/workflows/<flow>.yaml`) will include a sequence of agent references and dummy input/output mappings. The `tdev run <workflow>` command will read the workflow definition and call a placeholder Workflow Executor (to be implemented in Phase 4) that simply logs the steps execution in order.
   **Directory Path:** `tdev/cli.py` (logic to handle compose/run), writing files under `.tdev/workflows/`. Possibly create a helper in `tdev/core/workflow.py` to format or parse workflow definitions.
   **Expected Output:** Running `tdev compose --name sample-flow --steps AgentA,AgentB` produces a file like `.tdev/workflows/sample-flow.yaml` containing something like:

   ```yaml
   id: sample-flow-v1  
   steps:  
     - agent: AgentA  
     - agent: AgentB  
   ```

   (including more structure later, e.g. inputs/outputs). Running `tdev run sample-flow-v1` will load this file and print/log a message for each step execution (e.g. “Executing AgentA... done. Executing AgentB... done.”) without real logic yet.
   **Rationale:** These commands realize the workflow composition and execution capability of T-Developer’s CLI. Even minimally, allowing users to define an ordered list of agents and then executing that sequence is crucial to demonstrate the skeleton of the meta-agent workflow. It shows how the system will coordinate multiple agents (in sequence) to fulfill a task, which is the essence of an orchestrated workflow.

### Phase 3: Core Framework – Agent/Tool Base and Registry

1. **Define Agent and Tool Base Classes**
   **Description:** Create abstract base classes for **Agent** and **Tool** to provide a common interface. For example, `tdev/core/agent.py` defining class `Agent` with an abstract method (e.g. `run(input_data) -> output_data`), and perhaps properties like `name` or `description`. Similarly, `tdev/core/tool.py` for Tool with a `use(input_data)` or similar method. These base classes will be inherited by all concrete agent/tool implementations. Also define a simple **Team** class or concept if needed (for grouping agents, as indicated by registry spec supporting type "team").
   **Directory Path:** `tdev/core/agent.py`, `tdev/core/tool.py` (and possibly `tdev/core/team.py`).
   **Expected Output:** Base class definitions in the codebase. For instance, an `Agent` class that other agent classes (like PlannerAgent, etc.) can subclass. These base classes might also include common utility methods (e.g. logging or accessing the registry) to be expanded later. At this stage, they will mostly define the interface (method signatures) and minimal implementation (e.g. an `Agent.run()` that raises `NotImplementedError`).
   **Rationale:** Standardizing how agents and tools are implemented ensures that the orchestrator and registry can interact with any agent/tool uniformly. By having a base class, we make it easy to manage collections of agents/tools and invoke them polymorphically. This also clarifies for developers what functions to implement when creating a new agent or tool (as documented in AGENTS.md/TOOLS.md).

2. **Implement Agent Registry**
   **Description:** Develop the **AgentRegistry** component, which holds metadata and references to all agents, tools, and teams in the system. The registry can be a singleton class or module (`tdev/core/registry.py`) that maintains a dictionary mapping component names to their metadata and/or instantiated objects. In this minimal version, implement functions to:

   * Load registry data from a local JSON file (e.g. `.tdev/registry.json`) if it exists, otherwise initialize an empty registry.
   * Register a new agent/tool: given a Python class or a metadata dict, add it to the registry dictionary and update the JSON file. For now, the metadata can include fields like `type` (agent/tool), `class` (import path or class reference), and maybe a placeholder for `path`.
   * Retrieve an agent/tool by name (to be used by the workflow executor or other agents).
     Structure the registry JSON as per specification, for example: a mapping of names to an object with `type`, `class`, etc. (In this skeleton, local file storage is sufficient; S3/Dynamo can be integrated later for production.)
     **Directory Path:** `tdev/core/registry.py` and the runtime file `.tdev/registry.json`.
     **Expected Output:** A working `AgentRegistry` class or module that the rest of the system can call to lookup agent/tool classes by name. For example, after calling a registry `register()` on a new `SampleAgent`, the `.tdev/registry.json` might contain:

   ```json
   {
       "SampleAgent": {
           "type": "agent",
           "class": "tdev.agents.sample_agent.SampleAgent"
       }
   }  
   ```

   The registry code can import that class dynamically when needed to instantiate the agent. The CLI `register` command will utilize this to populate the registry from a file path. In local development, this JSON file is the source of truth for available components.
   **Rationale:** The AgentRegistry is a cornerstone of the meta-agent design, providing a unified reference to all components. Core agents like the WorkflowExecutor or Planner will query this registry to resolve agent names to actual classes at runtime. Implementing a minimal registry now allows the system to scale by simply adding entries for new agents/tools. It also enables dynamic discovery – e.g., listing available agents or ensuring that when the WorkflowExecutor runs a step, it can find the corresponding agent implementation. Storing the registry in a JSON file in `.tdev/` follows the design that local development uses a file-based registry, which is simple and transparent.

3. **Metadata Schema Definitions**
   **Description:** Define the schema (data model) for agent and tool metadata in code. Using a Python data class or Pydantic model (for future validation) can be helpful. For example, create a `AgentMeta` class with fields like `name`, `type`, `class_path`, `description`, etc., and a similar `ToolMeta` if needed. In this skeleton, we can keep it simple by using dictionaries internally (since the registry JSON structure is known), but having a clear schema will support documentation and future validation. Additionally, define a basic **input/output schema** representation for agents – for now this could just be notes or placeholders (since full schema validation is a future feature). For instance, allow registry entries to optionally include an `input_schema` or `output_schema` field (even if just stored and not enforced).
   **Directory Path:** `tdev/core/registry.py` (for schema definition or as separate `tdev/core/schema.py`).
   **Expected Output:** Clearly defined fields for agent/tool metadata, reflected in both code and the documentation. For instance, the documentation in AGENTS.md can list that an agent’s metadata includes “type: agent, class: import path, (future: input\_schema, output\_schema, etc.)”. The code might not fully utilize these yet, but the structure exists. The registry JSON and internal structures should at least incorporate `type`, `class` (and possibly `path` if pointing to file storage) for each entry.
   **Rationale:** Defining metadata schemas upfront ensures consistency across the system. As more agents/tools are added, everyone will follow the same format. It also makes the system self-descriptive: tools like the PlannerAgent can later use these metadata fields (e.g., tags or capabilities) to select appropriate agents. By planning for `input_schema` and `output_schema`, we acknowledge how agents’ interfaces could be described, even if we don't implement full validation now – this aligns with planned extensions in the design. In summary, a schema-driven approach makes the architecture robust and easier to extend or integrate with other systems.

4. **Register Core Example Agents/Tools (Skeleton Entries)**
   **Description:** Populate the registry with a few example components to illustrate usage. Create minimal implementations for one Agent and one Tool to test the flow end-to-end. For example, add a simple `EchoTool` (that just returns the input it receives) and an `EchoAgent` (that uses EchoTool or simply echoes a message). These can be placed in `tdev/tools/echo_tool.py` and `tdev/agents/echo_agent.py`. Use the `AgentRegistry.register()` method to add them (this could be done at startup or via the CLI register command). Ensure their entries appear in `.tdev/registry.json`.
   **Directory Path:** `tdev/agents/echo_agent.py`, `tdev/tools/echo_tool.py`, and update in `tdev/core/registry.py` or via CLI.
   **Expected Output:** Two basic components in the system to validate the infrastructure. For instance, `EchoTool` with a `use(input_data)` returning the same data, and `EchoAgent(Agent)` with a `run(input_data)` that perhaps calls the tool or just prints a confirmation. The registry will contain:

   ```json
   {
       "EchoTool": { "type": "tool", "class": "tdev.tools.echo_tool.EchoTool" },
       "EchoAgent": { "type": "agent", "class": "tdev.agents.echo_agent.EchoAgent" }
   }  
   ```

   With these present, one could compose a workflow like \[EchoAgent] and run it to see the flow working.
   **Rationale:** Having at least one agent and tool defined verifies that the registry, base classes, and CLI are working together. It also provides a template for developers on how an agent/tool is implemented and registered. These simple examples act as a smoke test for the skeleton: for example, `tdev compose --name echo-flow --steps EchoAgent` and `tdev run echo-flow` can demonstrate that the system finds `EchoAgent` via the registry and executes its `run` method. This builds confidence that the core infrastructure is correctly wired.

### Phase 4: Workflow Definition and Execution

1. **Design Workflow Definition Format**
   **Description:** Decide on a representation for workflows (likely JSON or YAML). Define a **Workflow** class or data structure to hold a workflow’s metadata: an ID or name, a list of steps, each step referencing an agent (by name or by reference), and possibly input/output mappings between steps. For the skeleton, this can be a simple list of agent names in order (assuming linear workflows). Create a parser/serializer that can load a workflow file from `.tdev/workflows/<name>.yaml` or `.json` and instantiate a Workflow object, and vice versa. Use the example from the Planner spec as a guideline for fields (ID, steps with agent names, etc.), though in minimal form we might not include complex mappings.
   **Directory Path:** `tdev/core/workflow.py` (for the Workflow class and load/save functions).
   **Expected Output:** A `Workflow` class that can represent a sequence of steps. For example:

   ```python
   class Workflow:  
       def __init__(self, id:str, steps: List[str]):  
           self.id = id  
           self.steps = steps  # e.g. ["AgentA", "AgentB"]  
   ```

   Additionally, functions like `load_workflow(file_path) -> Workflow` and `save_workflow(workflow) -> file` should be implemented. The workflow files themselves (in `.tdev/workflows/`) will contain structured data; for instance, `sample-flow-v1.yaml` might look like:

   ```yaml
   id: sample-flow-v1  
   steps:  
     - agent: EchoAgent  
   ```

   (and we can extend the format later to include inputs/outputs).
   **Rationale:** Formalizing the workflow definition is crucial for the system to understand what to execute. By creating a Workflow abstraction, we separate how workflows are stored from how they are run. This makes it easier to evolve the format (add new fields like branching, inputs/outputs) without changing the execution logic. It also means tools like the PlannerAgent can output a workflow definition in this format, and the executor can consume it. Having a clear minimal format now provides a foundation for more complex workflow compositions later.

2. **Implement Workflow Executor Agent (Stub)**
   **Description:** Create the **WorkflowExecutorAgent** – an agent responsible for executing a given Workflow step by step. In this minimal version, implement it as a class (e.g. `tdev/agents/workflow_executor_agent.py`) that inherits from `Agent` base. Its `run(workflow: Workflow)` method will iterate through the workflow’s steps and for each step: look up the agent name in the AgentRegistry, instantiate the agent, and call that agent’s `run` method with appropriate input. Because we don’t have real data flow yet, we can simplify by calling each agent with a static or dummy input (or no input), and perhaps capturing a dummy output. Ensure to log each step’s execution for traceability. After completing all steps, the WorkflowExecutor can return a summary or just indicate completion.
   **Directory Path:** `tdev/agents/workflow_executor_agent.py`, and ensure this class is registered in the AgentRegistry (type: agent).
   **Expected Output:** A stubbed `WorkflowExecutorAgent` that can be invoked via the CLI `tdev run` command. For example, if a workflow “echo-flow” consists of step `[EchoAgent]`, when `tdev run echo-flow` is executed, the WorkflowExecutorAgent loads the workflow, finds “EchoAgent” in the registry, instantiates `EchoAgent`, and calls its `run` method. The console output/log might be:

   ```
   Executing workflow echo-flow-v1:  
    - Step 1: Running EchoAgent... (completed)  
   Workflow execution finished.  
   ```

   (EchoAgent’s run may just print a message or return a dummy value.) The executor agent doesn’t need to handle failures or complex logic yet – just the linear sequence.
   **Rationale:** The WorkflowExecutorAgent is the component that actually **realizes** a composed solution by invoking the constituent agents in order. Implementing it, even in stub form, is a critical part of the “skeleton” – it turns the static definitions (in the registry and workflow files) into dynamic behavior. By using the registry to resolve each step’s agent, we validate that our registry design works for runtime lookup. This also sets up the pattern for future enhancements (passing real data between steps, error handling, logging, etc.). In essence, this task connects the pieces: CLI -> Workflow definition -> Registry -> Agent execution, showing a complete (if simplistic) flow.

3. **Stub Core Planning/Evaluation Agents (Placeholders)**
   **Description:** As part of the infrastructure, include placeholder classes for other core agents that will exist in the full system, namely **ClassifierAgent**, **PlannerAgent**, and **EvaluatorAgent**. These can be created in `tdev/agents/` with minimal implementation: e.g. `ClassifierAgent` with a `run(input)` that always classifies the input file as a certain type (tool/agent) without real analysis, or returns a dummy structure; `PlannerAgent` with a `run(input)` that perhaps calls a very simple rule or returns a fixed workflow plan (since in the future it would generate workflows); `EvaluatorAgent` can just return a fixed “score” or approval. We do not integrate them deeply now, but they should be registered in the AgentRegistry for future use.
   **Directory Path:** `tdev/agents/classifier_agent.py`, `tdev/agents/planner_agent.py`, `tdev/agents/evaluator_agent.py`.
   **Expected Output:** Basic class definitions for these agents. For example:

   ```python
   class ClassifierAgent(Agent):  
       def run(self, target_file:str):  
           # TODO: real classification; for now, assume it's an "agent"  
           return {"type": "agent", "name": "UnknownAgent"}  
   ```

   These stubs would be added to the registry (perhaps with a special flag or simply type=agent). They might not be invoked in the current CLI commands except possibly via a future `tdev classify` (which could call ClassifierAgent.run on a given file). No complex logic, just enough so that when these are later implemented, all structural hooks (like CLI and registry) are already in place.
   **Rationale:** By including the core agents of the system in the initial skeleton, we ensure the architecture accounts for them from the start. Even though they are not fully functional, their presence influences how others are built (e.g., knowing a PlannerAgent will produce workflow JSON means our Workflow class should be compatible with that format). It also allows writing documentation (ARCHITECTURE.md, AGENTS.md) that references these agents and their roles in the system. In short, these placeholders act as signposts for where critical logic will live, and they make it easier to implement the full behaviors later without changing the surrounding infrastructure.

### Phase 5: Testing Framework (Agent Tester) Integration

1. **Implement AgentTesterAgent (Test Runner Stub)**
   **Description:** Create an **AgentTesterAgent** class (e.g. `tdev/agents/agent_tester_agent.py`) that can test other agents or tools. In this minimal version, the AgentTesterAgent will take as input the name of a target agent/tool and perhaps an example input, then execute that target’s `run` method and compare the output to an expected result. Since we are skeletonizing, we can simplify: implement a method `test(target_name, sample_input, expected_output)` that loads the target from the AgentRegistry, runs it, and just prints whether the output matches the expected (or always return “pass” for now). Also add a CLI command `tdev test <AgentName>` that invokes AgentTesterAgent on a given agent (with some hard-coded test case or a simple echo test).
   **Directory Path:** `tdev/agents/agent_tester_agent.py` and CLI integration in `tdev/cli.py`.
   **Expected Output:** The ability to run `tdev test SomeAgent` from the command line and get a result of a test. For instance, if `SomeAgent` is in the registry and simply returns a constant, AgentTesterAgent will call it and verify the output. The CLI might output: `Testing SomeAgent... PASSED` (or a basic JSON result). Internally, AgentTesterAgent would follow a flow: lookup class in registry -> instantiate -> run with sample input -> compare result (very trivial comparison in this skeleton). We should also update `.tdev/registry.json` to include an entry for AgentTesterAgent itself, so it can be invoked via workflows if needed.
   **Rationale:** Quality assurance is a key part of the development workflow. Incorporating a test runner agent from the start emphasizes testability of each component. The AgentTesterAgent concept ensures **component-level quality assurance** in T-Developer. By stubbing it now, we can demonstrate how one agent (the tester) can load and validate another agent via the registry, which is a powerful meta capability. It also sets up the CLI for integration in CI pipelines (e.g., one could imagine running `tdev test all` to test all agents). In the skeleton, the implementation is minimal, but it provides the structure needed for test-driven development of agents going forward – aligning with the goal of enabling safe, reliable automation.

2. **Basic Test Cases and CI Setup**
   **Description:** Add a couple of basic unit tests in the `tests/` directory to verify that the skeleton components work as expected. For example, test that the AgentRegistry can register an agent and retrieve it, test that the WorkflowExecutorAgent correctly iterates through a simple workflow, and test that AgentTesterAgent returns “pass” for a known correct output. These tests can be run with `pytest`. Also, if possible, include a simple GitHub Actions workflow or note to run tests (depending on whether CI is in scope).
   **Directory Path:** `tests/test_registry.py`, `tests/test_workflow_executor.py`, `tests/test_agent_tester.py` (etc., as needed).
   **Expected Output:** A few passing tests confirming the minimal infrastructure functions. For instance, `test_registry.py` might create a dummy agent class, register it, and assert that it’s listed in the registry. `test_workflow_executor.py` could create a dummy workflow with one echo agent and assert that running it produces the expected log/output. These tests act as usage examples as well.
   **Rationale:** Including tests at this stage serves two purposes: it validates the design decisions (catching any integration issues early), and it reinforces a culture of testing. Since one of T-Developer’s components is itself a test runner, having actual tests in the project is fitting. This also ensures that new contributors (or automated CI) can verify the skeleton’s integrity as they add features. Essentially, it proves that the “minimal infrastructure” is not only present but also functional and ready to be built upon.

### Phase 6: Documentation and Final Touches

1. **Write Architecture and Design Documents**
   **Description:** Now that the code skeleton is in place, document it thoroughly. Write the **ARCHITECTURE.md** to reflect the new system design: describe how the meta-agent orchestrator concept works, enumerate the core agents (Classifier, Planner, Evaluator, WorkflowExecutor, Tester) and tools, and explain the data flow from CLI to execution (for example, how a `tdev run` triggers WorkflowExecutor which looks up agents in the registry, etc.). Include diagrams or ascii charts if helpful. Ensure to mention how the Registry is the central reference map and how the .tdev files (registry.json, workflow definitions) are used. Also cover deployment context (EC2, non-container, possibly how a user would run the CLI on EC2 or trigger it).
   **Directory Path:** `docs/ARCHITECTURE.md` (or root `ARCHITECTURE.md`).
   **Expected Output:** A comprehensive architecture document checked into the repository. It should serve as a reference for any developer or stakeholder to understand the system’s structure. For example, it would clarify that *“T-Developer’s brain is a MetaAgent orchestrator that coordinates specialized agents in sequence to fulfill a development task. The AgentRegistry acts as the directory of all available skills (agents/tools), enabling the orchestrator and others to dynamically discover and invoke them.”* This document may also highlight how the design allows easy addition of new agents/tools (modularity).
   **Rationale:** Architecture documentation is essential for knowledge sharing and future development. Given that the system is designed to be extendable (meta-agent managing other agents), having a clear description prevents confusion and ensures that new contributors understand the relationships and responsibilities of each component. It also records the reasoning behind the chosen design (why a registry, why a CLI-centric approach, etc.), which is useful for on-boarding and for revisiting design decisions.

2. **Document Agent/Tool Development Guide**
   **Description:** Draft the **AGENTS.md** and **TOOLS.md** files. In AGENTS.md, explain how to create a new agent in detail: the developer should subclass the Agent base, implement the `run` method, decide on any tool dependencies or input/output, then register the agent (via CLI or directly editing the registry). Provide an example using one of the skeleton agents as reference. In TOOLS.md, similarly outline how to write a new tool (subclass Tool base, implement its function, register it). Be sure to describe the metadata fields and the need to update the AgentRegistry (or use `tdev register`). Also, mention any conventions (e.g., naming, one file per agent, etc.).
   **Directory Path:** `docs/AGENTS.md`, `docs/TOOLS.md`.
   **Expected Output:** Two documentation files that serve as developer guides for extending the system. For instance, **AGENTS.md** would contain sections like “Agent Roles in T-Developer”, “Steps to Implement a New Agent” (with code snippets from the EchoAgent example), and “Registering the Agent in the Registry”. **TOOLS.md** would likewise have “What is a Tool vs an Agent” and “Steps to Create a Tool” with an example (perhaps an LLM-calling tool as a template). These docs should be written in a clear, tutorial-like style so that even someone new to the project can follow them to successfully add a component.
   **Rationale:** Since one of the project’s goals is to **easily add further agents/tools**, providing explicit documentation for that process is critical. These guides reduce the learning curve and help maintain consistency (everyone adds new agents in the recommended way). They also encourage contributions by demystifying the internals – showing that with the base classes and registry, adding a new capability is straightforward. In sum, these documents ensure the architecture’s extensibility is realized in practice by guiding users through it.

3. **Document Workflows and CLI Usage**
   **Description:** Complete the **WORKFLOWS.md** guide to cover how to define workflows (both manually and via the Planner in the future). Include an example of writing a simple workflow YAML by hand, explaining each part (workflow id, steps list, etc.), and how to run it with `tdev run`. Additionally, write **CLI\_USAGE.md** which can double as a user manual for the CLI. This should list each CLI command, its purpose, and examples. For instance, document `tdev init agent` and `tdev init tool` with their options, `tdev classify` usage (even if it’s stubbed, describe intended behavior), `tdev register <path>` to add to registry, `tdev compose` and `tdev run` for workflows, `tdev test` for running tests on an agent, etc. Mention any configuration or environment prerequisites if needed (like requiring AWS credentials if that were needed for future deploy commands, though for now deploy is stubbed).
   **Directory Path:** `docs/WORKFLOWS.md`, `docs/CLI_USAGE.md`.
   **Expected Output:** Two well-structured docs. **WORKFLOWS.md** might include a sample JSON/YAML workflow (perhaps borrowing the format from our Planner spec example) and a step-by-step explanation of how the WorkflowExecutor processes it. **CLI\_USAGE.md** will read like a help manual, possibly organized by category of commands (Initialization, Composition/Execution, Testing, Deployment). It should reflect the current state (noting which commands are fully functional vs placeholders). Cross-reference relevant docs (e.g., CLI guide might refer readers to Agents guide for understanding what agents to init).
   **Rationale:** These documents serve the dual purpose of guiding end-users and informing developers. Workflows are a new concept for users, so a clear explanation prevents misuse and errors in composition. The CLI usage doc ensures users can actually leverage the tool effectively, which is important even at an early stage – it invites feedback and further testing. Moreover, having these docs now means as the commands and workflow features evolve, the documentation can be incrementally updated, rather than written from scratch later. It’s part of delivering a polished skeleton, not just code but also how to use that code.

4. **Review and Refine**
   **Description:** Do a final pass over the whole project for coherence. This includes updating the main **README.md** to reflect the current state of the project (what it is, how to install/run the CLI on EC2, basic example usage). Ensure that the README links to the deeper documentation files for details. Remove or revise any legacy content that no longer applies (since earlier versions had a FastAPI service, the README should now emphasize the CLI and meta-agent approach). Also, check that all placeholders or “TODO” comments in code have corresponding tasks in docs or issues for future implementation, so it’s clear they are intentional. Optionally, set up a version tag or branch for this skeleton (like v2.0 skeleton).
   **Directory Path:** Project root (README.md, cleanup across repository).
   **Expected Output:** A clean, cohesive project artifact representing the minimal viable T-Developer framework. The README will provide a concise overview and quickstart (e.g., how to run an example workflow on EC2). All tests should be passing, and running `tdev --help` should show the commands matching the documented ones. The code should be organized with no dead links (e.g., registry file path correct) and the documentation should accurately reflect the code.
   **Rationale:** This step ensures that the skeleton isn’t just internally consistent but also externally presentable. Since the aim is to bootstrap further development, new team members or open-source contributors should be able to read the README, understand the vision from the architecture doc, follow the setup instructions, and experiment with the CLI (even if features are stubbed). A polished skeleton with good documentation makes the project approachable and sets a high standard for quality from the beginning. It also serves as a baseline to measure progress going forward – any new feature should maintain the coherence established here.

---

By completing the above phases, we will have a minimal but functional skeleton of the T-Developer system. This skeleton includes the critical infrastructure (CLI, registry, workflow engine, testing stub) and thorough documentation, providing a strong foundation upon which the richer capabilities (actual planning logic, LLM integration, cloud deployment, etc.) can be built. Each phase builds on the previous ones, ensuring that at every step the system remains runnable and understandable.
