---
name: n8n-executor
description: Use when executing n8n workflows, checking workflow status, or retrieving execution data.
---

# n8n Executor

## Overview
Assists in the execution and monitoring of workflows in an n8n instance using the n8n API.

## When to Use
- Triggering a specific n8n workflow by ID.
- Retrieving the status of a past execution.
- Fetching JSON data from a finished workflow.

## Core Pattern
Always confirm the workflow ID and the endpoint URL before execution.

```bash
# Example API call
curl -X POST "https://n8n.example.com/api/v1/workflows/[ID]/execute" \
     -H "X-N8N-API-KEY: [API_KEY]"
```

## Quick Reference
| Action | Endpoint Pattern |
|--------|-----------------|
| Execute | `POST /workflows/:id/execute` |
| Get Status | `GET /executions/:id` |
| List Workflows | `GET /workflows` |

## Implementation
1. Obtain workflow ID and API key.
2. Construct the API request.
3. Handle the response and log execution ID.

## Common Mistakes
- Incorrect API key or lack of authentication.
- Invalid workflow ID or endpoint.
- Network connectivity issues to the n8n instance.
