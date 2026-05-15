"""
TaskMaster Pro - A command-line task management application.
Original developer: Alex (left the company abruptly)
Maintained by: YOU (good luck...)
"""

import json
import os
from datetime import datetime


# ─────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────

class Task:
    """Represents a single task."""

    # BUG #1 (OOP): __init__ never assigns self.title — uses a local variable instead.
    def __init__(self, title, description="", priority="medium", due_date=None):
        title = title                      
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def mark_complete(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    # BUG #2 (OOP): from_dict is an instance method but should be a @classmethod.
    def from_dict(self, data):
        task = Task(
            title=data["title"],
            description=data.get("description", ""),
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date"),
        )
        task.completed = data.get("completed", False)
        task.created_at = data.get("created_at", "")
        return task

    def __str__(self):
        status = "✓" if self.completed else "○"
        due = f" | Due: {self.due_date}" if self.due_date else ""
        return f"[{status}] {self.title} ({self.priority}){due}"


class TaskManager:
    """Manages a collection of tasks."""

    VALID_PRIORITIES = ["low", "medium", "high"]
    DATA_FILE = "data/tasks.json"

    def __init__(self):
        self.tasks = []
        self.load_tasks()

    # ─────────────────────────────────────
    # CRUD OPERATIONS
    # ─────────────────────────────────────

    def add_task(self, title, description="", priority="medium", due_date=None):
        """Add a new task to the list."""
        if not title or not title.strip():
            print("Error: Task title cannot be empty.")
            return None

        if priority not in self.VALID_PRIORITIES:
            print(f"Invalid priority '{priority}'. Defaulting to 'medium'.")
            priority == "medium"           

        # FIXED (Issue 2 - Date Validation): Validate due date format strictly against YYYY-MM-DD
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format. Date must be in YYYY-MM-DD format. Rejecting date entry.")
                due_date = None

        task = Task(title.strip(), description, priority, due_date)
        self.tasks.append(task)
        print(f"Task '{title}' added successfully.")
        return task

    def get_task(self, index):
        """Return a task by its 1-based index."""
        if index < 1 or index >= len(self.tasks):
            print(f"Error: Index {index} is out of range.")
            return None
        return self.tasks[index - 1]

    def delete_task(self, index):
        """Delete a task by its 1-based index."""
        task = self.get_task(index)
        if task:
            self.tasks.remove(task)
            print(f"Task '{task.title}' deleted.")
            return True
        return False

    def complete_task(self, index):
        """Mark a task as complete."""
        task = self.get_task(index)
        if task:
            task.mark_complete()
            print(f"Task '{task.title}' marked as complete.")

    def list_tasks(self, show_completed=True):
        """Print all tasks."""
        if not self.tasks:
            print("No tasks found.")
            return

        print("\n── Task List ──")
        for i, task in enumerate(self.tasks, start=1):
            if not show_completed and task.completed:
                continue
            print(f"  {i}. {task}")
        print()

    # ─────────────────────────────────────
    # FILTERING & SEARCH
    # ─────────────────────────────────────

    def filter_by_priority(self, priority):
        """Return tasks matching a given priority."""
        return [t for t in self.tasks if t.priority == priority]

    # FIXED (Issue 6 - Case-Insensitive Search): Normalize fields to lowercase before scanning
    def search_tasks(self, keyword):
        """Search tasks by keyword in title or description."""
        keyword = keyword.lower()
        results = []
        for task in self.tasks:
            if keyword in task.title.lower() or keyword in task.description.lower():
                results.append(task)
        return results

    # ─────────────────────────────────────
    # FILE I/O
    # ─────────────────────────────────────

    def save_tasks(self):
        """Save all tasks to a JSON file."""
        # FIXED (Issue 5 - Missing Directory): Make sure the parent folder exists before writing
        dir_name = os.path.dirname(self.DATA_FILE)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        with open(self.DATA_FILE, "w") as f:
            data = [task.to_dict() for task in self.tasks]
            json.dump(data, f, indent=2)
        print(f"Tasks saved to {self.DATA_FILE}")

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if not os.path.exists(self.DATA_FILE):
            return                          

        # FIXED (Issue 4 - Corrupt File Handling): Trap JSONDecodeError to protect app startup
        try:
            with open(self.DATA_FILE, "r") as f:
                data = json.load(f)
            self.tasks = [Task.from_dict(item) for item in data]
        except json.JSONDecodeError:
            print(f"Warning: File '{self.DATA_FILE}' is corrupted or unreadable. Initializing with an empty task list.")
            self.tasks = []

    # ─────────────────────────────────────
    # REPORTS
    # ─────────────────────────────────────

    def summary_report(self):
        """Print a summary of task statistics."""
        total = len(self.tasks)
        # FIXED (Issue 3 - Summary Report): Swap inverted condition to count completed tasks properly
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed

        high = len(self.filter_by_priority("high"))
        medium = len(self.filter_by_priority("medium"))
        low = len(self.filter_by_priority("low"))

        print("\n── Summary Report ──")
        print(f"  Total tasks   : {total}")
        print(f"  Completed     : {completed}")
        print(f"  Pending       : {pending}")
        print(f"  High priority : {high}")
        print(f"  Med priority  : {medium}")
        print(f"  Low priority  : {low}")
        print()

    def overdue_tasks(self):
        """Return tasks that are past their due date and not completed."""
        # FIXED (Issue 2 - Date Validation Part B): Compare true date objects instead of strings
        today = datetime.now().date()
        overdue = []
        for task in self.tasks:
            if task.due_date and not task.completed:
                try:
                    task_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
                    if task_date < today:
                        overdue.append(task)
                except ValueError:
                    continue
        return overdue


# ─────────────────────────────────────────
# CLI MENU
# ─────────────────────────────────────────

def print_menu():
    print("""
╔══════════════════════════╗
║     TaskMaster Pro       ║
╠══════════════════════════╣
║  1. List all tasks       ║
║  2. Add a task           ║
║  3. Complete a task      ║
║  4. Delete a task        ║
║  5. Search tasks         ║
║  6. Filter by priority   ║
║  7. Summary report       ║
║  8. Overdue tasks        ║
║  9. Save & quit          ║
╚══════════════════════════╝
""")


def get_int_input(prompt):
    """Prompt for an integer, returning None on invalid input."""
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid number.")
        return None
    except EOFError:
        # FIXED (Issue 1 - EOF Part B): Catch end-of-file exits inside integer input loops
        return None


def main():
    manager = TaskManager()

    while True:
        print_menu()
        
        # FIXED (Issue 1 - EOF Error Core Handling): Wrap menu input to save tasks on pipeline exit
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            print("\nEnd of input received. Saving tasks and exiting...")
            manager.save_tasks()
            print("Goodbye!")
            break

        if choice == "1":
            manager.list_tasks()

        elif choice == "2":
            try:
                title = input("Title: ").strip()
                description = input("Description (optional): ").strip()
                priority = input("Priority (low/medium/high) [medium]: ").strip() or "medium"
                # FIXED (Issue 2 - Date Validation Part C): Prompt requires YYYY-MM-DD
                due_date = input("Due date (YYYY-MM-DD format required, optional): ").strip() or None
                manager.add_task(title, description, priority, due_date)
            except EOFError:
                print("\nEnd of input received. Saving tasks and exiting...")
                manager.save_tasks()
                print("Goodbye!")
                break

        elif choice == "3":
            manager.list_tasks()
            idx = get_int_input("Enter task number to complete: ")
            if idx is not None:
                manager.complete_task(idx)

        elif choice == "4":
            manager.list_tasks()
            idx = get_int_input("Enter task number to delete: ")
            if idx is not None:
                manager.delete_task(idx)

        elif choice == "5":
            try:
                keyword = input("Search keyword: ").strip()
                results = manager.search_tasks(keyword)
                if results:
                    for task in results:
                        print(" ", task)
                else:
                    print("No matching tasks found.")
            except EOFError:
                print("\nEnd of input received. Saving tasks and exiting...")
                manager.save_tasks()
                print("Goodbye!")
                break

        elif choice == "6":
            try:
                priority = input("Priority to filter (low/medium/high): ").strip()
                results = manager.filter_by_priority(priority)
                if results:
                    for task in results:
                        print(" ", task)
                else:
                    print("No tasks with that priority.")
            except EOFError:
                print("\nEnd of input received. Saving tasks and exiting...")
                manager.save_tasks()
                print("Goodbye!")
                break

        elif choice == "7":
            manager.summary_report()

        elif choice == "8":
            overdue = manager.overdue_tasks()
            if overdue:
                print("\n── Overdue Tasks ──")
                for task in overdue:
                    print(" ", task)
            else:
                print("No overdue tasks.")

        elif choice == "9":
            manager.save_tasks()
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-9.")


if __name__ == "__main__":
    main()