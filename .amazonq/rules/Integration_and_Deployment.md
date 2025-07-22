# T‑Developer Integration & Deployment Structure

This document details how T‑Developer integrates into development workflows (CI/CD) and how composed services are deployed and managed in runtime. It covers the DevSecOps pipeline, cloud deployment targets, and how different parts of the system connect in a live environment.

---

## 1. DevSecOps Pipeline Integration

T‑Developer is designed to integrate seamlessly with continuous integration and continuous deployment (CI/CD) workflows. This integration enables automated testing, classification, evaluation, and deployment of agents and workflows.

### 1.1 GitHub Actions Workflow

The following example shows how T‑Developer integrates with GitHub Actions:

```yaml
name: T-Dev QA
on: [pull_request]
jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
      - name: Run classify
        run: tdev classify ./agents/**/*.py
      - name: Run tests
        run: tdev test all
      - name: Run evaluator
        run: tdev evaluate ./workflows/*.json
      - name: Post to Slack
        run: ./scripts/slack_notify.sh "✅ All checks passed!"
```

### 1.2 Pipeline Steps

When code is pushed or a PR is opened, the following steps are executed:

1. **Classification**: `tdev classify` is run on all new or changed agent files. This invokes the ClassifierAgent to analyze the code structure and update metadata in the AgentStore.

2. **Testing**: `tdev test` runs the TestRunnerAgent to execute all relevant tests on agents and tools. This ensures that components behave as expected and meet quality standards.

3. **Evaluation**: `tdev evaluate` uses the EvaluatorAgent to score workflows for quality, efficiency, and robustness. This ensures that composed services meet predefined quality gates.

4. **Notification**: Results are aggregated and reported through:
   - PR comments or GitHub Check Runs
   - Slack notifications with summary information

5. **Deployment**: If all checks pass and scores exceed thresholds, the pipeline can automatically deploy the service to the chosen environment.

### 1.3 Example Slack Notification

```
📦 New Agent: SummarizerAgent classified as `agent`
✅ Tests passed (3/3)
🧠 Evaluator Score: 91 (A-)
🚀 Deployed to Lambda: arn:aws:lambda:...
```

## 2. Security and Approval Gates

T‑Developer implements several security measures and approval gates in the deployment process:

### 2.1 Quality-Based Approvals

Services are only automatically deployed if they meet quality criteria:
- All tests must pass
- Evaluator score must exceed deployment threshold (typically 85%)
- No security vulnerabilities detected

### 2.2 Manual Approval Options

For critical services or experimental changes, manual approval can be required:
- GitHub PR approvals from designated reviewers
- Slack-based approval buttons (planned extension)
- Manual promotion between environments

### 2.3 Security Practices

- Least privilege IAM roles are applied to deployed services
- Secrets are managed via AWS Secrets Manager or environment variables
- Sensitive information is never exposed in logs or notifications
- Future: Automated IAM policy generation based on agent capabilities

## 3. Deployment Targets and Process

T‑Developer supports multiple deployment targets for composed services:

### 3.1 AWS Lambda

**Process:**
1. Service code (agents + workflow runtime) is packaged into a ZIP file
2. ZIP is uploaded to S3
3. Lambda function is created or updated with the package
4. Function configuration (memory, timeout, etc.) is set based on service requirements

**Use Case:** Ideal for event-driven, stateless services with variable load

### 3.2 AWS ECS (Docker)

**Process:**
1. Docker image is built containing the service components
2. Image is pushed to Amazon ECR
3. ECS service is created or updated to use the new image
4. Task definition is configured with appropriate resources

**Use Case:** Better for long-running services or those with specific dependencies

### 3.3 Local/CLI Execution

**Process:**
1. Service is registered locally
2. Can be executed via `tdev run` command
3. Useful for development and testing

**Use Case:** Development, testing, or one-off executions

### 3.4 Service Instance Metadata

Each deployed service is tracked with metadata:

