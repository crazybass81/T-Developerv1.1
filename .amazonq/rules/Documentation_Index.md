# T‑Developer v1.1 Documentation Index

This document serves as an index to the complete T‑Developer v1.1 system design documentation set. Each linked document provides detailed information about specific aspects of the system.

---

## Core Documentation

1. [**Architecture Overview**](T-developer-architecture-v1.md) - The foundational architecture of T‑Developer v1.1

2. [**Rule Definitions**](Rule_Definitions.md) - System rule sets in both machine-readable and human-readable forms

3. [**Agent Squad Architecture**](Agent_Squad_Architecture.md) - Architecture of cooperating agent groups and the orchestrator

4. [**Agent Generator (Agno)**](Agno_Agent_Generator.md) - The agent-generation system for automatically producing new Tools or Agents

5. [**Tool Specification Format**](Tool_Specification.md) - Definition and specification of Tools in T‑Developer

6. [**Service Composition Mechanisms**](Service_Composition.md) - How T‑Developer composes services from available agents and tools

7. [**Architecture Diagrams**](Architecture_Diagrams.md) - Visual aids illustrating dynamic behavior and data flows

8. [**Integration & Deployment Structure**](Integration_and_Deployment.md) - How T‑Developer integrates into development workflows and deploys services

9. [**Glossary of Key Terms**](Glossary.md) - Definitions of all important terms and abbreviations

10. [**Versioning & Change Control Strategy**](Versioning_and_Change_Control.md) - How versions are managed and changes are controlled

## Component Specifications

### Agents

- [Agent Registry Specification](T-developer-agent-registry-spec.md)
- [Agent Reusability Tiers](T-developer-agent-reusability-tiers.md)
- [Agent Score Model](T-developer-agent-score-model.md)
- [Agent Test Suite](T-developer-agent-test-suite.md)
- [Agent Tester Specification](T-developer-agent-tester-spec.md)
- [Agent UI Launcher](T-developer-agent-ui-launcher.md)
- [Agent Version Manager](T-developer-agent-version-manager.md)
- [AgentStore API Specification](T-developer-agentstore-api-spec.md)
- [Auto Agent Composer](T-developer-auto-agent-composer.md)
- [Classifier Specification](T-developer-classifier-spec.md)
- [Evaluator Agent Specification](T-developer-evaluator-agent-spec.md)
- [MetaAgent Specification](T-developer-metaagent-spec.md)
- [Planner Agent Specification](T-developer-planner-agent-spec.md)
- [Team Specification](T-developer-team-spec.md)
- [Test Runner Agent](T-developer-test-runner-agent.md)

### Workflows & Execution

- [Workflow Schema](T-developer-workflow-schema.md)
- [Workflow Evaluator Agent](T-developer-workflow-evaluator-agent.md)
- [Workflow Executor Agent](T-developer-workflow-executor-agent.md)
- [Execution Snapshot Specification](T-developer-execution-snapshot-spec.md)

### Infrastructure & Integration

- [CLI Command Specification](T-developer-cli-command-spec.md)
- [DevSecOps Integration](T-developer-devsecops-integration.md)
- [Service Instance Specification](T-developer-service-instance-spec.md)
- [SaaS Template Library](T-developer-saas-template-library.md)
- [Test Run History Store](T-developer-test-run-history-store.md)

---

## 문서 인덱스 (Korean Summary)

이 문서는 T‑Developer v1.1 시스템 설계 문서 세트의 인덱스 역할을 합니다. 각 링크된 문서는 시스템의 특정 측면에 대한 자세한 정보를 제공합니다.

핵심 문서로는 T‑Developer v1.1의 기본 아키텍처를 설명하는 **아키텍처 개요**, 기계 및 사람이 읽을 수 있는 형식의 시스템 규칙 세트를 다루는 **규칙 정의**, 협력하는 에이전트 그룹과 오케스트레이터의 아키텍처를 설명하는 **에이전트 스쿼드 아키텍처**, 새로운 도구나 에이전트를 자동으로 생성하는 시스템인 **에이전트 생성기(Agno)**, T‑Developer에서 도구의 정의와 명세를 다루는 **도구 명세 형식**, T‑Developer가 사용 가능한 에이전트와 도구로부터 서비스를 구성하는 방법을 설명하는 **서비스 구성 메커니즘**, 동적 동작과 데이터 흐름을 보여주는 시각적 보조 자료인 **아키텍처 다이어그램**, T‑Developer가 개발 워크플로우에 통합되고 서비스를 배포하는 방법을 다루는 **통합 및 배포 구조**, 모든 중요한 용어와 약어의 정의를 제공하는 **주요 용어 용어집**, 버전이 관리되고 변경이 제어되는 방법을 설명하는 **버전 관리 및 변경 제어 전략**이 있습니다.

또한 에이전트, 워크플로우 및 실행, 인프라 및 통합에 관한 다양한 구성 요소 명세가 포함되어 있습니다.