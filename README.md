# 📋 TaskMaster Pro

> **You've just been hired. Congratulations — and condolences.**
>
> Your predecessor, Alex, built this task management application and then quietly
> disappeared one Monday morning, leaving behind a half-working codebase, zero
> documentation, and a sticky note that just said *"good luck lol"*.
>
> Your job: **fix it.**

---

## The Situation

TaskMaster Pro is a command-line application that lets users manage a to-do list.
It *almost* works. Tasks can be created, listed, completed, deleted, searched,
filtered, saved, and reported on.

But there are bugs. Some will crash the app immediately. Some are sneaky logic
errors that produce wrong results. Some are lurking, waiting for a specific input
to detonate.

Every bug has been filed as a **GitHub Issue**. Your job is to find the bug, fix
it, and close the issue with a pull request.

---

## Project Structure

```
taskmaster/
├── task_manager.py        # Main application (← the crime scene)
├── tests/
│   └── test_task_manager.py   # Test suite (some tests already fail)
├── data/                  # Auto-created when you save tasks
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-instructor>/taskmaster-pro.git
cd taskmaster-pro
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python task_manager.py
```

### 5. Run the tests

```bash
python -m pytest tests/ -v
```

You'll see several tests failing right away — that's the point.

---

## How to Contribute a Fix

1. **Pick an issue** from the Issues tab. Comment on it so classmates know you're
   working on it.
2. **Create a branch** named after the issue number:
   ```bash
   git checkout -b fix/issue-3-priority-validation
   ```
3. **Fix the bug** and make sure the relevant test passes.
4. **Commit** your change with a descriptive message:
   ```bash
   git commit -m "Fix #3: correct priority assignment from == to ="
   ```
5. **Open a Pull Request** against `main`. Reference the issue in the PR description.
6. Your instructor will review and merge it — then the points are yours!

---

## Grading / Points

Each issue is worth a set number of points (listed in the issue). Points are
awarded when your pull request is **reviewed and merged**. First correct fix wins
the points — no duplicate submissions.

| Difficulty | Points |
|------------|--------|
| 🟢 Easy    | 5 pts  |
| 🟡 Medium  | 10 pts |
| 🔴 Hard    | 15 pts |

---

## Rules

- You may discuss bugs with classmates, but **code must be your own**.
- You must include or update a test that proves the bug is fixed.
- No rewriting the whole file — targeted fixes only.
- Have fun. Alex would have wanted that. Probably.
