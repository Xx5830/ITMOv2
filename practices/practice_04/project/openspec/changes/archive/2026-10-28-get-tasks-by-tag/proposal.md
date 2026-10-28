# Proposal

## Why

`GET /tasks` always returns every task. Tasks already carry tags, but a client cannot narrow the list by tag without downloading everything and filtering itself.

## What Changes

- `GET /tasks` accepts an optional single query parameter `tag`.
- With `tag`, only tasks whose `tags` contain that exact value (case-sensitive) are returned, in the original insertion order.
- `tag` is trimmed before comparison; an empty or whitespace-only `tag` is rejected with `400 Bad Request`.
- Without `tag`, behavior is unchanged.
- Automated tests for the new scenarios are added in this change.

## Capabilities

### New Capabilities
- `task-filtering`: filtering the task list by a single tag via the `tag` query parameter.

### Modified Capabilities

## Impact

- Code: `app/main.py` (`GET /tasks` handler only), new tests under `tests/`.
- API: backward-compatible addition of an optional query parameter.
- Not affected: models, `POST /tasks` validation, `DELETE /tasks/{id}`, static frontend, `docs/`, `scripts/check.sh`.
