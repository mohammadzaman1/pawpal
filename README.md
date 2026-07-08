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

## 📐 Smarter Scheduling

| Feature           | Method(s)                                          | Notes                                                                           |
| ----------------- | -------------------------------------------------- | ------------------------------------------------------------------------------- |
| Task sorting      | `Scheduler.sort_by_time()`                         | Sorts tasks by `HH:MM` strings and keeps unscheduled tasks last.                |
| Filtering         | `Scheduler.filter_tasks()`                         | Filters by completion status, pet name, or both using the current owner roster. |
| Conflict handling | `Scheduler.detect_time_conflicts()`                | Returns warning messages for exact time collisions instead of crashing.         |
| Recurring tasks   | `Task.mark_completed()`, `Task._next_occurrence()` | Creates the next daily, weekly, or custom recurring instance after completion.  |

The scheduler currently uses lightweight rules that are easy to explain and test. It sorts with a simple time key, filters with linear scans, warns on exact time matches, and advances recurring tasks by creating a fresh next instance.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