```json
{
  "service_id": "policy-matcher-v1",
  "status": "active",
  "created_at": "2025-07-22T04:00:00Z",
  "workflow_id": "clustered-match-flow",
  "agents": ["ScraperAgent", "ClusterAgent", "ChatAgent"],
  "deployment": {
    "type": "lambda",
    "region": "ap-northeast-2",
    "entrypoint": "handler.py::run"
  },
  "entry_input_type": "text",
  "output_type": "response",
  "last_executed_at": "2025-07-22T06:20:31Z"
}
```

This metadata is stored in DynamoDB and used to track the status and configuration of all deployed services.

## 4. Integration with Cloud Services

T‑Developer integrates with various cloud services for storage, execution, and monitoring:

### 4.1 Storage Services

| Component | Storage Service | Purpose |
|-----------|-----------------|---------|
| Agent Code | S3 or Git | Version-controlled storage of agent implementations |
| Agent Metadata | DynamoDB | Fast access to agent properties and relationships |
| Workflow Definitions | S3, Git, or DynamoDB | Versioned storage of workflow JSON/YAML |
| Service Instances | DynamoDB | Track deployed services and their status |
| Execution State | DynamoDB or Redis | Maintain context during workflow execution |

### 4.2 Compute Services

| Component | Compute Service | Purpose |
|-----------|-----------------|---------|
| Workflow Execution | AWS Lambda | Serverless execution of workflows |
| Long-running Services | AWS ECS | Container-based execution for complex services |
| Development | Local CLI | Local execution for testing and development |

### 4.3 Monitoring & Logging

| Component | Service | Purpose |
|-----------|---------|---------|
| Execution Logs | CloudWatch Logs | Detailed logs of workflow execution |
| Metrics | CloudWatch Metrics | Performance and usage metrics |
| Alerts | SNS, Slack | Notifications for errors or important events |
| Test Results | TestRunHistoryStore (DynamoDB) | Historical test outcomes for quality tracking |

## 5. Deployment Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Agent Code     │     │    Workflow     │     │  Configuration  │
│  (S3 or Git)    │     │  Definition     │     │  (Parameters)   │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────┬───────────┴───────────┬───────────┘
                     │                       │
           ┌─────────▼───────────┐  ┌────────▼────────┐
           │  Service Instance   │  │  AgentRegistry  │
           │    Definition       │  │   (DynamoDB)    │
           └─────────┬───────────┘  └────────┬────────┘
                     │                       │
                     └───────────┬───────────┘
                                 │
                     ┌───────────▼───────────┐
                     │      Deployment       │
                     └───────────┬───────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌────────▼────────┐    ┌─────────▼───────────┐  ┌────────▼────────┐
│  AWS Lambda     │    │     AWS ECS         │  │  Local CLI      │
│  Function       │    │   (Container)       │  │  Execution      │
└────────┬────────┘    └─────────┬───────────┘  └────────┬────────┘
         │                       │                       │
         └───────────┬───────────┴───────────┬───────────┘
                     │                       │
           ┌─────────▼───────────┐  ┌────────▼────────┐
           │  Execution Logs     │  │  State Storage  │
           │  (CloudWatch)       │  │   (DynamoDB)    │
           └─────────────────────┘  └─────────────────┘
```

This diagram illustrates how agent code, workflow definitions, and configuration are combined into a service instance definition, which is then deployed to various targets and monitored during execution.

## 6. Integration with Development Workflow

T‑Developer provides several integration points for developers:

### 6.1 CLI Commands

Developers can interact with the system through the CLI:

```bash
# Deploy a service
tdev deploy --service-id policy-matcher-v1 --target lambda

# Check service status
tdev status policy-matcher-v1

