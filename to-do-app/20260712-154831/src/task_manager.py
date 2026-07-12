"""
Task management logic for the To-Do App.

Pure functions and classes separate from route handlers,
so unit tests can import and call them directly.
"""


class Task:
    """Represents a single to-do item."""

    def __init__(self, task_id: int, text: str):
        self.id = task_id
        self.text = text
        self.completed = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "completed": self.completed,
        }


class TaskManager:
    """Manages a collection of tasks with add, delete, and toggle operations."""

    def __init__(self):
        self.tasks = []  # list[Task]
        self._next_id = 1

    def add_task(self, text: str) -> Task | None:
        """
        Add a new task if the text is non-empty after trimming.

        Returns the created Task object, or None if input was empty/whitespace.
        """
        trimmed = text.strip()
        if not trimmed:
            return None

        task = Task(self._next_id, trimmed)
        self.tasks.append(task)
        self._next_id += 1
        return task

    def get_tasks(self) -> list[dict]:
        """Return all tasks as a list of dictionaries."""
        return [t.to_dict() for t in self.tasks]

    def delete_task(self, task_id: int) -> bool:
        """Remove a task by ID. Returns True if found and removed, False otherwise."""
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return len(self.tasks) < before

    def toggle_complete(self, task_id: int) -> bool:
        """Toggle the completed status of a task. Returns True if found, False otherwise."""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                return True
        return False

    def get_task(self, task_id: int) -> dict | None:
        """Return a single task's data by ID, or None if not found."""
        for task in self.tasks:
            if task.id == task_id:
                return task.to_dict()
        return None
