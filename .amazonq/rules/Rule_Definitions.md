# T‑Developer Rule Definitions

This document details the system's rule sets in both machine-readable and human-readable forms. It covers the explicit logic and heuristics that govern the system's behavior, including classification criteria, scoring formulas, and evaluation rules.

---

## 1. Classification Rules

The `ClassifierAgent` uses these rules to determine how a Python component is classified as a Tool, Agent, Composite Agent, or Team based on the number of decision points ("brains") and coordination presence.

### Machine-Readable Format

```yaml
classification_rules:
  - condition: "decision_points == 0"
    classify_as: "Tool"
    reusability: "A"
    description: "No decision logic"
  
  - condition: "decision_points == 1"
    classify_as: "Agent"
    reusability: "B"
    description: "Single decision logic"
  
  - condition: "decision_points >= 2 AND no_internal_routing == true"
    classify_as: "Composite Agent"
    reusability: "C"
    description: "Multiple decision points without coordination"
  
  - condition: "decision_points >= 2 AND has_controller == true"
    classify_as: "Team"
    reusability: "D"
    description: "Multiple decision points with coordination"
```

### Human-Readable Explanation

- If a component has **no decision logic** (no branching, no conditional statements), it is classified as a **Tool**. Tools are pure functions with the highest reusability (Tier A).
- If a component has **one decision point** (one logical branch or conditional), it is classified as an **Agent**. Agents have high reusability (Tier B) and are role-specific.
- If a component has **two or more decision points without internal routing** between them, it is classified as a **Composite Agent**. These have medium reusability (Tier C).
- If a component has **two or more decision points with a coordinator** that manages them, it is classified as a **Team**. Teams have lower reusability (Tier D) due to their specialized nature.

Decision logic ("brain") is identified through:
- Branching structures (`if`, `match`, `try/except`, `switch`)
- Conditional logic based on LLM responses
- Internal routing among tools or agents

## 2. Workflow Evaluation Rules

The `WorkflowEvaluatorAgent` uses these rules to assess workflow quality and completeness.

### Machine-Readable Format

```yaml
evaluation_metrics:
  - name: "structural_completeness"
    weight: 0.30
    rules:
      - "All required steps must be present"
      - "Input/output connections must be valid"
      - "No dangling inputs or outputs"
  
  - name: "agent_suitability"
    weight: 0.25
    rules:
      - "Agents must match their intended roles"
      - "Agent capabilities must align with step requirements"
  
  - name: "error_resilience"
    weight: 0.20
    rules:
      - "Critical steps should have error handling"
      - "Fallback mechanisms should exist for key operations"
  
  - name: "efficiency"
    weight: 0.15
    rules:
      - "Minimize redundant steps"
      - "Optimize for minimal agent count vs. task complexity"
  
  - name: "clarity"
    weight: 0.10
    rules:
      - "Step names should be descriptive"
      - "Flow should be logical and easy to follow"
```

### Human-Readable Explanation

The `WorkflowEvaluatorAgent` scores workflows based on five key dimensions:

1. **Structural Completeness (30%)**: Ensures all necessary steps are present and properly connected. A workflow is incomplete if required steps are missing or if data cannot flow properly between steps.

2. **Agent Suitability (25%)**: Evaluates whether the selected agents or teams are appropriate for their assigned tasks. For example, using a `SummarizerAgent` for translation would be unsuitable, or using a simple agent where a team is needed for complex coordination.

3. **Error Resilience (20%)**: Assesses how well the workflow handles potential failures. Good workflows include validation steps, retry mechanisms, or fallback options.

4. **Efficiency (15%)**: Measures how efficiently the workflow accomplishes its goal. Unnecessary steps or overly complex agent combinations reduce this score. Using teams appropriately can improve efficiency by encapsulating complex logic.

5. **Clarity (10%)**: Evaluates how understandable and maintainable the workflow is. Clear step names and logical flow improve this score.

The final score is calculated as a weighted average of these five dimensions:

```
final_score = (completeness * 0.3) + (suitability * 0.25) + (resilience * 0.2) + (efficiency * 0.15) + (clarity * 0.1)
```

## 3. Scoring & Prioritization Rules

The `AgentScoreModel` uses these rules to evaluate agent reliability, quality, and reusability.

### Machine-Readable Format

