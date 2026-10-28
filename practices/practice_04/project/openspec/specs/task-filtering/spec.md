# task-filtering Specification

## Purpose
Lets API clients list only the tasks that carry a given tag, instead of always receiving the full task list.

## Requirements

### Requirement: Filter tasks by a single tag
`GET /tasks` SHALL accept an optional query parameter `tag` and, when present, return only tasks whose tag list contains exactly that value, compared case-sensitively, preserving the original task order.

#### Scenario: No tag parameter returns all tasks
- **WHEN** a client requests `GET /tasks` without `tag`
- **THEN** the response is `200 OK` with all tasks

#### Scenario: Matching tag returns only matching tasks
- **WHEN** a client requests `GET /tasks?tag=work` and some tasks have the tag `work`
- **THEN** the response is `200 OK` containing only those tasks, in their original order

#### Scenario: No match returns an empty list
- **WHEN** a client requests `GET /tasks?tag=unknown` and no task has that tag
- **THEN** the response is `200 OK` with an empty list

#### Scenario: Matching is case-sensitive
- **WHEN** a task has the tag `Work` and a client requests `GET /tasks?tag=work`
- **THEN** that task is not returned

#### Scenario: Surrounding whitespace is ignored
- **WHEN** a client requests `GET /tasks?tag=%20work%20`
- **THEN** the result is the same as for `tag=work`

### Requirement: Reject an empty tag filter
When `tag` is present but empty or whitespace-only, `GET /tasks` SHALL respond with `400 Bad Request` instead of returning a list.

#### Scenario: Empty tag
- **WHEN** a client requests `GET /tasks?tag=`
- **THEN** the response is `400 Bad Request`

#### Scenario: Whitespace-only tag
- **WHEN** a client requests `GET /tasks?tag=%20%20`
- **THEN** the response is `400 Bad Request`
