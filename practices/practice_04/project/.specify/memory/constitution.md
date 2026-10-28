# graph-by-tags Constitution

## Core Principles

### I. Test-First (NON-NEGOTIABLE)
Тест пишется раньше кода и должен упасть. Новые тесты следуют `tests/test_example.py`
(Arrange-Act-Assert, один сценарий на тест, через публичный HTTP-интерфейс).

### II. Authoritative Backend
Валидация и фильтрация данных живёт на бэкенде; фронт не дублирует правила, а показывает ответ сервера.

### III. Minimal Change
Одна фича - один узкий change. Не менять модели, POST-валидацию, `docs/requirements.md`
и `scripts/check.sh` без явного поручения.

### IV. Contract Before Code
Если фича затрагивает и UI, и API, общий контракт (параметры, коды ответов, состояния UI)
согласуется письменно до реализации.

## Constraints
Бэкенд: FastAPI, in-memory хранилище. Фронт: чистый HTML/JS + d3-force, без сборки.

## Workflow
`sh scripts/check.sh` зелёный перед каждым коммитом. Решения о поведении принимает человек.

**Version**: 1.0.0 | **Ratified**: 2026-10-28
