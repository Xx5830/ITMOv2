# Tasks: title-search

**Input**: Design documents from `/specs/002-title-search/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL; this plan lists implementation tasks only, aligned with the project's test-first principle but leaving test authoring to separate commands if requested.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Ensure feature docs present at specs/002-title-search/ (plan.md, spec.md, research.md, data-model.md, contracts/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core prerequisites that MUST be complete before ANY user story can be implemented

- [X] T002 Verify existing GET /tasks tag filter contract alignment with specs/001-title-search/contracts/search-contract.md and update cross-references in specs/002-title-search/contracts/search-contract.md if needed

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 — Найти задачи по части названия (Priority: P1) 🎯 MVP

**Goal**: Добавить необязательный параметр q для регистронезависимого поиска по подстроке в title

**Independent Test**: 
- Create tasks "Buy milk" and "Read book"; GET /tasks?q=milk returns only "Buy milk"
- GET /tasks?q=MILK returns same
- GET /tasks?q=zzz returns 200 and []

### Implementation for User Story 1

- [X] T003 [US1] Add contract example cases for q-only filtering in specs/002-title-search/contracts/search-contract.md
- [X] T004 [US1] Update quickstart scenarios for US1 in specs/002-title-search/quickstart.md

**Checkpoint**: At this point, contract and quickstart document q-only behavior; ready for tests/implementation

---

## Phase 4: User Story 2 — Отвергнуть пустой запрос (Priority: P2)

**Goal**: Пустой/пробельный q → 400 с detail

**Independent Test**:
- GET /tasks?q= and GET /tasks?q=%20%20 return 400 with detail

### Implementation for User Story 2

- [X] T005 [US2] Add 400 error contract examples for empty/whitespace q in specs/002-title-search/contracts/search-contract.md
- [X] T006 [US2] Update quickstart with empty/whitespace q error validation in specs/002-title-search/quickstart.md

**Checkpoint**: Contract covers error semantics; quickstart updated

---

## Phase 5: User Story 3 — Совместить поиск с фильтром по тегу (Priority: P3)

**Goal**: Совместная фильтрация q и tag по логике «И»

**Independent Test**:
- Given tasks "Buy milk" [shop] and "Milk report" [work]; GET /tasks?q=milk&tag=work returns only "Milk report"

### Implementation for User Story 3

- [X] T007 [US3] Document combined q+tag contract and example in specs/002-title-search/contracts/search-contract.md
- [X] T008 [US3] Update quickstart with combined filter scenario in specs/002-title-search/quickstart.md

**Checkpoint**: All user story contracts and quickstart scenarios complete

---

## Phase N: Polish & Cross-Cutting

- [X] T009 [P] Review and align data-model constraints references in specs/002-title-search/data-model.md
- [X] T010 [P] Ensure links between plan.md/spec.md/contracts/quickstart.md are consistent within specs/002-title-search/

---

## Dependencies & Execution Order

- Phase 1 → Phase 2 → US1 (MVP) → US2 → US3 → Polish

### Story Dependencies

- US2 depends on US1 contracts being in place (empty-q semantics build on q parameter definition)
- US3 depends on US1 (q) and existing tag behavior

### Parallel Opportunities

- T009 and T010 can run in parallel after user story documents are present

## Implementation Strategy

- MVP: Deliver US1 (q-only filtering) first. Stop and validate with quickstart.
- Incrementally add US2 (empty-q 400) and US3 (q+tag AND), validating at each checkpoint.
