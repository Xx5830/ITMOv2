# Feature Specification: Поиск задач по названию (логика / API)

**Feature Branch**: `001-title-search`
**Created**: 2026-10-28
**Status**: Draft
**Input**: "Хочу искать задачи по части названия: GET /tasks?q=..."
**Команда**: 2 (логика и API). Парная спека UI: `openspec/changes/search-tasks-ui/`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Найти задачи по части названия (Priority: P1)

Клиент API передаёт `q` и получает только задачи, в названии которых есть эта подстрока.

**Why this priority**: без этого поиск не существует; остальное его дополняет.

**Independent Test**: создать задачи "Buy milk", "Read book", вызвать `GET /tasks?q=MILK`, получить только "Buy milk".

**Acceptance Scenarios**:

1. **Given** задачи "Buy milk" и "Read book", **When** `GET /tasks?q=milk`, **Then** 200 и список из одной задачи "Buy milk".
2. **Given** те же задачи, **When** `GET /tasks?q=MILK`, **Then** результат тот же (регистр не важен).
3. **Given** те же задачи, **When** `GET /tasks?q=zzz`, **Then** 200 и пустой список `[]`.
4. **Given** три совпадающие задачи, **When** `GET /tasks?q=b`, **Then** порядок в ответе совпадает с порядком создания.
5. **Given** любые задачи, **When** `GET /tasks` без `q`, **Then** возвращаются все задачи, как раньше.

### User Story 2 - Отвергнуть пустой запрос (Priority: P2)

Пустой или пробельный `q` - ошибка клиента, а не «показать всё».

**Independent Test**: `GET /tasks?q=%20%20` возвращает 400 с полем `detail`.

**Acceptance Scenarios**:

1. **Given** любые задачи, **When** `GET /tasks?q=`, **Then** 400 и JSON `{"detail": "..."}`.
2. **Given** любые задачи, **When** `GET /tasks?q=%20%20`, **Then** 400.

### User Story 3 - Совместить поиск с фильтром по тегу (Priority: P3)

`q` и `tag` можно передать вместе: условия объединяются по «И».

**Independent Test**: задачи "Buy milk" [shop], "Milk report" [work]; `GET /tasks?q=milk&tag=work` вернёт только "Milk report".

**Acceptance Scenarios**:

1. **Given** задачи выше, **When** `q=milk&tag=work`, **Then** только "Milk report".
2. **Given** `q=milk&tag=`, **Then** 400 (правило пустого `tag` уже действует).

### Edge Cases

- `q` с пробелами по краям (` milk `): края отбрасываются, поиск идёт по `milk`.
- Внутренние пробелы сохраняются: `q=buy milk` ищет подстроку целиком.
- `q` длиннее 100 символов: 400 (названия не длиннее 100, совпадений быть не может).
- Спецсимволы (`%`, `.`, `*`) ищутся буквально, не как шаблон.
- Несколько значений `?q=a&q=b`: берётся одно значение, поведение по правилам FastAPI (последнее).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `GET /tasks` MUST принимать необязательный `q`.
- **FR-002**: При `q` MUST возвращаться только задачи, где `q.strip()` входит в `title` без учёта регистра.
- **FR-003**: Порядок результата MUST совпадать с порядком создания.
- **FR-004**: Пустой/пробельный `q` или `q` длиннее 100 символов после `strip` MUST давать 400 с `{"detail": <строка>}`.
- **FR-005**: `q` MUST комбинироваться с `tag` по «И».
- **FR-006**: Без `q` поведение `GET /tasks` MUST остаться прежним.
- **FR-007**: Нет совпадений MUST давать 200 и `[]`, не 404.

### Key Entities

- **Task**: `{id: int, title: str, tags: list[str]}` - без изменений.

## Success Criteria *(mandatory)*

- **SC-001**: Все сценарии выше покрыты автотестами, `sh scripts/check.sh` зелёный.
- **SC-002**: Существующие 9 тестов проходят без правок.
- **SC-003**: Изменён только обработчик `GET /tasks` в `app/main.py`.

## Assumptions

- Хранилище остаётся in-memory, поиск линейный.
- Нормализация Unicode и поиск по тегам-подстрокам вне объёма.
