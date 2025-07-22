# T‑Developer Tool Specification Format

This document explains what Tools are in the T‑Developer system and how to define and specify them. It covers the conceptual definition of a Tool, how to create one, and how Tools are represented in the system.

---

## 1. Definition of a Tool

In the T‑Developer context, a **Tool** is a pure function module with **no internal decision logic**. Tools are the simplest components in the system and serve as highly reusable, atomic operations that perform specific tasks.

Key characteristics of Tools:
- No decision-making logic (no branching, no conditionals)
- Function-level execution
- Highest reusability (Tier A)
- Atomic operations that do one thing well

Examples of Tools include:
- **GPTCallerTool**: Calls an LLM API to generate text
- **S3UploaderTool**: Uploads data to Amazon S3
- **PDFExtractorTool**: Extracts text from PDF documents
- **ImageAnalysisTool**: Analyzes images for content or features

Tools are the building blocks of Agents and Teams, providing the fundamental operations that more complex components combine and coordinate.

## 2. Code Template/Decorator

Tools are defined in code using the `@tool` decorator. This decorator marks a Python function as a Tool and registers it with the system.

### Basic Tool Example

```python
@tool
def s3_uploader(data: str, bucket: str, key: str):
    """
    Uploads data to an S3 bucket.
    
    Args:
        data: The content to upload
        bucket: The S3 bucket name
        key: The object key in the bucket
        
    Returns:
        str: The URL of the uploaded object
    """
    # Implementation to upload to S3
    url = f"s3://{bucket}/{key}"
    upload_to_s3(data, bucket, key)
    return url
```

This is classified as a Tool because it has no branching logic (no "if" statements or decision making). The `@tool` decorator registers the function as a Tool with the system, making it available for use by Agents and in workflows.

### Tool Function Structure

A well-designed Tool function should:
1. Have clear input parameters with type hints
2. Include a descriptive docstring
3. Perform a single, focused operation
4. Return a consistent output type
5. Handle errors appropriately (either internally or with clear exceptions)

## 3. Tool Metadata Format

When a Tool is registered in the system, it is represented by metadata in the AgentStore. This metadata describes the Tool's properties and capabilities.

### Tool Metadata Example

```json
{
  "name": "GPTCallerTool",
  "type": "tool",
  "brain_count": 0,
  "reusability": "A",
  "path": "s3://tdev-codebase/tools/gpt_caller.py",
  "class": "tools.gpt.GPTCallerTool",
  "description": "Calls an LLM to get a completion",
  "input_schema": {
    "prompt": "string",
    "model": "string",
    "temperature": "float"
  },
  "output_schema": {
    "completion": "string"
  },
  "tags": ["LLM", "openai", "text-generation"]
}
```

### Key Metadata Fields

| Field | Description |
| ----- | ----------- |
| `name` | Unique identifier for the Tool |
| `type` | Always "tool" for Tools |
| `brain_count` | Always 0 for Tools (no decision logic) |
| `reusability` | Always "A" (highest) for Tools |
| `path` | Storage location of the Tool's code |
| `class` | Python class/function name to import |
| `description` | Brief explanation of the Tool's purpose |
| `input_schema` | Definition of expected input parameters |
| `output_schema` | Definition of the return value structure |
| `tags` | Keywords for categorization and search |

Tools have the simplest metadata structure in the system, as they have no sub-components and no decision logic.

## 4. How to Create a New Tool

Creating a new Tool in T‑Developer involves the following steps:

### 4.1 Using the CLI

The easiest way to create a Tool is using the T‑Developer CLI:

```bash
tdev init tool --name GPTCallerTool --template llm-call
```

This command:
1. Creates a new Python file with the Tool template
2. Sets up the basic structure with the `@tool` decorator
3. Adds a skeleton implementation to fill in

### 4.2 Manual Creation

To create a Tool manually:

1. Create a new Python file in your project's tools directory
2. Define a function with the `@tool` decorator
3. Implement the Tool's functionality
4. Register the Tool with the system:

```bash
tdev register ./tools/my_tool.py
```

### 4.3 Tool Development Guidelines

When developing a Tool:

