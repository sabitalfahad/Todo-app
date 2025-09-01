"""
TodoApp
=======

A simple, file-based Todo list application that manages tasks persistently.

Features:
- Add new todos
- Edit existing todos
- Mark todos as complete
- Clear all todos
- Persistent storage using text file
- Type hints for better code clarity
- Human-friendly string representation
- Easy to integrate into other projects

Usage:
    app = TodoApp()
    app.add("Buy groceries")
    app.edit(0, "Buy organic groceries")
    app.complete(0)  # Mark as done
    todos = app.get_all()
    print(app)  # Human-friendly output
"""

from typing import List, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

FILEPATH = "todos.txt"

class TodoApp:
    """A Todo list application with persistent storage."""

    def __init__(self, filename: str = FILEPATH) -> None:
        """Initialize TodoApp with optional custom filename."""
        self.filename = filename
        self.todos: List[str] = self.load()

    def load(self) -> List[str]:
        """Load todos from the storage file."""
        try:
            Path(self.filename).parent.mkdir(parents=True, exist_ok=True)
            with open(self.filename, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            logging.warning("Todo file not found. Starting with an empty list.")
            return []
        except Exception as e:
            logging.error(f"Error loading todos: {e}")
            return []

    def save(self) -> None:
        """Save the current todos to the storage file."""
        try:
            Path(self.filename).parent.mkdir(parents=True, exist_ok=True)
            with open(self.filename, "w", encoding="utf-8") as f:
                f.writelines(f"{todo}\n" for todo in self.todos)
        except Exception as e:
            logging.error(f"Error saving todos: {e}")

    def add(self, todo: str) -> bool:
        """Add a new todo to the list."""
        todo = todo.strip()
        if todo:
            self.todos.append(todo)
            self.save()
            logging.info(f"Added todo: {todo}")
            return True
        return False

    def edit(self, index: int, new_text: str) -> bool:
        """Edit an existing todo."""
        new_text = new_text.strip()
        if 0 <= index < len(self.todos) and new_text:
            old = self.todos[index]
            self.todos[index] = new_text
            self.save()
            logging.info(f"Edited todo: '{old}' → '{new_text}'")
            return True
        return False

    def complete(self, index: Optional[int] = None) -> None:
        """Mark a todo as completed by removing it."""
        if index is None:
            logging.info("Cleared all todos")
            self.todos.clear()
        elif 0 <= index < len(self.todos):
            logging.info(f"Completed todo: {self.todos[index]}")
            self.todos.pop(index)
        self.save()

    def get_all(self) -> List[str]:
        """Get all current todos."""
        return self.todos.copy()

    def __len__(self) -> int:
        """Return number of todos."""
        return len(self.todos)

    def __str__(self) -> str:
        """Return a human-friendly list of todos."""
        if not self.todos:
            return "No todos yet!"
        return "\n".join(f"{i+1}. {todo}" for i, todo in enumerate(self.todos))