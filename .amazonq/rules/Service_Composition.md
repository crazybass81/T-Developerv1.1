# T‑Developer Service Composition Mechanisms

This document explains how T‑Developer composes services (workflows) from available agents and tools. It covers how a user's request or goal is translated into a runnable SaaS service via the planning, orchestration, and workflow execution process.

---

## 1. Overview of Composition

In T‑Developer, **service composition** refers to the process of building a **workflow** (a series of agent/tool steps) that, when executed, fulfills a user's SaaS request. This composition process is automated through the PlannerAgent and related components.

The key aspects of service composition include:
- Breaking down a high-level goal into discrete steps
- Selecting appropriate agents/tools for each step
- Defining the data flow between steps
- Creating an executable workflow definition

The output of composition is a **workflow definition** (JSON/YAML) that outlines the service's logic flow and can be executed by the WorkflowExecutorAgent.

## 2. PlannerAgent's Role

The **PlannerAgent** is the core component responsible for service composition. It follows these steps to transform a goal into a workflow:

### 2.1 Goal Parsing

The PlannerAgent begins by parsing the input, which can be:

**Natural Language Goal:**
```text
Build a service that summarizes documents and uploads them to S3.
```

**Structured Goal JSON:**
```json
{
  "goal": "문서 요약 후 클라우드에 업로드",
  "inputs": ["document"],
  "output": "s3_url"
}
```

The PlannerAgent extracts key information from the goal:
- Required functionality (summarization, uploading)
- Input types (document)
- Expected output (S3 URL)

### 2.2 Agent Registry Query

The PlannerAgent queries the **AgentRegistry/AgentStore** to find candidate components for each sub-task:
- For summarization: `SummarizerAgent`
- For uploading: `S3UploaderAgent`

It considers factors such as:
- Agent capabilities and purpose
- Input/output compatibility
- Reusability tier
- Reliability score

### 2.3 Task Decomposition

The PlannerAgent divides the overall task into sequential or parallel steps:
1. Summarize the document
2. Upload the summary to S3

This decomposition can be done through:
- Rule-based analysis of the goal
- Pattern matching with known workflows
- LLM assistance for complex goals

### 2.4 Agent Selection

For each step, the PlannerAgent selects the most appropriate agent or tool from the candidates based on:
- Compatibility with the step's requirements
- Agent score (quality, stability, reusability)
- Resource efficiency
- Version compatibility

### 2.5 Workflow Definition Generation

Finally, the PlannerAgent produces a workflow definition in JSON format:

```json
{
  "id": "summarize-upload-flow-v1",
  "inputs": { "doc": "string" },
  "steps": [
    {
      "id": "summarize",
      "agent": "SummarizerAgent",
      "input_from": "doc",
      "output_to": "summary"
    },
    {
      "id": "upload",
      "agent": "S3UploaderAgent",
      "input_from": "summary",
      "output_to": "s3_url"
    }
  ],
  "outputs": {
    "result": "s3_url"
  }
}
```

This workflow definition specifies:
- The input to the workflow (`doc`)
- Each step with its agent and data mappings
- How data flows between steps
- The final output of the workflow

## 3. Workflow Definition Schema

The formal schema of a workflow includes these key elements:

### 3.1 ID (식별자)
A unique identifier for the workflow, often including a version suffix (e.g., `summarize-upload-flow-v1`).

### 3.2 Description (설명)
A summary of the workflow's purpose and function.

### 3.3 Inputs (입력 정의)
The structure of input values received from the user:
```json
"inputs": {
  "query": "string",
  "max_length": "number"
}
```

### 3.4 Steps (단계)
An array of execution steps, each mapping an agent to part of the data flow:
```json
"steps": [
  {
    "id": "step_name",
    "agent": "AgentName",
    "input_from": "source_key",
    "output_to": "destination_key"
  }
]
```

Each step includes:
- `id`: A unique identifier for the step
- `agent`: The name of the agent or tool to execute
- `input_from`: Where to get input data (from workflow inputs or previous step outputs)
- `output_to`: Where to store the step's output in the context

### 3.5 Outputs (출력 정의)
The final output returned from the workflow:
```json
"outputs": {
  "result": "final_step_output"
}
```

### 3.6 Advanced Fields (Optional)
Future extensions may support:
- `condition`: Conditional execution of steps
- `parallel`: Parallel execution of steps
- `tool`: Direct use of tools in steps
- `workflow_ref`: Reference to a sub-workflow

## 4. Service Composition Process

The end-to-end process of service composition follows this sequence:

1. **User Request**: A user submits a goal or structured specification
2. **Classification**: If code is provided, the ClassifierAgent analyzes it
3. **Planning**: The PlannerAgent generates one or more candidate workflows
4. **Evaluation**: The EvaluatorAgent scores each workflow on quality, efficiency, etc.
5. **Selection**: The best workflow is chosen based on evaluation scores
6. **Refinement (Optional)**: If no workflow meets quality thresholds, the PlannerAgent may refine its approach
7. **Storage**: The final workflow definition is stored for execution and future reference
8. **Execution**: The WorkflowExecutorAgent runs the workflow with user inputs

This process may include iterative refinement:
- If the EvaluatorAgent finds issues with a workflow, it provides feedback
- The PlannerAgent uses this feedback to generate an improved workflow
- This cycle continues until a satisfactory workflow is produced or a maximum iteration count is reached

## 5. Integration with Auto-Generation