# Execute a workflow locally
tdev run policy-flow-v1 --input query="Startup support for youth"
```

### 6.2 UI Integration

The Agent UI Launcher provides a web interface for:
- Testing individual agents
- Visualizing workflow execution
- Monitoring deployed services
- Sharing execution results

### 6.3 IDE Integration

Future extensions may include IDE plugins for:
- Agent code generation
- Workflow visualization
- Direct deployment from the IDE
- Real-time feedback on agent quality

## 7. Versioning in Deployment

Versioning is a critical aspect of the deployment process:

### 7.1 Service Instance Versioning

When a workflow or agent is updated, a new service instance is created with an incremented version:
- `policy-matcher-v1` → `policy-matcher-v2`

This ensures that:
- Multiple versions can coexist
- Rollbacks are straightforward
- Version history is preserved

### 7.2 Deployment Strategies

T‑Developer supports several deployment strategies:
- **Blue/Green**: Deploy new version alongside old, then switch traffic
- **Canary**: Gradually route traffic to new version
- **Immediate**: Replace old version with new version immediately

The strategy can be specified during deployment:
```bash
tdev deploy --service-id policy-matcher-v2 --strategy canary
```

## 8. Security & Compliance

T‑Developer implements several security best practices:

### 8.1 Secret Management

- API keys and credentials are stored in AWS Secrets Manager
- Secrets are never logged or exposed in notifications
- Access to secrets is controlled via IAM policies

### 8.2 Least Privilege

- Each deployed service uses a custom IAM role
- Roles are scoped to the minimum permissions required
- Future: Automatic IAM policy generation based on agent capabilities

### 8.3 Audit Trail

- All deployments are logged with user information
- Service instance history is preserved
- Changes to agents and workflows are tracked in Git

## 9. Change Management

T‑Developer provides a comprehensive change management process:

### 9.1 Change Flow

1. Developer creates or modifies an agent or workflow
2. Changes are committed to Git repository
3. CI pipeline runs classification, tests, and evaluation
4. Results are reported via PR comments and Slack
5. If quality gates pass, changes are merged
6. Deployment pipeline creates new service instance
7. Service is deployed to target environment
8. Monitoring confirms successful deployment

### 9.2 Rollback Process

If issues are detected after deployment:
1. Issue is identified through monitoring or user reports
2. Previous version is redeployed:
   ```bash
   tdev rollback --service-id policy-matcher-v2 --to v1
   ```
3. Root cause analysis is performed
4. Fix is developed and goes through the change flow again

---

## 통합 및 배포 구조 요약 (Korean Summary)

T‑Developer는 개발 워크플로우(CI/CD)에 원활하게 통합되며 구성된 서비스를 런타임에 배포하고 관리하는 방법을 제공합니다.

DevSecOps 파이프라인 통합을 통해 GitHub Actions와 같은 CI/CD 도구에서 자동화된 테스트, 분류, 평가 및 배포가 가능합니다. 코드가 푸시되거나 PR이 열리면 분류, 테스트, 평가, 알림, 배포 단계가 실행됩니다.

T‑Developer는 AWS Lambda, AWS ECS(Docker), 로컬/CLI 실행과 같은 여러 배포 대상을 지원합니다. 각 배포된 서비스는 DynamoDB에 저장된 메타데이터로 추적됩니다.

시스템은 스토리지, 컴퓨팅, 모니터링 및 로깅을 위한 다양한 클라우드 서비스와 통합됩니다. 개발자는 CLI 명령, UI 통합, IDE 통합을 통해 시스템과 상호작용할 수 있습니다.

버전 관리는 배포 프로세스의 중요한 측면으로, 워크플로우나 에이전트가 업데이트되면 증분된 버전으로 새 서비스 인스턴스가 생성됩니다. T‑Developer는 블루/그린, 카나리, 즉시와 같은 여러 배포 전략을 지원합니다.

보안 및 규정 준수를 위해 시스템은 비밀 관리, 최소 권한, 감사 추적과 같은 여러 보안 모범 사례를 구현합니다. 또한 포괄적인 변경 관리 프로세스와 롤백 프로세스를 제공합니다.