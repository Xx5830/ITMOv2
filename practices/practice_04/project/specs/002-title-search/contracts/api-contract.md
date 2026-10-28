# Contract: GET /tasks with q and tag

## Endpoint

GET /tasks

## Query Parameters

- q (optional):
  - Type: string
  - Behavior: case-insensitive substring match on title
  - Trimmed before validation and matching
  - Errors: 400 if empty after trim or length > 100

- tag (optional, existing):
  - Type: string
  - Behavior: exact match in task tags
  - Errors: 400 if empty after trim

## Combination Rules

- If both q and tag provided: apply AND logic (task must satisfy both filters)
- If only q provided: filter by title substring
- If only tag provided: filter by tag
- If neither provided: return all tasks

## Responses

- 200 OK: JSON array of tasks, ordered by creation time
- 400 Bad Request: JSON {"detail": string} for invalid q or tag

## Examples

- GET /tasks?q=milk → tasks with titles containing "milk" (any case)
- GET /tasks?q=milk&tag=work → tasks whose titles contain "milk" and have tag "work"
- GET /tasks?q=%20%20 → 400 {"detail": "..."}