1. **Focus on a single responsibility**: A Tool should do one thing well
2. **Minimize side effects**: Make operations as pure as possible
3. **Handle errors gracefully**: Either catch exceptions internally or document the exceptions that might be thrown
4. **Document inputs and outputs clearly**: Use type hints and docstrings
5. **Ensure idempotency when possible**: The same input should produce the same output
6. **Optimize for reusability**: Avoid hardcoding values or making assumptions about context

## 5. Tool Specification vs. Agent Specification

Tools have simpler specifications compared to Agents:

| Aspect | Tool | Agent |
| ------ | ---- | ----- |
| Decision Logic | None | One or more decision points |
| Brain Count | 0 | 1+ |
| Reusability | Very High (A) | High to Medium (B-C) |
| Metadata | Simple | More complex |
| Dependencies | None or external only | May include Tools |
| Implementation | Single function | Function with branching or class |

While an Agent's specification includes a list of Tools it uses internally and its decision logic, a Tool's specification is just the function itself and its input/output schema.

## 6. Example (English & Korean)

### Example: EmailSenderTool

**English**: The `EmailSenderTool` is a tool that sends emails via SMTP. It takes `to_address`, `subject`, and `content` as input and returns a status object with success flag and message ID. It has no decision logic, just a call to an email service API.

**Korean**: `EmailSenderTool`은 SMTP를 통해 이메일을 보내는 도구입니다. `to_address`(받는 사람), `subject`(제목), `content`(내용)을 입력으로 받아 성공 여부와 메시지 ID가 포함된 상태 객체를 반환합니다. 의사 결정 로직이 없고 이메일 서비스 API를 호출하는 기능만 있습니다.

### Implementation Example

```python
@tool
def email_sender(to_address: str, subject: str, content: str) -> dict:
    """
    Sends an email via SMTP.
    
    Args:
        to_address: Email recipient
        subject: Email subject line
        content: Email body content
        
    Returns:
        dict: Status object with success flag and message ID
    """
    try:
        message_id = send_email_via_smtp(to_address, subject, content)
        return {
            "success": True,
            "message_id": message_id
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

## 7. Ensuring Quality and Reusability

Because Tools are the most reusable components in T‑Developer, ensuring their quality is critical:

### Testing

All Tools should have comprehensive test cases that verify:
- Correct behavior with valid inputs
- Proper error handling with invalid inputs
- Performance characteristics with large inputs

### Documentation

Tools should be well-documented with:
- Clear function signatures with type hints
- Comprehensive docstrings
- Examples of usage
- Notes on limitations or edge cases

### Interface Design

Tool interfaces should be:
- Intuitive and consistent
- Focused on a single responsibility
- Flexible enough for various use cases
- Stable across versions when possible

### Error Handling

Tools should handle errors in a consistent way:
- Catch and handle expected errors internally when appropriate
- Raise clear, specific exceptions for unexpected errors
- Include context in error messages
- Return structured error information when using status objects

---

## 도구 명세 형식 요약 (Korean Summary)

T‑Developer에서 **도구(Tool)**는 내부 의사결정 로직이 없는 순수 함수 모듈입니다. 도구는 시스템에서 가장 단순한 구성 요소로, 특정 작업을 수행하는 재사용성이 매우 높은 원자적 연산으로 작동합니다.

도구는 `@tool` 데코레이터를 사용하여 코드로 정의됩니다. 이 데코레이터는 Python 함수를 도구로 표시하고 시스템에 등록합니다. 도구가 시스템에 등록되면 AgentStore에 메타데이터로 표현됩니다.

새 도구를 만드는 가장 쉬운 방법은 T‑Developer CLI를 사용하는 것입니다: `tdev init tool --name 도구이름 --template 템플릿이름`. 도구를 개발할 때는 단일 책임에 집중하고, 부작용을 최소화하며, 오류를 적절히 처리하고, 입력과 출력을 명확히 문서화하며, 가능한 경우 멱등성을 보장하고, 재사용성을 최적화해야 합니다.

도구는 에이전트보다 더 단순한 명세를 가집니다. 도구에는 의사결정 로직이 없고(브레인 수 0), 재사용성이 매우 높으며(A 등급), 메타데이터가 단순하고, 종속성이 없거나 외부 종속성만 있으며, 구현이 단일 함수로 이루어집니다.