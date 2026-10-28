# Практика 5 — рабочий журнал (SDD в существующем проекте, OpenSpec)

Официального README от курса на эту практику ещё нет в апстриме — есть только
презентация [`prenetation.pdf`](prenetation.pdf) (16 слайдов, OpenSpec в
brownfield-проекте, 90 минут). Этот файл — не задание курса, а мой рабочий
журнал по прохождению обеих частей презентации.

Проект, на котором проходится цикл: [`practices/practice_04/project`](../practice_04/project)
(graph-by-tags, FastAPI + d3-force) — тот же брownfield-проект, что и в
практике 4. Сама установка и артефакты OpenSpec живут внутри него, в
`practices/practice_04/project/openspec/`.

## План (по слайдам презентации)

### Часть 1 — полный цикл одной фичи
1. Подготовка — установка OpenSpec CLI, `openspec init --profile core`.
2. Исследование — выбор одной маленькой фичи из списка 10 идей, `explore`
   (код и тесты читаются, не меняются).
3. Требования — `propose`: цель, 3–5 условий приёмки, границы.
4. Обсуждение — независимый review предложения до разрешения на код.
5. Код — `apply`: реализация строго по согласованному плану, TDD.
6. Проверки — независимый прогон тестов проекта, приёмка.
7. Архив — `sync` + `archive`: обновление `specs/`, change уходит в историю.

### Часть 2 — настройка OpenSpec под себя
8. Добавление одного project rule в `openspec/config.yaml`.
9. Проверка действия правила на отдельном черновом change, diff до/после.

## Журнал

_(заполняется по ходу прохождения — см. ниже)_

## Статус

В процессе.

## Что сделано

**Установка.** Node ≥ 20.19, `npm install -g @fission-ai/openspec@1.14.1`, `openspec init --profile core`
в `practices/practice_04/project`. Бинарь лежит в `~/.npm-global/bin`, поэтому его нужно добавить в `PATH`.

**Фича.** `GET /tasks?tag=X` — фильтр существующего списка по тегу (из списка идей на слайде 5).

**Цикл OpenSpec (часть 1)**

| Шаг | Артефакт |
|---|---|
| Explore | [`explore-notes.md`](explore-notes.md): что уже есть, 5 спорных вопросов, baseline 2/2 |
| Propose | `proposal.md`, дельта спеки, `design.md`, `tasks.md`; `openspec validate --strict` — valid |
| Решения человека | пустой/пробельный `tag` → 400; строго один `tag`; `strip()`; тесты в этом же change |
| Apply (TDD) | `tests/test_filter_by_tag.py` (7 кейсов): красные 5/9, затем зелёные 9/9; правка только `GET /tasks` в `app/main.py` |
| Archive | `openspec/changes/archive/2026-10-28-get-tasks-by-tag/`, основная спека `openspec/specs/task-filtering/spec.md` |

**Настройка под себя (часть 2).** В `openspec/config.yaml` добавлено `rules.design`:
«Объясни взаимодействие компонентов диаграммой Mermaid». Правило подхватывается следующим
`openspec instructions design`; проверить его на новом change.

## Проверка

```sh
cd practices/practice_04/project && sh scripts/check.sh    # 9 passed
PATH="$HOME/.npm-global/bin:$PATH" openspec validate --all --no-interactive
```

## Не сделано

ДЗ 5 (второй SDD-фреймворк, две согласованные спеки UI и логики) — отдельная работа.
