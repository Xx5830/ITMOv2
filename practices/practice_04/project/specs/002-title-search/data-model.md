# Data Model: title-search

## Entities

- Task
  - id: int
  - title: str (non-empty after trim, max 100 chars)
  - tags: list[str] (1..5 items; each non-empty, <=20 chars; alnum or hyphen)

## Derived/Validation Rules

- Query q (optional):
  - When provided, q is trimmed. If empty after trim or length > 100 → 400.
  - Matching rule: case-insensitive substring of title.
  - Ordering: preserve creation order in responses.

- Query tag (optional, existing):
  - Non-empty after trim; else 400.
  - Matching rule: exact membership in task.tags.

## Relationships

- None added. Tag-based graph relationships are unchanged.
