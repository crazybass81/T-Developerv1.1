# T‑Developer Glossary of Key Terms

This glossary defines all important terms and abbreviations used in the T‑Developer system design. Each term includes a concise definition in English and, where helpful, a Korean translation or equivalent term.

---

## Core Concepts

- **Tool** (코드 툴) – A "0-brain" component; a simple, reusable function with no internal decision logic. Tools are atomic operations that perform specific tasks.

- **Agent** (에이전트) – A "1-brain" component that encapsulates one decision or strategy, performing a specific role. It may use tools internally.

- **Team** (팀) – A "Multi-brain" composite; a group of agents working together under some coordination. Represents a complex workflow as one entity.

- **MetaAgent (Orchestrator)** (오케스트레이터) – The orchestrator agent that sequences other agents (Planner, Classifier, etc.) to achieve an end-to-end goal. Essentially the controller of the whole process.

## Specialized Agents

- **ClassifierAgent** (분류 에이전트) – Analyzes code to classify it as Tool/Agent/Team based on structure.

- **PlannerAgent** (플래너 에이전트) – Plans workflows by selecting and ordering agents/tools to meet a goal.

- **EvaluatorAgent (WorkflowEvaluator)** (평가 에이전트) – Evaluates and scores workflows or agents for quality and suitability.

- **WorkflowExecutorAgent** (워크플로우 실행 에이전트) – Executes a composed workflow step-by-step, managing inputs/outputs.

- **TestRunnerAgent** (에이전트 테스터) – Tests an agent or tool by running it with sample inputs and comparing outputs to expected results.

- **AutoAgentComposer (Agno)** (자동 에이전트 생성기) – Generates new agent or tool code from a description (the agent generation system).

- **AgentStore (Agent Registry)** (에이전트 스토어/레지스트리) – The centralized storage for agent definitions and metadata.

- **AgentVersionManager** (에이전트 버전 관리자) – A component that manages different versions of agents and can decide which version to deploy based on score or rules.

- **Q-Developer** (Q-Developer) – The autonomous developer assistant that can make changes according to the design documents.

## Other Terms

- **SaaS** (서비스형 소프트웨어) – Software as a Service, the type of application T-Developer assembles.

- **Brain** (브레인) – In this context, a "brain" means a decision-making point or logic branch within an agent. Used to measure complexity of agents/teams.

- **Composite Agent** (복합 에이전트) – An agent that is complex enough to be more than a single brain, but not structured as a formal Team. Has multiple decisions but no explicit coordinator.

- **Workflow** (워크플로우) – The JSON or YAML definition of a composed process (series of steps using agents/tools).

- **Service Instance** (서비스 인스턴스) – A deployed, executable instance of a workflow (with specific agents and configuration).

- **Agent (or Tool) Metadata** (에이전트 메타데이터) – The JSON record describing an agent/tool (name, type, path, etc.).

- **Agent Score** (에이전트 점수) – The composite score indicating an agent's quality/reliability.

- **Reusability** (재사용성) – A measure of how general-purpose an agent is (Tools = very high reusability, Teams = low). Often labeled A (highest) through E (lowest) or "high/low".

- **Reusability Tier** (재사용성 등급) – The classification of components based on reusability, from A (Tool, highest) to E (SaaS System Block, lowest).

- **AgentTestSuite** (에이전트 테스트 스위트) – A collection of test cases for validating an agent's behavior.

- **ExecutionSnapshot** (실행 스냅샷) – A record of a workflow execution, including inputs, outputs, and intermediate results.

- **TestRunHistoryStore** (테스트 실행 기록 저장소) – The storage system for test execution results.

- **AgentScoreModel** (에이전트 점수 모델) – The system for calculating agent quality, stability, and reusability scores.

- **DevSecOps** (DevSecOps) – Development, Security, and Operations; the integration of security practices into the development lifecycle.

- **CI/CD** (CI/CD) – Continuous Integration and Continuous Deployment; automated processes for testing and deploying code changes.

- **Workflow Definition** (워크플로우 정의) – The formal specification of a workflow, including steps, inputs, and outputs.

- **Service Composition** (서비스 구성) – The process of assembling a service from individual components.

- **Agent Squad** (에이전트 스쿼드) – A group of agents working together under orchestration to achieve a goal.

- **Agno** (Agno) – Short for "Agent Generator"; the system that automatically creates new agents.

- **Deployment Target** (배포 대상) – The environment where a service instance is deployed (Lambda, ECS, etc.).

- **Quality Gate** (품질 게이트) – A threshold that must be passed before a component can proceed to the next stage (e.g., deployment).

- **Rollback** (롤백) – The process of reverting to a previous version of a component or service.

- **Version** (버전) – A specific iteration of a component, identified by a version number or tag.

- **Semantic Versioning** (시맨틱 버전 관리) – A versioning scheme using major.minor.patch format.

- **Blue/Green Deployment** (블루/그린 배포) – A deployment strategy where two identical environments exist, and traffic is switched between them.

- **Canary Deployment** (카나리 배포) – A deployment strategy where a new version is gradually rolled out to a subset of users.

- **IAM** (IAM) – Identity and Access Management; controls permissions for AWS resources.

- **S3** (S3) – Simple Storage Service; AWS object storage service.

- **DynamoDB** (DynamoDB) – AWS NoSQL database service.

- **Lambda** (Lambda) – AWS serverless compute service.

- **ECS** (ECS) – Elastic Container Service; AWS container orchestration service.

- **CloudWatch** (CloudWatch) – AWS monitoring and observability service.

---

## 용어집 요약 (Korean Summary)

이 용어집은 T‑Developer 시스템 설계에 사용된 모든 중요한 용어와 약어를 정의합니다. 각 용어는 영어로 간결하게 정의되어 있으며, 필요한 경우 한국어 번역이나 동등한 용어가 제공됩니다.

핵심 개념으로는 내부 의사결정 로직이 없는 순수 함수인 **도구(Tool)**, 하나의 의사결정이나 전략을 캡슐화하는 **에이전트(Agent)**, 일부 조정 하에 함께 작동하는 에이전트 그룹인 **팀(Team)**, 그리고 전체 프로세스의 컨트롤러 역할을 하는 **오케스트레이터(MetaAgent)**가 있습니다.

특수 에이전트로는 코드를 분석하여 Tool/Agent/Team으로 분류하는 **분류 에이전트(ClassifierAgent)**, 목표를 달성하기 위해 에이전트/도구를 선택하고 순서를 지정하는 **플래너 에이전트(PlannerAgent)**, 워크플로우나 에이전트의 품질과 적합성을 평가하는 **평가 에이전트(EvaluatorAgent)**, 구성된 워크플로우를 단계별로 실행하는 **워크플로우 실행 에이전트(WorkflowExecutorAgent)** 등이 있습니다.

기타 용어로는 T-Developer가 조립하는 애플리케이션 유형인 **SaaS(서비스형 소프트웨어)**, 에이전트 내의 의사결정 지점을 의미하는 **브레인(Brain)**, 구성된 프로세스의 JSON 또는 YAML 정의인 **워크플로우(Workflow)**, 배포된 실행 가능한 워크플로우 인스턴스인 **서비스 인스턴스(Service Instance)** 등이 있습니다.