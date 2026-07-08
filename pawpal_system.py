from dataclasses import dataclass, field, replace
from datetime import date, timedelta


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

RECURRENCE_INTERVALS = {"daily": timedelta(days=1), "weekly": timedelta(days=7)}


def _format_time(minutes_from_midnight: int) -> str:
    """Convert minutes from midnight to a HH:MM string."""
    hours, minutes = divmod(minutes_from_midnight, 60)
    return f"{hours:02d}:{minutes:02d}"


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    time: int | None = None  # preferred start time in minutes from midnight
    recurrence: str | None = None  # "daily", "weekly", or None
    due_date: date | None = None
    completed: bool = False

    def fits_in(self, minutes_remaining: int) -> bool:
        """Return True if this task's duration fits within the remaining time."""
        return self.duration_minutes <= minutes_remaining

    def mark_complete(self) -> None:
        """Mark this task as completed so the scheduler skips it."""
        self.completed = True

    def next_occurrence(self) -> "Task | None":
        """Compute the next instance of a recurring task.

        Returns:
            A new, incomplete Task due one interval (RECURRENCE_INTERVALS["daily"]
            or ["weekly"]) after this task's due_date (or after today, if unset),
            or None if this task has no recurrence set.
        """
        interval = RECURRENCE_INTERVALS.get(self.recurrence)
        if interval is None:
            return None
        base_date = self.due_date or date.today()
        return replace(self, due_date=base_date + interval, completed=False)


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a new task to this pet's task list."""
        self.tasks.append(task)

    def edit_task(self, title: str, updated_task: Task) -> None:
        """Replace the task matching the given title with updated_task."""
        for i, task in enumerate(self.tasks):
            if task.title == title:
                self.tasks[i] = updated_task
                return

    def complete_task(self, title: str) -> None:
        """Mark the named task complete and, if it recurs, queue up its next occurrence.

        Args:
            title: The title of the task to complete. Matches the first
                pending (not-yet-completed) task with this title.
        """
        for task in self.tasks:
            if task.title == title and not task.completed:
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task is not None:
                    self.tasks.append(next_task)
                return


@dataclass
class ScheduleEntry:
    task: Task
    start_time: int  # minutes from midnight, e.g. 480 = 8:00am
    pet_name: str = ""
    reasoning: str = ""

    def start_time_str(self) -> str:
        """Convert start_time in minutes to a HH:MM string."""
        return _format_time(self.start_time)


class Schedule:
    def __init__(self):
        self.entries: list[ScheduleEntry] = []

    def add_entry(self, task: Task, start_time: int, pet_name: str = "", reasoning: str = "") -> None:
        """Add a scheduled task entry with its start time, pet name, and reasoning."""
        self.entries.append(ScheduleEntry(task=task, start_time=start_time, pet_name=pet_name, reasoning=reasoning))

    def display(self) -> str:
        """Format and return the full schedule as a readable string."""
        if not self.entries:
            return "No tasks scheduled."
        lines = []
        for i, entry in enumerate(self.entries, start=1):
            lines.append(
                f"  {i}.  {entry.start_time_str()}  |  {entry.pet_name:<10}  |  "
                f"{entry.task.title:<20}  {entry.task.duration_minutes:>3} min  [{entry.task.priority}]"
            )
            lines.append(f"       -> {entry.reasoning}")
            lines.append("")
        return "\n".join(lines)


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of all tasks across every pet this owner has."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def get_schedule(self) -> Schedule:
        """Generate and return today's schedule for this owner's pets."""
        return Scheduler().generate(self)

    def filter_tasks(self, completed: bool | None = None, pet_name: str | None = None) -> list[tuple[Task, str]]:
        """Filter this owner's tasks by completion status and/or pet name.

        Args:
            completed: If set, only include tasks whose completed flag matches.
                Leave as None to include tasks regardless of status.
            pet_name: If set, only include tasks belonging to the pet with this name.
                Leave as None to include tasks from every pet.

        Returns:
            A list of (task, pet_name) pairs matching all given filters.
        """
        results = []
        for pet in self.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                results.append((task, pet.name))
        return results


class Scheduler:
    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by their preferred time of day.

        Args:
            tasks: Tasks to sort. Tasks may or may not have a preferred `time` set.

        Returns:
            A new list ordered by ascending `time` (minutes from midnight);
            tasks with no preferred time (time is None) are placed last.
        """
        return sorted(tasks, key=lambda t: (t.time is None, t.time if t.time is not None else 0))

    def detect_conflicts(self, schedule: Schedule) -> list[str]:
        """Lightweight overlap check: flag any two entries whose time windows intersect.

        Sorts entries by start time and sweeps adjacent pairs once (O(n log n)),
        rather than comparing every pair of entries (O(n^2)). Returns human-readable
        warning strings instead of raising, so a conflict never crashes the
        program -- it's surfaced to the caller to print or log as needed.

        Args:
            schedule: The Schedule whose entries should be checked for overlaps.

        Returns:
            A list of warning messages, one per overlapping pair of entries found.
            Empty if no conflicts exist.
        """
        warnings = []
        sorted_entries = sorted(schedule.entries, key=lambda e: e.start_time)
        for current, nxt in zip(sorted_entries, sorted_entries[1:]):
            current_end = current.start_time + current.task.duration_minutes
            if current_end > nxt.start_time:
                warnings.append(
                    f"Conflict: '{current.task.title}' ({current.pet_name}) runs "
                    f"{current.start_time_str()}-{_format_time(current_end)}, "
                    f"overlapping '{nxt.task.title}' ({nxt.pet_name}) starting at {nxt.start_time_str()}."
                )
        return warnings

    def generate(self, owner: Owner) -> Schedule:
        """Build a Schedule by sorting pending tasks by priority and fitting them into available time."""
        pending = [
            (task, pet.name)
            for pet in owner.pets
            for task in pet.tasks
            if not task.completed
        ]
        sorted_pairs = sorted(pending, key=lambda pair: PRIORITY_ORDER.get(pair[0].priority, 99))

        schedule = Schedule()
        minutes_remaining = owner.available_minutes
        current_time = 8 * 60  # start at 8:00am

        for task, pet_name in sorted_pairs:
            if task.fits_in(minutes_remaining):
                reasoning = (
                    f"Priority is {task.priority}; "
                    f"{minutes_remaining} min remaining, task takes {task.duration_minutes} min."
                )
                schedule.add_entry(task, current_time, pet_name, reasoning)
                current_time += task.duration_minutes
                minutes_remaining -= task.duration_minutes

        return schedule
