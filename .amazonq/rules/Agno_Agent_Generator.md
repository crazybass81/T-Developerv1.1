# T‑Developer Agent Generator (Agno)

This document explains the agent-generation system, referred to as "agno," within the T‑Developer architecture. It details what agno is, how it works, and how it integrates with other components to automatically produce new Tools or Agents based on rules and requirements.

---

## 1. Introduction to Agno

**Agno** (Agent Generator) is the subsystem in T‑Developer responsible for automatically creating new agent definitions when the existing library does not have what is needed for a given task. It takes high-level specifications or goals as input and outputs ready-to-use agent code and metadata.

Agno works based on rules and patterns to ensure generated agents meet the system's standards. It serves as the "creativity engine" that allows T‑Developer to expand its capabilities autonomously by designing new components on demand.

The primary implementation of agno is the `AutoAgentComposer` component, which handles the end-to-end process of agent generation, from specification to code to registration.

## 2. Agno Workflow & Components

The agno system operates through a four-stage process:

### 2.1 Specification Intake

Agno accepts descriptions of desired capabilities in two formats:

**Natural Language Prompt:**
```text
Create an agent that scans a QR image and returns the associated username.
```

**Structured Specification:**
```json
{
  "goal": "Extract text from a PDF and summarize it",
  "input": "pdf_url",
  "tools": ["PDFExtractorTool", "GPTCallerTool"],
  "output": "summary"
}
```

### 2.2 Analysis & Planning

Agno analyzes the specification to:
- Extract the core functionality required
- Identify input and output parameters
- Determine which existing tools or agents could be leveraged
- Plan the logical flow of the new agent

During this phase, agno may query the `AgentRegistry` to find suitable tools or agents that can be composed to fulfill the requirement.

### 2.3 Code Generation

Based on the analysis, agno generates:

**Agent Metadata:**
```json
{
  "name": "QRCodeResolverAgent",
  "type": "agent",
  "input": "image",
  "output": "username",
  "tools": ["QRCodeReaderTool", "UserDBLookupTool"]
}
```

**Agent Code:**
```python
@agent
def qr_resolver(image):
    qr_code = QRCodeReaderTool().run(image)
    user = UserDBLookupTool().run(qr_code)
    return user
```

The generated code follows T‑Developer's conventions, including the appropriate decorator (`@agent`) and a clean, functional structure.

### 2.4 Registration & Classification

Finally, agno:
1. Sends the generated code to the `ClassifierAgent` to verify its structure and determine its brain count and reusability tier
2. Registers the new agent in the `AgentRegistry` with its metadata
3. Returns the agent definition to the caller (e.g., the `PlannerAgent` or CLI)

## 3. Rules and Templates in Generation

Agno uses several rule sets and templates to guide the generation process:

### Domain-Specific Rules

```yaml
generation_rules:
  - domain: "image_processing"
    if_contains: ["image", "scan", "photo", "picture"]
    suggest_tools: ["ImageLoaderTool", "OCRTool", "ImageAnalysisTool"]
  
  - domain: "text_generation"
    if_contains: ["generate", "create text", "write"]
    suggest_tools: ["GPTCallerTool", "TemplateFillerTool"]
  
  - domain: "data_storage"
    if_contains: ["save", "store", "upload"]
    suggest_tools: ["S3UploaderTool", "DatabaseWriterTool"]
```

### Code Templates

Agno maintains templates for common agent patterns:

**Simple Tool Wrapper:**
```python
@agent
def {{agent_name}}({{input_params}}):
    result = {{tool_name}}().run({{input_params}})
    return result
```

**Sequential Tool Chain:**
```python
@agent
def {{agent_name}}({{input_params}}):
    intermediate = {{first_tool}}().run({{input_params}})
    result = {{second_tool}}().run(intermediate)
    return result
```

**Conditional Logic:**
```python
@agent
def {{agent_name}}({{input_params}}):
    if {{condition}}:
        result = {{tool_a}}().run({{input_params}})
    else:
        result = {{tool_b}}().run({{input_params}})
    return result
```

These templates ensure that generated agents follow consistent patterns and best practices.

## 4. Agno's Role in Orchestration

Agno is invoked in two primary scenarios:

### 4.1 On-Demand by PlannerAgent

When the `PlannerAgent` is designing a workflow and identifies a missing capability:

1. PlannerAgent determines that no existing agent can perform a required step
2. PlannerAgent requests the orchestrator to generate a new agent
3. Orchestrator calls agno with a specification of the needed capability
4. Agno generates the agent and registers it
5. PlannerAgent incorporates the new agent into the workflow

This allows T‑Developer to autonomously fill gaps in its capabilities during workflow planning.

### 4.2 Direct Invocation via CLI

Developers can manually invoke agno through the CLI:

```bash
tdev generate agent --name QRCodeResolverAgent --goal "Scan QR codes and resolve usernames"
```

This creates a new agent based on the specified goal and saves it to the local development environment.

## 5. Integration Points

Agno integrates with several other components in the T‑Developer ecosystem:

### 5.1 AgentRegistry/AgentStore

- Agno queries the registry to check for existing agents with similar functionality
- Agno registers newly generated agents in the store
- The registry provides metadata about available tools that agno can use in new agents

### 5.2 ClassifierAgent