```yaml
agent_score_model:
  quality:
    formula: "pass_rate(last_5_test_runs) * 0.7 + average_execution_quality * 0.3"
    description: "Measures correctness and output quality"
  
  stability:
    formula: "1 - failure_rate(last_3_days)"
    description: "Measures reliability in production"
  
  reusability:
    formula: "normalized_reuse_count"
    description: "Measures adoption across workflows"
  
  final_score:
    formula: "quality * 0.5 + stability * 0.25 + reusability * 0.25"
    description: "Overall agent reliability score"
  
  deployment_threshold: 0.85
  rollback_threshold: 0.70
```

### Human-Readable Explanation

The `AgentScoreModel` calculates several metrics to evaluate an agent's overall reliability:

1. **Quality (50% of final score)**: Combines test pass rate (70%) and execution quality metrics (30%). Higher quality means the agent produces correct and valuable outputs.

2. **Stability (25% of final score)**: Derived from the agent's failure rate in production over the last three days. A stable agent rarely fails in real-world usage.

3. **Reusability (25% of final score)**: Based on how frequently the agent is used across different workflows. Widely adopted agents score higher.

The final score is calculated as:
```
final_score = (quality * 0.5) + (stability * 0.25) + (reusability * 0.25)
```

Important thresholds:
- An agent must exceed a score of 0.85 to be automatically deployed to production
- If an agent's score falls below 0.70 in production, it may trigger automatic rollback to a previous version

## 4. Execution Strategy Selection Rules

These rules determine the optimal execution approach based on task complexity and resource efficiency.

### Machine-Readable Format

```yaml
execution_strategy_rules:
  - condition: "can_compose_from_tools_only == true"
    strategy: "tools_only"
    priority: 1
    reason: "Lowest cost, highest efficiency"
  
  - condition: "single_agent_combination_possible == true"
    strategy: "single_agent"
    priority: 2
    reason: "Moderate cost, good efficiency"
  
  - condition: "team_structure_required == true"
    strategy: "team_based"
    priority: 3
    reason: "Higher cost, requires advanced model"
  
  - condition: "default"
    strategy: "design_new_agent"
    priority: 4
    reason: "Highest cost, requires agent creation"
```

### Human-Readable Explanation

The system follows these rules to minimize LLM usage and optimize resource efficiency:

1. **Tools-Only Strategy**: If the task can be accomplished using only Tools (no decision logic required), execute immediately. This has the lowest cost and highest efficiency.

2. **Single-Agent Strategy**: If a combination of a single Agent with Tools can solve the task, use this approach. This has moderate cost and good efficiency.

3. **Team-Based Strategy**: If the task requires a Team structure (multiple decision points with coordination), use an advanced model like GPT-4o. This has higher cost but is necessary for complex tasks.

4. **Design New Agent**: If none of the above strategies can solve the task, design a new Agent or modify an existing one. This has the highest cost but ensures all tasks can eventually be completed.

## 5. Rule Application Process

Rules are applied by various components in the T‑Developer system:

- **Classification Rules**: Applied by the `ClassifierAgent` when analyzing Python code
- **Workflow Evaluation Rules**: Applied by the `WorkflowEvaluatorAgent` when scoring workflows
- **Agent Scoring Rules**: Applied by the `EvaluatorAgent` and `AgentScoreModel`
- **Execution Strategy Rules**: Applied by the `PlannerAgent` when designing workflows

All rules are stored in version-controlled configuration files to ensure consistency and traceability of changes.

---

## 규칙 정의 요약 (Korean Summary)

T‑Developer 시스템은 다양한 규칙 세트를 사용하여 동작합니다:

1. **분류 규칙**: 의사결정 포인트("브레인") 수와 조정 존재 여부에 따라 컴포넌트를 Tool, Agent, Composite Agent, Team으로 분류합니다. 브레인이 없으면 Tool, 하나면 Agent, 둘 이상이면서 조정자가 없으면 Composite Agent, 둘 이상이면서 조정자가 있으면 Team입니다.

2. **워크플로우 평가 규칙**: 구조적 완전성(30%), 에이전트 적합성(25%), 오류 복원력(20%), 효율성(15%), 명확성(10%)을 기준으로 워크플로우 품질을 평가합니다.

3. **점수 및 우선순위 규칙**: 품질(50%), 안정성(25%), 재사용성(25%)을 기준으로 에이전트의 신뢰성을 평가합니다. 최종 점수가 0.85 이상이어야 자동 배포되며, 0.70 미만으로 떨어지면 롤백이 트리거될 수 있습니다.

4. **실행 전략 선택 규칙**: 리소스 효율성을 최적화하기 위해 Tool만 사용, 단일 Agent 사용, Team 구조 사용, 또는 새 Agent 설계 중에서 최적의 전략을 선택합니다.