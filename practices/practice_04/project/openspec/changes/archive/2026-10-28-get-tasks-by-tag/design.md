# Design

## Context

`GET /tasks` returns the in-memory `_tasks` list as-is. Tags are stored already trimmed and validated at creation, so comparison needs no normalization of stored data. See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Add filtering inside the existing handler with minimal code.

**Non-Goals:**
- Multiple tags, case-insensitive matching, UI changes, pagination.

## Decisions

- Declare `tag: Optional[str] = Query(None)` on the existing handler. Alternative: a separate `/tasks/search` route — rejected, it splits one resource across two endpoints.
- Distinguish "absent" (`None`) from "present but blank": absent returns everything, blank raises `HTTPException(400)`. Alternative: treat blank as no filter — rejected, it hides client bugs.
- Filter with a list comprehension over `_tasks`, which preserves insertion order.

## Risks / Trade-offs

- Linear scan per request → acceptable for the in-memory store; revisit only if storage changes.
