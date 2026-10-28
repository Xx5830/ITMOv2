"""Фильтр GET /tasks?tag=... (change get-tasks-by-tag)."""
import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_storage():
    main._tasks.clear()
    main._next_id = 1
    yield
    main._tasks.clear()
    main._next_id = 1


def _add(title, tags):
    assert client.post("/tasks", json={"title": title, "tags": tags}).status_code == 201


def test_without_tag_returns_all_tasks():
    _add("a", ["work"])
    _add("b", ["home"])

    response = client.get("/tasks")

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["a", "b"]


def test_matching_tag_returns_only_matching_tasks_in_order():
    _add("a", ["work", "urgent"])
    _add("b", ["home"])
    _add("c", ["work"])

    response = client.get("/tasks", params={"tag": "work"})

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["a", "c"]


def test_unknown_tag_returns_empty_list():
    _add("a", ["work"])

    response = client.get("/tasks", params={"tag": "unknown"})

    assert response.status_code == 200
    assert response.json() == []


def test_matching_is_case_sensitive():
    _add("a", ["Work"])

    response = client.get("/tasks", params={"tag": "work"})

    assert response.json() == []


def test_surrounding_whitespace_in_tag_is_ignored():
    _add("a", ["work"])

    response = client.get("/tasks", params={"tag": "  work  "})

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["a"]


@pytest.mark.parametrize("value", ["", "   "])
def test_blank_tag_is_rejected_with_400(value):
    _add("a", ["work"])

    response = client.get("/tasks", params={"tag": value})

    assert response.status_code == 400
