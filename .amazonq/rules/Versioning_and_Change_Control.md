# T‑Developer Versioning and Change Control Strategy

This document outlines how versions are managed for agents, workflows, and the T‑Developer system itself, and how changes are controlled and tracked over time. It provides guidelines for version numbering, maintaining backward compatibility, and processes for updating components safely—especially important in a system that auto-generates and deploys code.

---

## 1. Agent Versioning Scheme

T‑Developer uses a combination of semantic versioning and simple version identifiers for its components:

* **Semantic Versioning (major.minor.patch)** is used for agent implementations, where:
  * **Major** version changes indicate non-backward-compatible API changes
  * **Minor** version changes add functionality in a backward-compatible manner
  * **Patch** version changes represent backward-compatible bug fixes

* **Simple Version Identifiers** (v1, v2, v3) are used in workflow IDs and agent references within workflows

### Naming Conventions

* Agent versions in code: `"version": "1.3.0"` (semantic versioning)
* Agent references in workflows: `SummarizerAgent@v2` (simple identifier)
* Workflow IDs: `policy-match-flow-v1` (embedded version)

## 2. Storing and Retrieving Versions

### Agent Version Storage

The `AgentStore` maintains multiple versions of each agent:

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

* Each version maintains its own metadata, status, and path to implementation
* The `AgentStore` API supports retrieving specific versions via query parameters
* Future plans include Git-backed history tracking for all agent metadata changes

### Workflow Version Storage

* Workflows are stored as JSON files in Git repositories with version-specific filenames
* Path convention: `/flows/policy-match-flow-v1.json`
* Each new workflow version is a separate file, enabling side-by-side comparison

## 3. AgentVersionManager & Automated Control

The `AgentVersionManager` plays a central role in version control:

* **Version Resolution**: Automatically selects appropriate agent versions based on context:
  ```python
  resolve(agent_name, strategy="stable" | "latest" | "fastest")
  ```

* **Quality-Based Promotion**: New versions are only promoted to "stable" status when:
  * All tests pass successfully
  * `AgentScoreModel` final score exceeds deployment threshold
  * No regressions are detected in key metrics

* **Fallback Mechanism**: Provides automatic rollback to previous versions on failure:
  ```python
  if version_exec_failed("SummarizerAgent@v2"):
      fallback_to("SummarizerAgent@v1")
  ```

## 4. Workflow Versioning

Workflows follow a simple versioning scheme with embedded version identifiers:

* **Version Incrementing**: When a workflow is modified, a new version is created with an incremented version number
* **Storage**: Each workflow version is stored as a separate JSON file in Git
* **Referencing**: Workflows explicitly reference specific agent versions to ensure stability
* **Compatibility**: Workflows are designed to be compatible with specific agent version ranges

## 5. Change Propagation and Compatibility

T‑Developer manages change propagation through several mechanisms:

* **Explicit Version References**: Agents can reference specific tool versions they depend on
* **Compatibility Testing**: The `TestRunnerAgent` verifies that new agent versions work with existing workflows
* **Version Pinning**: Critical workflows can pin exact agent versions to prevent unexpected changes
* **Dependency Tracking**: The system maintains a graph of dependencies between components

### Compatibility Strategy

* Tools should maintain backward compatibility where possible
* Breaking changes require a new major version and clear documentation
* Agents should specify minimum required versions of tools they use
* Workflows should reference specific agent versions to ensure stability

## 6. Source Control for Artifacts

All T‑Developer artifacts are maintained in version control:

* **Agent Code**: Stored in Git repositories with proper versioning
* **Workflow Definitions**: JSON files in Git with version-specific filenames
* **Configuration**: Versioned alongside code to ensure reproducibility
* **Documentation**: Maintained in Git with the same versioning scheme as code

### Repository Structure

```
repository/
├── agents/
│   ├── summarizer_v1.py
│   └── summarizer_v2.py
├── tools/
│   └── gpt_caller.py
├── workflows/
│   ├── policy-match-flow-v1.json
│   └── policy-match-flow-v2.json
└── docs/
    └── versioning.md
```

## 7. Release Management

T‑Developer platform releases follow semantic versioning:

* **Current Version**: T‑Developer v1.1
* **Version Increments**:
  * Major version: Significant architecture changes or breaking API changes
  * Minor version: New features, components, or non-breaking enhancements
  * Patch version: Bug fixes and minor improvements

### Release Process

