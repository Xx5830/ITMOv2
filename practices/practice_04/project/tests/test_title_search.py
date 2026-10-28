"""Поиск GET /tasks?q=... (title-search).

Паттерн: Arrange - Act - Assert, один сценарий на тест.
Тестируем через публичный HTTP-интерфейс.
"""
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


def test_q_filters_by_case_insensitive_substring():
    _add("Buy milk", ["shop"])  # match
    _add("Read book", ["read"])  # no match

    response = client.get("/tasks", params={"q": "milk"})

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["Buy milk"]


def test_q_is_case_insensitive():
    _add("Buy milk", ["shop"])  # match

    response = client.get("/tasks", params={"q": "MILK"})

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["Buy milk"]


def test_q_no_matches_returns_empty_list():
    _add("Buy milk", ["shop"])  # existing

    response = client.get("/tasks", params={"q": "zzz"})

    assert response.status_code == 200
    assert response.json() == []


def test_without_q_returns_all_tasks():
    _add("a", ["work"]) 
    _add("b", ["home"]) 

    response = client.get("/tasks")

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["a", "b"]


@pytest.mark.parametrize("value", ["", "   "])
def test_blank_q_is_rejected_with_400(value):
    _add("a", ["work"]) 

    response = client.get("/tasks", params={"q": value})

    assert response.status_code == 400


def test_q_trimmed_edges_are_ignored():
    _add("Buy milk", ["shop"]) 

    response = client.get("/tasks", params={"q": "  milk  "})

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["Buy milk"]


def test_q_longer_than_100_rejected_with_400():
    _add("a", ["work"]) 
    long_q = "x" * 101

    response = client.get("/tasks", params={"q": long_q})

    assert response.status_code == 400


def test_q_combines_with_tag_and_logic():
    _add("Buy milk", ["shop"])            # q matches, tag=shop
    _add("Milk report", ["work"])          # q matches, tag=work (expected)
    _add("Milk chocolate", ["fun"])        # q matches, tag=fun

    response = client.get("/tasks", params={"q": "milk", "tag": "work"})

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["Milk report"]