- Agno sends generated code to the ClassifierAgent for analysis
- ClassifierAgent determines the agent's type, brain count, and reusability tier
- This classification is included in the agent's metadata

### 5.3 Q-Developer / Code Refinement

- Agno may integrate with Q-Developer for code refinement
- Generated code can be reviewed and improved before final registration
- This creates a human-in-the-loop or AI-assisted refinement process

### 5.4 DevSecOps Pipeline

- Newly generated agents can trigger CI/CD workflows
- Agno can create pull requests for new agents via GitHub integration
- Tests are automatically generated and run against new agents

## 6. Structure of Agno (Internals)

Internally, the AutoAgentComposer (agno) consists of several subcomponents:

### 6.1 Spec Parser

Responsible for interpreting natural language or structured specifications and extracting key requirements:
- Goal/purpose
- Input/output parameters
- Domain hints
- Suggested tools

### 6.2 Tool Selector

Identifies the most appropriate tools or agents to use in the new agent:
- Queries AgentRegistry for available tools
- Matches tools to requirements
- Considers reusability and reliability scores
- Optimizes for minimal complexity

### 6.3 Code Generator

Creates the actual agent code:
- Selects appropriate code template
- Fills in template with selected tools and logic
- Ensures proper error handling
- Adds documentation comments

### 6.4 Classifier/Registrar

Handles the final steps of agent creation:
- Sends code to ClassifierAgent
- Creates metadata record
- Registers agent in AgentRegistry
- Returns complete agent definition

## 7. Example Generation Scenario

Let's walk through a complete example of agno generating a new agent:

### User Request

A user or PlannerAgent requests:
```
Create an agent that scans a QR image and returns the associated username.
```

### Spec Parsing

Agno identifies:
- Input: image (QR code)
- Output: username
- Required capabilities: QR code scanning, user lookup

### Tool Selection

Agno queries the AgentRegistry and finds:
- `QRCodeReaderTool`: Extracts text from QR images
- `UserDBLookupTool`: Looks up usernames from identifiers

### Code Generation

Agno selects the "Sequential Tool Chain" template and generates:

```python
@agent
def qr_resolver(image):
    # Extract text from QR code image
    qr_code = QRCodeReaderTool().run(image)
    # Look up username associated with the code
    user = UserDBLookupTool().run(qr_code)
    return user
```

### Classification & Registration

Agno sends the code to ClassifierAgent, which determines:
- Type: Agent (has one decision point)
- Brain count: 1
- Reusability: B (high)

Agno creates the metadata:

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

The agent is registered in the AgentRegistry and is now available for use in workflows.

### 예제 생성 시나리오 (Korean)

사용자 또는 PlannerAgent가 "QR 이미지를 스캔하여 관련 사용자 이름을 반환하는 에이전트 생성"을 요청합니다. Agno는 입력(QR 코드 이미지)과 출력(사용자 이름)을 식별하고, 필요한 기능(QR 코드 스캔, 사용자 조회)을 파악합니다. AgentRegistry에서 `QRCodeReaderTool`과 `UserDBLookupTool`을 찾아 "순차적 도구 체인" 템플릿을 선택하여 코드를 생성합니다. ClassifierAgent는 이를 분석하여 유형(Agent), 브레인 수(1), 재사용성(B-높음)을 결정하고, 메타데이터를 생성하여 AgentRegistry에 등록합니다.

## 8. Future Considerations

Agno has several planned enhancements:

### 8.1 Test Generation

Future versions will automatically generate test cases alongside new agents:
- Input/output pairs for basic functionality
- Edge case tests for robustness
- Integration tests with dependent components

### 8.2 Logic Type Selection

Users will be able to specify the type of decision logic:
- Rule-based (explicit conditions)
- LLM-based (using language models for decisions)
- Hybrid approaches

### 8.3 Improvement Loop

An integration with `tdev refine` will enable iterative improvement:
1. Generate initial agent
2. Test and evaluate performance
3. Automatically refine based on results
4. Repeat until quality threshold is met

### 8.4 Multi-File Output

Agno will support generating more complex structures:
- `.py` code file
- `.meta.json` metadata file
- `.test.json` test suite
- `.md` documentation

---

## 에이전트 생성기 (Agno) 요약 (Korean Summary)

Agno(Agent Generator)는 T‑Developer 내에서 기존 라이브러리에 필요한 기능이 없을 때 새로운 에이전트 정의를 자동으로 생성하는 서브시스템입니다. 자연어 프롬프트나 구조화된 명세를 입력으로 받아 사용 가능한 에이전트 코드와 메타데이터를 출력합니다.

Agno는 명세 수집, 분석 및 계획, 코드 생성, 등록 및 분류의 4단계 프로세스로 작동합니다. 도메인별 규칙과 코드 템플릿을 사용하여 일관된 패턴과 모범 사례를 따르는 에이전트를 생성합니다.

Agno는 PlannerAgent가 워크플로우를 설계하는 동안 누락된 기능을 식별할 때 호출되거나 CLI를 통해 직접 호출될 수 있습니다. AgentRegistry/AgentStore, ClassifierAgent, Q-Developer, DevSecOps 파이프라인과 통합되어 T‑Developer 생태계의 핵심 부분으로 기능합니다.