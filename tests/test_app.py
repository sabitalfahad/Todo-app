# tests/test_app.py

import pytest
from src import TodoApp


@pytest.fixture
def todo_app(tmp_path):
    """Fixture to create a temporary TodoApp with its own storage file."""
    test_file = tmp_path / "test_todos.txt"
    return TodoApp(filename=str(test_file))


def test_add_todo(todo_app):
    assert todo_app.add("Buy milk") is True
    assert "Buy milk" in todo_app.get_all()


def test_add_empty_todo(todo_app):
    assert todo_app.add("") is False
    assert todo_app.get_all() == []


def test_edit_todo_success(todo_app):
    todo_app.add("Old Task")
    assert todo_app.edit(0, "New Task") is True
    assert todo_app.get_all() == ["New Task"]


def test_edit_invalid_index(todo_app):
    assert todo_app.edit(99, "Doesn't exist") is False


def test_complete_single(todo_app):
    todo_app.add("Task 1")
    todo_app.add("Task 2")
    todo_app.complete(0)
    assert todo_app.get_all() == ["Task 2"]


def test_complete_all(todo_app):
    todo_app.add("Task A")
    todo_app.add("Task B")
    todo_app.complete()  # clear all
    assert todo_app.get_all() == []
