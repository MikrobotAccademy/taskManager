# GitHub Issues — TaskMaster Pro
## Copy & paste each block into a new GitHub Issue

> **Setup instructions for instructor:**
> 1. Create a new GitHub repo called `taskmaster-pro`
> 2. Push all project files
> 3. Go to Issues → New Issue for each block below
> 4. Add the labels: `bug`, and one of `easy` / `medium` / `hard`
> 5. Pin this file somewhere private (don't commit it to the repo!)

---

---

## ISSUE #1 — Task titles are never saved on the object
**Label:** `bug` `easy`
**Points:** 🟢 5 points

### Description

When you add a task and then immediately list tasks, the title shows up fine.
But when tasks are saved to file and reloaded, all task titles come back
as `None` — or you get an `AttributeError: 'Task' object has no attribute 'title'`
when the app tries to display them.

### Steps to Reproduce

1. Run the app
2. Add a task called `"Buy groceries"`
3. Choose **Save & quit**
4. Re-open the app
5. List tasks

**Expected:** `Buy groceries` appears in the list  
**Actual:** `AttributeError` or task title shows as `None`

### Hints

- Look at the `Task.__init__` method closely.
- How is `title` being stored? Is it being attached to the object?
- Compare how `title` is handled vs how `description` is handled.

### Acceptance Criteria

- `test_task_has_title` passes
- `test_to_dict_roundtrip` passes
- Tasks survive a save → reload cycle with their title intact

---

---

## ISSUE #2 — Cannot load tasks from file (`Task.from_dict` crashes)
**Label:** `bug` `medium`
**Points:** 🟡 10 points

### Description

After saving tasks and restarting the app, it crashes immediately with a
`TypeError`. The error message looks something like:

```
TypeError: from_dict() takes 2 positional arguments but only 1 was given
```

Or the tasks load but all their fields are scrambled / empty.

### Steps to Reproduce

1. Add any task and save
2. Quit and re-run the app

**Expected:** Saved tasks are loaded and shown  
**Actual:** `TypeError` on startup

### Hints

- `from_dict` is supposed to be called as `Task.from_dict(data)` — a factory method.
- Look at how Python distinguishes between *instance methods* and *class methods*.
- What decorator turns a regular method into a class method? What does that change
  about the first parameter?

### Acceptance Criteria

- `test_load_restores_tasks` passes
- The app starts cleanly after a save-quit-restart cycle

---

---

## ISSUE #3 — Invalid priority is accepted without correction
**Label:** `bug` `easy`
**Points:** 🟢 5 points

### Description

If you enter a priority like `"URGENT"` or `"critical"`, the app prints
`"Invalid priority... Defaulting to 'medium'"` — but then saves the task
with the invalid priority anyway.

### Steps to Reproduce

1. Add a task
2. When prompted for priority, enter `"critical"`
3. List tasks

**Expected:** Task priority is shown as `medium`  
**Actual:** Task priority is shown as `critical`

### Hints

- Find the line that's supposed to reassign `priority` to `"medium"`.
- Look very carefully at the operator being used. Is it doing what you think?
- In Python, `==` and `=` look similar but do very different things.

### Acceptance Criteria

- `test_add_task_invalid_priority_defaults_to_medium` passes
- A task added with priority `"URGENT"` shows `medium` when listed

---

---

## ISSUE #4 — The last task in the list can never be selected
**Label:** `bug` `medium`
**Points:** 🟡 10 points

### Description

If you have, say, 3 tasks, and try to complete or delete task number 3,
the app says `"Error: Index 3 is out of range"` — even though task 3
clearly exists.

### Steps to Reproduce

1. Add exactly 3 tasks
2. Try to complete task **3**

**Expected:** Task 3 is marked complete  
**Actual:** `Error: Index 3 is out of range`

### Hints

- Find `get_task()` and look at the boundary check.
- Consider a list with 3 items. What are the valid 1-based indices?
  What values should pass the range check, and what should be rejected?
- Look at whether `>=` or `>` is appropriate here.

### Acceptance Criteria

- `test_get_task_last_index` passes
- `test_get_task_valid_index` passes
- Completing or deleting the last task in any list works correctly

---

---

## ISSUE #5 — Priority filter is case-sensitive (breaks silently)
**Label:** `bug` `easy`
**Points:** 🟢 5 points

### Description

Using the **Filter by priority** menu option only works if you type the
priority in *exactly* the right case. Typing `"High"` or `"HIGH"` returns
zero results even when high-priority tasks exist.

### Steps to Reproduce

1. Add a task with priority `high`
2. Choose **Filter by priority**
3. Type `High` (capital H)

**Expected:** The high-priority task is shown  
**Actual:** `"No tasks with that priority."`

### Hints

- Find `filter_by_priority()`.
- Python string comparison is case-sensitive. `"High" == "high"` is `False`.
- What string method converts a string to all lowercase?
- Should you normalize just the input, or both sides of the comparison?

### Acceptance Criteria

- `test_filter_case_insensitive` passes
- Filtering with `"HIGH"`, `"High"`, or `"high"` all return the same results

---

---

## ISSUE #6 — Task search is case-sensitive
**Label:** `bug` `easy`
**Points:** 🟢 5 points

### Description

Searching for `"groceries"` won't find a task titled `"Buy Groceries"`.
The search is case-sensitive, so users have to know the exact capitalization
used when the task was created.

### Steps to Reproduce

1. Add a task titled `"Buy Groceries"`
2. Search for `"groceries"` (lowercase)

**Expected:** Task is found  
**Actual:** No results

### Hints

- Find `search_tasks()`. The keyword is already lowercased.
- What about the fields being searched against — `task.title` and `task.description`?
- Apply the same lowercase transformation to those before comparing.

### Acceptance Criteria

- `test_search_case_insensitive` passes
- Searching is case-insensitive for both title and description

---

---

## ISSUE #7 — Saving tasks crashes if the `data/` folder doesn't exist
**Label:** `bug` `medium`
**Points:** 🟡 10 points

### Description

On a fresh clone of the repo (before the `data/` directory exists), choosing
**Save & quit** immediately crashes with:

```
FileNotFoundError: [Errno 2] No such file or directory: 'data/tasks.json'
```

### Steps to Reproduce

1. Clone the repo fresh (no `data/` folder present)
2. Add a task
3. Choose **Save & quit**

**Expected:** A `data/` folder is created and tasks are saved  
**Actual:** `FileNotFoundError`

### Hints

- Find `save_tasks()`.
- Before writing a file to a folder, you need to make sure that folder exists.
- Look up `os.makedirs()`. What argument do you pass to make it safe to call
  even if the directory already exists?

### Acceptance Criteria

- `test_save_creates_file` passes
- Running the app on a fresh clone and saving works without any errors

---

---

## ISSUE #8 — A corrupted save file crashes the app on startup
**Label:** `bug` `medium`
**Points:** 🟡 10 points

### Description

If `data/tasks.json` gets corrupted (e.g., manually edited incorrectly,
or the app crashed mid-write), the app refuses to start at all:

```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

The user loses access to the app entirely until they manually delete the file.

### Steps to Reproduce

1. Save some tasks
2. Open `data/tasks.json` in a text editor and break it (delete a `{`, etc.)
3. Re-run the app

**Expected:** A friendly error message is shown, and the app starts with an
empty task list  
**Actual:** Crash on startup

### Hints

- Find `load_tasks()`.
- Use a `try/except` block to catch JSON parsing errors.
- What exception does `json.load()` raise when the file is invalid?
- After catching it, print a helpful message and make sure `self.tasks` ends
  up as an empty list.

### Acceptance Criteria

- `test_load_handles_corrupt_file` passes
- A corrupted file prints a warning and starts the app with zero tasks

---

---

## ISSUE #9 — Summary report shows completed and pending counts swapped
**Label:** `bug` `medium`
**Points:** 🟡 10 points

### Description

The summary report shows the wrong numbers for completed vs pending tasks.
If you have 2 tasks and complete 1, the report says `Completed: 1, Pending: 1` —
OK so far — but if you complete *all* tasks, it shows `Completed: 0, Pending: 2`.
It's exactly backwards.

### Steps to Reproduce

1. Add 2 tasks
2. Complete task 1
3. View the **Summary report**

**Expected:** `Completed: 1 | Pending: 1`  
**Actual:** `Completed: 1 | Pending: 1` ← seems OK with 1 done, but try completing
both tasks and you'll see `Completed: 0, Pending: 2`

### Hints

- Find `summary_report()` and look at the line that calculates `completed`.
- It uses a generator expression with a condition — check the condition carefully.
- What's the difference between `if t.completed` and `if not t.completed`?

### Acceptance Criteria

- `test_summary_completed_count` passes
- Completing all tasks shows `Completed: N, Pending: 0`

---

---

## ISSUE #10 — Overdue task detection breaks with non-ISO date formats
**Label:** `bug` `hard`
**Points:** 🔴 15 points

### Description

The app lets users type any string as a due date (like `"01/05/2025"` or
`"tomorrow"`). These are stored as-is. The `overdue_tasks()` method then
compares dates as strings, which only works correctly for `YYYY-MM-DD` format.
Other formats produce silently wrong results — a task due `"01/05/2025"` is
treated as *not* overdue because `"01/..."` > `"2025-..."` in string comparison.

### Steps to Reproduce

1. Add a task with due date `01/05/2020` (clearly in the past)
2. Choose **Overdue tasks**

**Expected:** The task appears as overdue  
**Actual:** It does not appear (or the app crashes, depending on the value)

### What needs to be done

1. **Validate** the due date format in `add_task()` — only accept `YYYY-MM-DD`.
   If the format is wrong, print an error and reject the date (set it to `None`).
2. **Parse** dates properly in `overdue_tasks()` using `datetime.strptime()`.
3. Handle the `ValueError` that `strptime` raises on invalid input gracefully.

### Hints

- `datetime.strptime("2025-05-01", "%Y-%m-%d")` returns a `datetime` object
  you can compare with `<` and `>`.
- Wrap the parsing in a `try/except ValueError`.
- Update the prompt in `main()` to say `(YYYY-MM-DD format required)`.

### Acceptance Criteria

- Entering `"01/05/2025"` as a due date is rejected with a clear error message
- `overdue_tasks()` correctly identifies tasks past their due date
- Invalid stored dates are skipped gracefully (no crash)

---

---

## ISSUE #11 — App crashes on Ctrl+D / EOF instead of exiting cleanly
**Label:** `bug` `hard`
**Points:** 🔴 15 points

### Description

When running the app in a terminal and pressing `Ctrl+D` (Linux/Mac) or
`Ctrl+Z` (Windows) — or when feeding the app piped input that ends — it
crashes with:

```
EOFError: EOF when reading a line
```

A well-behaved CLI app should exit gracefully when it receives end-of-input.

### Steps to Reproduce

```bash
echo "9" | python task_manager.py    # Works fine
echo "" | python task_manager.py     # Crashes with EOFError
```

### Hints

- Find where `input()` is called in `main()`.
- Wrap the `input()` call in a `try/except EOFError`.
- When `EOFError` is caught, save tasks and break out of the loop cleanly —
  same as if the user chose option 9.
- Check if `get_int_input()` also needs the same treatment.

### Acceptance Criteria

- `echo "" | python task_manager.py` exits cleanly without a traceback
- Tasks are saved before the app exits on EOF

---

---

## ISSUE #12 — Invalid menu options are silently ignored
**Label:** `bug` `easy`
**Points:** 🟢 5 points

### Description

If you type anything other than `1`–`9` at the main menu (like `"hello"`,
`"0"`, or `"10"`), nothing happens. The menu reprints and the app continues,
but there's no feedback telling the user their input was invalid.

A junior developer started writing the fix, then left a comment instead of
finishing it.

### Steps to Reproduce

1. Run the app
2. Type `"hello"` at the menu prompt

**Expected:** `"Invalid option. Please choose 1-9."`  
**Actual:** The menu silently reprints with no message

### Hints

- Find the `else` branch at the bottom of the `while` loop in `main()`.
- There's a commented-out `print` statement. Uncomment it and make sure the
  message is accurate and helpful.

### Acceptance Criteria

- Entering an invalid option prints a clear error message
- The menu then reprints normally

---

---

# 🏆 Point Summary

| # | Title | Difficulty | Points |
|---|-------|------------|--------|
| 1 | Task titles never saved on the object | 🟢 Easy | 5 |
| 2 | `from_dict` crashes on load | 🟡 Medium | 10 |
| 3 | Invalid priority accepted without correction | 🟢 Easy | 5 |
| 4 | Last task can never be selected | 🟡 Medium | 10 |
| 5 | Priority filter is case-sensitive | 🟢 Easy | 5 |
| 6 | Search is case-sensitive | 🟢 Easy | 5 |
| 7 | Save crashes if `data/` folder missing | 🟡 Medium | 10 |
| 8 | Corrupted save file crashes startup | 🟡 Medium | 10 |
| 9 | Summary report shows counts swapped | 🟡 Medium | 10 |
| 10 | Overdue detection breaks on non-ISO dates | 🔴 Hard | 15 |
| 11 | App crashes on Ctrl+D / EOF | 🔴 Hard | 15 |
| 12 | Invalid menu options silently ignored | 🟢 Easy | 5 |
| | **TOTAL** | | **105 pts** |

---

# 🔑 Answer Key (Instructor Only — Do Not Commit!)

| Issue | Fix |
|-------|-----|
| #1 | Change `title = title` → `self.title = title` in `Task.__init__` |
| #2 | Add `@classmethod` decorator to `from_dict`; change `self` → `cls`; call `cls(...)` |
| #3 | Change `priority == "medium"` → `priority = "medium"` |
| #4 | Change `index >= len(self.tasks)` → `index > len(self.tasks)` |
| #5 | Change comparison to `t.priority == priority.lower()` (or normalize both) |
| #6 | Change to `keyword in task.title.lower() or keyword in task.description.lower()` |
| #7 | Add `os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)` before `open()` |
| #8 | Wrap `json.load()` in `try/except json.JSONDecodeError`, set `self.tasks = []` in except |
| #9 | Change `if not t.completed` → `if t.completed` in the `completed` sum |
| #10 | Validate date format with `datetime.strptime` in `add_task`; parse both dates in `overdue_tasks` |
| #11 | Wrap the `input()` in `main()` with `try/except EOFError`; also fix `get_int_input()` |
| #12 | Uncomment the `print("Invalid option...")` line in the `else` branch |
