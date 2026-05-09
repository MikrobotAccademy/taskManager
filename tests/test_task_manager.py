"""
Tests for TaskMaster Pro.

These tests are intentionally incomplete — part of your job is to
make the application work so that these pass, and to write additional
tests for cases that aren't covered yet.

Run with:  python -m pytest tests/test_task_manager.py -v
"""

import pytest
import os
import json
from task_manager import Task, TaskManager


# ── Task class tests ────────────────────────────────────────────────

class TestTask:

    def test_task_has_title(self):
        """A Task should store its title."""
        task = Task("Buy milk")
        assert task.title == "Buy milk"

    def test_task_default_priority(self):
        task = Task("Study Python")
        assert task.priority == "medium"

    def test_task_starts_incomplete(self):
        task = Task("Do laundry")
        assert task.completed is False

    def test_mark_complete(self):
        task = Task("Exercise")
        task.mark_complete()
        assert task.completed is True

    def test_to_dict_roundtrip(self):
        """to_dict and from_dict should produce equivalent tasks."""
        original = Task("Read a book", description="Chapter 1-3", priority="low")
        data = original.to_dict()
        restored = Task.from_dict(data)
        assert restored.title == original.title
        assert restored.description == original.description
        assert restored.priority == original.priority


# ── TaskManager tests ───────────────────────────────────────────────

class TestTaskManager:

    def setup_method(self):
        """Create a fresh manager (no saved state)."""
        # Temporarily redirect data file so tests don't touch the real one
        TaskManager.DATA_FILE = "data/test_tasks.json"
        self.manager = TaskManager()
        self.manager.tasks = []          # start clean

    def teardown_method(self):
        if os.path.exists("data/test_tasks.json"):
            os.remove("data/test_tasks.json")
        TaskManager.DATA_FILE = "data/tasks.json"

    # ── add_task ──

    def test_add_task_returns_task(self):
        task = self.manager.add_task("Write report")
        assert task is not None
        assert len(self.manager.tasks) == 1

    def test_add_task_empty_title_rejected(self):
        task = self.manager.add_task("")
        assert task is None
        assert len(self.manager.tasks) == 0

    def test_add_task_invalid_priority_defaults_to_medium(self):
        task = self.manager.add_task("Meeting", priority="URGENT")
        assert task is not None
        assert task.priority == "medium"

    # ── get_task ──

    def test_get_task_valid_index(self):
        self.manager.add_task("First task")
        self.manager.add_task("Second task")
        task = self.manager.get_task(2)
        assert task.title == "Second task"

    def test_get_task_last_index(self):
        """The last valid index should not return None."""
        self.manager.add_task("Only task")
        task = self.manager.get_task(1)
        assert task is not None

    def test_get_task_out_of_range(self):
        self.manager.add_task("Solo task")
        task = self.manager.get_task(99)
        assert task is None

    # ── complete / delete ──

    def test_complete_task(self):
        self.manager.add_task("Fix bug")
        self.manager.complete_task(1)
        assert self.manager.tasks[0].completed is True

    def test_delete_task(self):
        self.manager.add_task("Temporary task")
        self.manager.delete_task(1)
        assert len(self.manager.tasks) == 0

    # ── search / filter ──

    def test_search_case_insensitive(self):
        self.manager.add_task("Buy Groceries")
        results = self.manager.search_tasks("groceries")
        assert len(results) == 1

    def test_filter_by_priority(self):
        self.manager.add_task("High task", priority="high")
        self.manager.add_task("Low task", priority="low")
        results = self.manager.filter_by_priority("high")
        assert len(results) == 1

    def test_filter_case_insensitive(self):
        self.manager.add_task("Important thing", priority="high")
        results = self.manager.filter_by_priority("High")   # capital H
        assert len(results) == 1

    # ── save / load ──

    def test_save_creates_file(self):
        self.manager.add_task("Persistent task")
        self.manager.save_tasks()
        assert os.path.exists("data/test_tasks.json")

    def test_load_restores_tasks(self):
        self.manager.add_task("Remember me")
        self.manager.save_tasks()

        new_manager = TaskManager()
        new_manager.tasks = []
        new_manager.load_tasks()
        assert len(new_manager.tasks) == 1
        assert new_manager.tasks[0].title == "Remember me"

    def test_load_handles_corrupt_file(self):
        """A corrupted JSON file should not crash the app."""
        os.makedirs("data", exist_ok=True)
        with open("data/test_tasks.json", "w") as f:
            f.write("this is not valid json {{{{")
        try:
            self.manager.load_tasks()   # should NOT raise
        except Exception as e:
            pytest.fail(f"load_tasks() raised an exception on corrupt file: {e}")

    # ── summary report ──

    def test_summary_completed_count(self, capsys):
        self.manager.add_task("Task A")
        self.manager.add_task("Task B")
        self.manager.complete_task(1)
        self.manager.summary_report()
        captured = capsys.readouterr()
        assert "Completed     : 1" in captured.out
        assert "Pending       : 1" in captured.out
