from datetime import date

from pawpal_system import Task, Pet, Schedule, Scheduler


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    assert len(pet.tasks) == 1


# --- Sorting correctness (Scheduler.sort_by_time) ---


def test_sort_by_time_happy_path_orders_chronologically():
    morning = Task(title="Breakfast", duration_minutes=10, priority="high", time=480)  # 8:00
    midday = Task(title="Walk", duration_minutes=20, priority="medium", time=720)  # 12:00
    evening = Task(title="Dinner", duration_minutes=15, priority="high", time=1080)  # 18:00

    result = Scheduler().sort_by_time([evening, morning, midday])

    assert [t.title for t in result] == ["Breakfast", "Walk", "Dinner"]


def test_sort_by_time_pushes_untimed_tasks_to_end():
    timed = Task(title="Walk", duration_minutes=20, priority="medium", time=480)
    untimed = Task(title="Grooming", duration_minutes=30, priority="low", time=None)

    result = Scheduler().sort_by_time([untimed, timed])

    assert [t.title for t in result] == ["Walk", "Grooming"]


def test_sort_by_time_preserves_order_for_equal_times():
    first = Task(title="Feeding", duration_minutes=10, priority="high", time=480)
    second = Task(title="Meds", duration_minutes=5, priority="high", time=480)

    result = Scheduler().sort_by_time([first, second])

    assert [t.title for t in result] == ["Feeding", "Meds"]


def test_sort_by_time_all_untimed_keeps_original_order():
    a = Task(title="A", duration_minutes=10, priority="low", time=None)
    b = Task(title="B", duration_minutes=10, priority="low", time=None)

    result = Scheduler().sort_by_time([a, b])

    assert [t.title for t in result] == ["A", "B"]


# --- Recurrence logic (Pet.complete_task / Task.next_occurrence) ---


def test_complete_daily_task_creates_next_day_occurrence():
    pet = Pet(name="Biscuit", species="dog", age=3)
    pet.add_task(Task(
        title="Walk", duration_minutes=20, priority="high",
        recurrence="daily", due_date=date(2026, 7, 8),
    ))

    pet.complete_task("Walk")

    assert len(pet.tasks) == 2
    original, next_task = pet.tasks
    assert original.completed is True
    assert next_task.completed is False
    assert next_task.due_date == date(2026, 7, 9)


def test_complete_weekly_task_creates_occurrence_seven_days_later():
    pet = Pet(name="Biscuit", species="dog", age=3)
    pet.add_task(Task(
        title="Grooming", duration_minutes=45, priority="medium",
        recurrence="weekly", due_date=date(2026, 7, 8),
    ))

    pet.complete_task("Grooming")

    next_task = pet.tasks[1]
    assert next_task.due_date == date(2026, 7, 15)


def test_complete_non_recurring_task_does_not_create_occurrence():
    pet = Pet(name="Biscuit", species="dog", age=3)
    pet.add_task(Task(title="Vet visit", duration_minutes=60, priority="high"))

    pet.complete_task("Vet visit")

    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed is True


def test_complete_task_only_affects_first_pending_match_with_duplicate_titles():
    pet = Pet(name="Biscuit", species="dog", age=3)
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))

    pet.complete_task("Feeding")

    completed_flags = [t.completed for t in pet.tasks]
    assert completed_flags == [True, False]


def test_complete_task_with_unknown_title_is_a_noop():
    pet = Pet(name="Biscuit", species="dog", age=3)
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))

    pet.complete_task("Nonexistent")

    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed is False


# --- Conflict detection (Scheduler.detect_conflicts) ---


def test_detect_conflicts_flags_overlapping_entries():
    schedule = Schedule()
    schedule.add_entry(
        Task(title="Walk", duration_minutes=30, priority="high"), start_time=540, pet_name="Biscuit",
    )
    schedule.add_entry(
        Task(title="Feeding", duration_minutes=15, priority="medium"), start_time=550, pet_name="Mochi",
    )

    warnings = Scheduler().detect_conflicts(schedule)

    assert len(warnings) == 1
    assert "Walk" in warnings[0] and "Feeding" in warnings[0]


def test_detect_conflicts_ignores_back_to_back_entries():
    schedule = Schedule()
    schedule.add_entry(
        Task(title="Walk", duration_minutes=30, priority="high"), start_time=540, pet_name="Biscuit",
    )
    schedule.add_entry(
        Task(title="Feeding", duration_minutes=15, priority="medium"), start_time=570, pet_name="Mochi",
    )

    warnings = Scheduler().detect_conflicts(schedule)

    assert warnings == []


def test_detect_conflicts_no_overlap_returns_empty():
    schedule = Schedule()
    schedule.add_entry(
        Task(title="Walk", duration_minutes=30, priority="high"), start_time=540, pet_name="Biscuit",
    )
    schedule.add_entry(
        Task(title="Feeding", duration_minutes=15, priority="medium"), start_time=700, pet_name="Mochi",
    )

    warnings = Scheduler().detect_conflicts(schedule)

    assert warnings == []


def test_detect_conflicts_empty_schedule_returns_empty():
    warnings = Scheduler().detect_conflicts(Schedule())

    assert warnings == []
