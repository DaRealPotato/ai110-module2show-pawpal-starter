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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

```
  Today's Schedule for Jordan
========================================
08:00 — [Biscuit] Morning walk (30 min) [high]
  Why: Priority is high; 90 min remaining, task takes 30 min.
08:30 — [Biscuit] Feeding (10 min) [high]
  Why: Priority is high; 60 min remaining, task takes 10 min.
08:40 — [Mochi] Grooming (15 min) [medium]
  Why: Priority is medium; 50 min remaining, task takes 15 min.
08:55 — [Mochi] Playtime (20 min) [low]
  Why: Priority is low; 35 min remaining, task takes 20 min.
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The test suite (`tests/test_pawpal.py`) covers the core scheduling behaviors:

- Sorting correctness — `Scheduler.sort_by_time()` orders tasks chronologically by preferred time, pushes untimed tasks to the end, and preserves the original order for tasks with equal or missing times.
- Recurrence logic — completing a "daily" or "weekly" task via `Pet.complete_task()` marks the original done and appends a new occurrence due one interval later; non-recurring tasks and unknown/duplicate titles are handled without creating spurious tasks.
- Conflict detection — `Scheduler.detect_conflicts()` flags overlapping schedule entries, correctly treats back-to-back (non-overlapping) entries as conflict-free, and handles the empty-schedule case.
- Baseline checks that marking a task complete updates its status and that adding a task updates a pet's task list.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\arell\Codepath\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 15 items

tests\test_pawpal.py ...............                                     [100%]

============================= 15 passed in 0.07s ==============================
```

Confidence Level:(4/5)

All 15 tests pass, including boundary cases for sorting ties, back-to-back scheduling, and recurrence date math. Confidence isn't a full 5/5 because the tests exercise these behaviors in isolation there's no test yet that runs `Scheduler.generate()` end-to-end with recurring tasks re-entering the pool, or that checks conflict detection against `generate()`'s own output (which by construction never overlaps, so that path is currently unverified in combination).

## ✨ Features

- **Priority-based scheduling** — `Scheduler.generate()` sorts all pending tasks by priority (high → medium → low, stable for ties) and greedily fits each into the owner's remaining time budget, generating a plain-English reason for every placement (or skip) as it goes.
- **Sorting by time** — `Scheduler.sort_by_time()` orders tasks by their preferred time of day (ascending, minutes from midnight); tasks with no preferred time are sorted to the end rather than dropped or errored on.
- **Conflict warnings** — `Scheduler.detect_conflicts()` sweeps a generated schedule once (sorted by start time, O(n log n)) and flags any two entries whose time windows overlap, returning human-readable warning strings instead of raising — back-to-back (non-overlapping) tasks are correctly treated as conflict-free.
- **Daily & weekly recurrence** — `Task.next_occurrence()` + `Pet.complete_task()` let a task carry a `"daily"` or `"weekly"` recurrence; completing it marks the original done and automatically queues a fresh, incomplete instance due one interval later.
- **Task filtering** — `Owner.filter_tasks(completed=, pet_name=)` returns matching `(task, pet_name)` pairs by completion status, pet, or both, without requiring a full schedule regeneration.
- **Cross-pet task aggregation** — `Owner.get_all_tasks()` flattens tasks across every pet an owner has, so scheduling and sorting operate on the full daily load rather than per-pet.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their preferred `time` (minutes from midnight); tasks with no preferred time sort last. The main daily plan itself (`Scheduler.generate()`) sorts by `priority` first (high → medium → low), then fits each task into whatever time remains. |
| Filtering | `Owner.filter_tasks(completed=, pet_name=)` | Returns `(task, pet_name)` pairs filtered by completion status, pet name, or both — e.g. "show me Biscuit's pending tasks." |
| Conflict handling | `Scheduler.detect_conflicts()` | Sorts schedule entries by start time and sweeps adjacent pairs once (O(n log n)) to find overlapping time windows. Returns a list of warning strings instead of raising, so a double-booking is surfaced without crashing the program. |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Tasks can carry a `recurrence` of `"daily"` or `"weekly"`. Completing a recurring task via `Pet.complete_task(title)` marks it done and automatically appends a fresh instance due one interval later (`due_date + timedelta(days=1)` or `timedelta(days=7)`). |



## 📸 Demo Walkthrough

### Main UI features

The Streamlit app (`app.py`) walks through four steps:

1. Owner Info — enter a name and how many minutes are available today; saving updates the owner in place, so pets/tasks you've already added aren't lost.
2. Add a Pet — enter name, species, and age; added pets appear in a running table with their task counts.
3. Add a Task — assign a task (title, duration, priority) to a pet, optionally with a preferred time and a recurrence (none/daily/weekly). Tasks appear in a table showing recurrence and completion status, and any pending task can be marked complete from a dropdown.
4. Generate Schedule — a "preview by preferred time" expander shows tasks ordered by Scheduler.sort_by_time(), and the "Generate schedule" button runs Scheduler.generate() to produce today's plan with reasoning for each entry, plus any conflict warnings from Scheduler.detect_conflicts().

### Example workflow

1. Save owner "Jordan" with 90 available minutes.
2. Add a pet, "Biscuit" (dog).
3. Add a task, "Morning walk" (30 min, high priority, daily recurrence, preferred time 7:00am).
4. Click "Generate schedule" to see the plan for today, along with the reasoning behind each placement.
5. Mark "Morning walk" complete — since it recurs daily, a fresh pending occurrence for tomorrow is queued automatically.

### Key Scheduler behaviors shown

- Priority-based scheduling: generate() sorts pending tasks by priority (high → medium → low) and greedily fits each into the remaining time budget, explaining why each task landed where it did.
- Time-based sorting: sort_by_time() orders tasks by preferred time of day, with untimed tasks sorted last — useful for previewing a day at a glance independent of priority.
- Conflict warnings: detect_conflicts() flags any two schedule entries with overlapping time windows (e.g., two pets' tasks double-booked at the same time) without ever raising an exception — warnings are surfaced for the owner to resolve.
- Recurring tasks: completing a "daily" or "weekly" task via complete_task() automatically queues its next occurrence, due one interval later.

### Sample CLI output (`python main.py`)

```
=================================================================
  Today's Schedule for Jordan
=================================================================
  #    TIME    PET          TASK                      DUR  PRIORITY
-----------------------------------------------------------------
  1.  08:00  |  Biscuit     |  Morning walk           30 min  [high]
       -> Priority is high; 90 min remaining, task takes 30 min.

  2.  08:30  |  Biscuit     |  Feeding                10 min  [high]
       -> Priority is high; 60 min remaining, task takes 10 min.

  3.  08:40  |  Mochi       |  Grooming               15 min  [medium]
       -> Priority is medium; 50 min remaining, task takes 15 min.

  4.  08:55  |  Mochi       |  Playtime               20 min  [low]
       -> Priority is low; 35 min remaining, task takes 20 min.

=================================================================

Tasks sorted by time:
  07:00  Morning walk
  07:30  Feeding
  09:00  Grooming
  09:00  Playtime

Biscuit's pending tasks:
  Biscuit: Morning walk
  Biscuit: Feeding

Completing 'Morning walk' (daily) for Biscuit...
  Morning walk    [done]  due=n/a  recurrence=daily
  Feeding         [pending]  due=n/a  recurrence=None
  Morning walk    [pending]  due=2026-07-09  recurrence=daily

Conflict detection demo:
  WARNING: Conflict: 'Vet visit' (Biscuit) runs 09:00-09:30, overlapping 'Grooming' (Mochi) starting at 09:00.
```
