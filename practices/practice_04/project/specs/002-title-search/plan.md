# Implementation Plan: title-search

Branch: 002-title-search | Date: 2026-10-28 | Spec: specs/002-title-search/spec.md

Input: Feature specification from specs/002-title-search/spec.md

Note: This plan follows the /speckit.plan workflow and generates Phase 0 and Phase 1 design artifacts without changing code.

## Summary

Add optional query parameter q to GET /tasks to filter tasks by case-insensitive substring match on title. Empty/whitespace-only q yields 400. q combines with existing tag filter via logical AND. Behavior without q remains unchanged.

## Technical Context

**Language/Version**: Python 3.14 (venv observed); runtime Linux

**Primary Dependencies**: FastAPI, Pydantic

**Storage**: In-memory list within process (no database)

**Testing**: pytest with FastAPI TestClient (pattern in tests/test_example.py)

**Target Platform**: Linux server; browser UI served as static files

**Project Type**: Web service with static frontend

**Performance Goals**: For datasets up to ~100 tasks, 95% of search requests return results under 1 second

**Constraints**: No database; backend authoritative validation; minimal change policy; no changes to docs/requirements.md or scripts/check.sh

**Scale/Scope**: Educational scope; small in-memory dataset; single-process server

## Constitution Check

GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.

- Test-First (NON-NEGOTIABLE): Plan introduces tests for q before code changes. PASS
- Authoritative Backend: Validation (empty q -> 400) enforced server-side. PASS
- Minimal Change: Single narrow change to GET /tasks behavior; no model or unrelated changes. PASS
- Contract Before Code: API contract for GET /tasks (q and tag) documented in contracts/. PASS
- Constraints: Backend FastAPI with in-memory storage; frontend static. PASS

## Project Structure

### Documentation (this feature)

```text
specs/002-title-search/
├── plan.md              # This file (/speckit.plan output)
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/
    └── search-contract.md  # Phase 1 output
```

### Source Code (repository root)

```text
app/
├── __init__.py
└── main.py              # FastAPI app with /tasks endpoints

tests/
├── test_example.py
└── test_filter_by_tag.py (existing)
```

**Structure Decision**: Single FastAPI app with tests under tests/. No additional projects or packages required.

## Complexity Tracking

No constitution violations; section not applicable.