1. Feature branches are developed and tested independently
2. Changes are merged to main branch after review
3. Release candidates undergo comprehensive testing
4. Successful candidates are tagged with version numbers
5. Release notes document all significant changes

## 8. Automated Change Control

T‑Developer employs several automated mechanisms for change control:

* **CI/CD Pipeline**: Automatically tests all changes before deployment
* **EvaluatorAgent**: Scores new workflows and agents to detect regressions
* **Git Integration**: Every change to agent definitions creates a commit
* **Automated Testing**: `TestRunnerAgent` executes test suites for all components

### Quality Gates

New versions must pass through quality gates before promotion:

* All tests must pass
* Code quality metrics must meet thresholds
* Performance must not degrade
* Security scans must not detect new vulnerabilities

## 9. Rollback Strategy

T‑Developer supports rapid rollback when issues are detected:

* **Agent Rollback**: `AgentVersionManager` can revert to previous stable versions
* **Workflow Rollback**: Previous workflow versions remain available for redeployment
* **System Rollback**: Platform releases can be reverted if critical issues are found

### Retention Policy

* Previous stable versions are retained indefinitely
* Experimental versions may be pruned after a defined period
* All version history is maintained in Git for audit purposes

## 10. Version Tagging Conventions

T‑Developer uses consistent version tagging across all components:

* **Agent Versions**: `v1`, `v2`, etc. for simple references; `1.0.0`, `1.1.0` for semantic versioning
* **Workflow IDs**: Always include version suffix (e.g., `-v1`, `-v2`)
* **Platform Releases**: Tagged as `v1.1`, `v2.0`, etc.
* **Pre-release Versions**: Marked with suffixes like `-alpha`, `-beta`, `-rc1`

## 11. Example Scenario: Version Progression

### SummarizerAgent Evolution

1. **SummarizerAgent v1.0**:
   * Basic summarization using GPT-3.5
   * Deployed and stable

2. **SummarizerAgent v1.1**:
   * Improved algorithm with better quality scores
   * Both versions exist in AgentStore
   * PlannerAgent prefers v1.1 due to higher quality score

3. **Monitoring and Rollback**:
   * Production monitoring detects higher failure rate in v1.1
   * AgentScoreModel's stability metric drops below threshold
   * System automatically reverts to v1.0 for new workflows
   * Development team addresses issues in v1.1

4. **Resolution**:
   * Fixed version released as v1.2
   * Tests confirm stability and quality improvements
   * System gradually transitions to v1.2 as default

## 12. Policy for Rule Changes

Changes to system rules and configurations follow specific guidelines:

* **Scoring Algorithm Changes**: Considered minor version changes if backward compatible
* **Classification Criteria Updates**: Require thorough testing and documentation
* **Configuration Files**: Version-controlled alongside code
* **Rule Testing**: All rule changes must be validated against test cases

## 13. Document Revision Tracking

T‑Developer design documentation follows the same versioning principles:

* Documents are updated to reflect current system version
* Major architecture changes trigger document version updates
* All documentation is maintained in Git with proper history
* Changes to documentation are reviewed and approved like code changes

### Documentation Changelog

A changelog tracks significant updates to system documentation:

* Initial release: T‑Developer v1.0 documentation
* Current: T‑Developer v1.1 documentation with updated agent specifications
* Future: Will reflect v2.0 architecture when developed

---

## 버전 관리 및 변경 제어 전략 요약 (Korean Summary)

T‑Developer는 에이전트, 워크플로우 및 시스템 자체에 대한 버전을 체계적으로 관리합니다. 시맨틱 버전 관리(major.minor.patch)와 간단한 버전 식별자(v1, v2)를 조합하여 사용하며, `AgentVersionManager`가 버전 해결 및 자동 롤백을 담당합니다.

품질 기반 승격 시스템을 통해 새 버전은 테스트 통과 및 `AgentScoreModel` 점수가 임계값을 초과할 때만 "안정" 상태로 승격됩니다. 모든 아티팩트는 Git에서 버전 관리되며, 워크플로우는 특정 에이전트 버전을 명시적으로 참조하여 안정성을 보장합니다.

시스템은 자동화된 테스트, 품질 게이트 및 신속한 롤백 메커니즘을 통해 변경 사항을 엄격하게 제어합니다. 이러한 전략은 자동 생성 및 배포 코드를 포함하는 시스템에서 특히 중요하며, T‑Developer의 안정성과 확장성을 보장합니다.