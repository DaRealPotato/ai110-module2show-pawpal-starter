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
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts tasks by their preferred `time` (minutes from midnight); tasks with no preferred time sort last. The main daily plan itself (`Scheduler.generate()`) sorts by `priority` first (high → medium → low), then fits each task into whatever time remains. |
| Filtering | `Owner.filter_tasks(completed=, pet_name=)` | Returns `(task, pet_name)` pairs filtered by completion status, pet name, or both — e.g. "show me Biscuit's pending tasks." |
| Conflict handling | `Scheduler.detect_conflicts()` | Sorts schedule entries by start time and sweeps adjacent pairs once (O(n log n)) to find overlapping time windows. Returns a list of warning strings instead of raising, so a double-booking is surfaced without crashing the program. |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Tasks can carry a `recurrence` of `"daily"` or `"weekly"`. Completing a recurring task via `Pet.complete_task(title)` marks it done and automatically appends a fresh instance due one interval later (`due_date + timedelta(days=1)` or `timedelta(days=7)`). |



## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