When the PlannerAgent cannot find a suitable agent for a required step, it can integrate with the agent generation system (agno):

1. PlannerAgent identifies a capability gap (e.g., no agent can perform OCR on an image)
2. PlannerAgent requests the orchestrator to generate a new agent
3. Orchestrator calls the AutoAgentComposer (agno) with a specification
4. AutoAgentComposer generates a new agent (e.g., `ImageOCRAgent`)
5. The new agent is registered in the AgentRegistry
6. PlannerAgent incorporates the new agent into the workflow

This dynamic agent generation capability makes T‑Developer's service composition highly extensible, allowing it to address new requirements without manual intervention.

## 6. Execution of Composed Service

After composition, the workflow definition is handed off to the **WorkflowExecutorAgent**, which:

1. Loads the workflow definition
2. Initializes the execution context with user inputs
3. Executes each step in sequence:
   - Resolves the agent for the step
   - Extracts inputs from the context
   - Calls the agent with the inputs
   - Stores the output in the context
4. Returns the final output as defined in the workflow

The workflow definition is typically stored in a repository or database for:
- Reuse in future requests
- Version tracking
- Audit and analysis
- Sharing across environments

## 7. Example Scenario

Let's walk through a complete service composition example:

### User Request
```
Build a policy recommendation system for young entrepreneurs.
```

### Planning Process

1. The PlannerAgent analyzes the request and identifies three main tasks:
   - Scrape policy documents
   - Cluster similar policies
   - Generate chat-based recommendations

2. It queries the AgentRegistry and finds:
   - `ScraperAgent`: Can retrieve policy documents from websites
   - `ClusterAgent`: Can group similar documents
   - `ChatAgent`: Can generate conversational responses

3. The PlannerAgent creates a workflow definition:

```json
{
  "id": "policy-match-flow-v1",
  "description": "Policy recommendation system for entrepreneurs",
  "inputs": {
    "query": "string"
  },
  "steps": [
    {
      "id": "scrape",
      "agent": "ScraperAgent",
      "input_from": "query",
      "output_to": "raw_policies"
    },
    {
      "id": "cluster",
      "agent": "ClusterAgent",
      "input_from": "raw_policies",
      "output_to": "grouped_policies"
    },
    {
      "id": "chat",
      "agent": "ChatAgent",
      "input_from": "grouped_policies",
      "output_to": "final_response"
    }
  ],
  "outputs": {
    "result": "final_response"
  }
}
```

4. The EvaluatorAgent reviews the workflow and confirms it is complete and efficient.

5. The WorkflowExecutorAgent executes the workflow with the user's query.

6. The result is a policy recommendation tailored to young entrepreneurs.

### 예제 시나리오 (Korean)

사용자가 "청년 창업가를 위한 정책 추천 시스템 구축"을 요청합니다. PlannerAgent는 요청을 분석하여 정책 문서 스크래핑, 유사 정책 클러스터링, 채팅 기반 추천 생성이라는 세 가지 주요 작업을 식별합니다. AgentRegistry에서 ScraperAgent, ClusterAgent, ChatAgent를 찾아 워크플로우 정의를 생성합니다. EvaluatorAgent가 워크플로우를 검토하여 완전하고 효율적인지 확인한 후, WorkflowExecutorAgent가 사용자의 쿼리로 워크플로우를 실행합니다. 결과적으로 청년 창업가에게 맞춤화된 정책 추천이 제공됩니다.

## 8. Service Composition vs. Traditional Orchestration

T‑Developer's approach to service composition differs from traditional methods in several key ways:

### Dynamic vs. Static

Traditional orchestration typically involves manually defined workflows with fixed components. T‑Developer can dynamically generate workflows and even create new components on demand.

### Goal-Oriented vs. Step-Oriented

Traditional approaches focus on connecting predefined steps. T‑Developer starts with a high-level goal and automatically determines the necessary steps.

### Adaptive vs. Fixed

If requirements change or new capabilities are needed, T‑Developer can adapt by generating new agents or modifying workflows without manual intervention.

### Quality-Driven

T‑Developer incorporates quality evaluation into the composition process, ensuring that generated workflows meet predefined standards before execution.

---

## 서비스 구성 메커니즘 요약 (Korean Summary)

T‑Developer의 서비스 구성은 사용자의 요청이나 목표를 실행 가능한 SaaS 서비스로 변환하는 과정입니다. PlannerAgent는 목표를 분석하고, AgentRegistry에서 적절한 구성 요소를 찾고, 작업을 단계로 분해하고, 각 단계에 가장 적합한 에이전트를 선택하여 워크플로우 정의를 생성합니다.

워크플로우 정의는 ID, 설명, 입력, 단계, 출력을 포함하는 JSON 형식으로 생성됩니다. 각 단계는 에이전트와 데이터 매핑을 지정합니다. 서비스 구성 프로세스는 사용자 요청, 분류, 계획, 평가, 선택, 정제(선택 사항), 저장, 실행의 순서로 진행됩니다.

PlannerAgent가 필요한 단계에 적합한 에이전트를 찾을 수 없는 경우, 에이전트 생성 시스템(agno)과 통합하여 새 에이전트를 생성할 수 있습니다. 이 동적 에이전트 생성 기능은 T‑Developer의 서비스 구성을 매우 확장 가능하게 만들어 수동 개입 없이 새로운 요구 사항을 해결할 수 있습니다.