# T-Developer API Module

This module provides a FastAPI server for interacting with T-Developer v1.1 from web and chat interfaces.

## Components

### API Server

The `server.py` file defines a FastAPI application with endpoints for interacting with T-Developer. It provides:

- REST endpoints for orchestrating goals, classifying code, and managing components
- WebSocket support for real-time updates and interactions
- Integration with the DevCoordinatorAgent for orchestration
- Feedback collection and monitoring

## API Endpoints

The API server exposes the following endpoints:

### REST Endpoints

- `GET /`: Root endpoint that returns the API version
- `GET /agents`: List all registered agents
- `GET /tools`: List all registered tools
- `GET /teams`: List all registered teams
- `POST /orchestrate`: Orchestrate a goal
- `POST /classify`: Classify code
- `POST /feedback`: Submit feedback for an agent
- `GET /feedback/{agent_name}`: Get feedback for an agent

### WebSocket Endpoint

- `WebSocket /ws/{client_id}`: WebSocket endpoint for real-time updates

## Usage

### Starting the API Server

You can start the API server using the CLI:

```bash
tdev serve --port 8000
```

Or programmatically:

```python
from tdev.api.server import start_server

start_server()
```

### Making API Requests

Example of making a request to the API:

```python
import requests
import json

# Orchestrate a goal
response = requests.post(
    "http://localhost:8000/orchestrate",
    json={"goal": "Echo test input"}
)
result = response.json()
print(result)

# Classify code
response = requests.post(
    "http://localhost:8000/classify",
    json={"code": "def test(): return 'hello'"}
)
result = response.json()
print(result)
```

### Using WebSockets

Example of using WebSockets:

```javascript
// JavaScript example
const socket = new WebSocket("ws://localhost:8000/ws/client1");

socket.onopen = function(e) {
  console.log("Connection established");
  socket.send(JSON.stringify({goal: "Echo test input"}));
};

socket.onmessage = function(event) {
  console.log("Received data:", JSON.parse(event.data));
};

socket.onclose = function(event) {
  if (event.wasClean) {
    console.log(`Connection closed cleanly, code=${event.code} reason=${event.reason}`);
  } else {
    console.log('Connection died');
  }
};

socket.onerror = function(error) {
  console.log(`WebSocket error: ${error.message}`);
};
```

## Deployment

The API server can be deployed to AWS using the provided CloudFormation template and deployment scripts. The deployment creates:

- An API Gateway for the REST endpoints
- Lambda functions for handling requests
- DynamoDB tables for storing data
- CloudWatch logs for monitoring

To deploy the API server:

```bash
python scripts/deploy_infrastructure.py
```

## Integration with UI

The API server is designed to be integrated with the Agent UI Launcher or other front-end applications. It provides all the necessary endpoints for:

- Submitting goals and code
- Monitoring workflow execution
- Managing agents and tools
- Collecting feedback