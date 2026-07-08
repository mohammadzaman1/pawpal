# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
Mochi: Morning feeding (10 min, priority: high)
Biscuit: Afternoon walk (30 min, priority: high)
Mochi: Litter box cleanup (15 min, priority: medium)
```

## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

These tests cover task sorting, recurring task completion, conflict detection, and a basic empty-schedule edge case.

Successful test run:

```text
============================= test session starts ==============================
platform darwin -- Python 3.12.5, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/ashik/Codes/Codepath_AI/pawpal
plugins: anyio-4.14.1
collected 7 items

tests/test_pawpal.py .......                                             [100%]

============================== 7 passed in 0.01s ===============================
```

Confidence Level: 5/5 stars

## Features

- Time-based sorting with `Scheduler.sort_by_time()`, which orders tasks by `HH:MM` and keeps unscheduled tasks at the end.
- Priority-aware scheduling with `Scheduler.schedule_tasks()`, which fills the day by choosing high-priority tasks first and skipping tasks that do not fit in the available time.
- Filtering with `Scheduler.filter_tasks()`, which can narrow results by completion status, pet name, or both.
- Conflict warnings with `Scheduler.detect_time_conflicts()`, which groups tasks by exact time and reports collisions instead of raising an error.
- Recurring task completion with `Task.mark_completed()` and `Task._next_occurrence()`, which create the next daily, weekly, or custom repeat instance when a task is completed.
- Cached schedule views with `Scheduler.today_tasks`, `Scheduler.tasks_left`, and `Scheduler.completed_tasks`, which stay in sync after scheduling, editing, and completion updates.

## Demo Walkthrough

1. Start on the Streamlit page and enter basic owner information, then add one or more pets with names, ages, species, and breeds.
2. Use the task form to assign care work to a specific pet. Each task captures a title, optional time, duration, and priority.
3. Click **Generate schedule** to build a plan for the day based on the available minutes you enter.
4. Review the schedule table to see tasks sorted by time, plus any leftover tasks that did not fit in the time budget.
5. Watch for conflict warnings when two tasks share the same time, and use the pet filter to focus on one animal’s schedule.

The example workflow is: add a pet, add a task, generate the schedule, and then review the results and warnings.

The main UI lets a user add pets, create tasks, choose a time budget, and inspect each pet’s task list alongside today’s schedule. It also shows completion counts and conflict warnings so the user can quickly understand how the plan was assembled.

Key scheduler behaviors shown in the app include sorting tasks by time, filtering tasks by pet or completion state, warning about exact time conflicts, and carrying recurring tasks forward after completion.

Sample CLI output from running `main.py`:

```text
Tasks sorted by time
----------------------
07:30 | Mochi: Morning feeding
09:00 | Mochi: Brush coat
09:00 | Biscuit: Vet follow-up
15:00 | Biscuit: Afternoon walk
18:00 | Mochi: Litter box cleanup

Completed tasks
----------------
Biscuit: Vet follow-up

Mochi tasks
------------
Litter box cleanup (18:00)
Morning feeding (07:30)
Brush coat (09:00)

Schedule warnings
-----------------
Warning: 2 tasks are scheduled at 09:00 -> Mochi: Brush coat, Biscuit: Vet follow-up
```
