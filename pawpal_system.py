from dataclasses import dataclass, field


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    is_recurring: bool = False
    completed: bool = False

    def fits_in(self, minutes_remaining: int) -> bool:
        """Return True if this task's duration fits within the remaining time."""
        return self.duration_minutes <= minutes_remaining

    def mark_complete(self) -> None:
        """Mark this task as completed so the scheduler skips it."""
        self.completed = True


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


@dataclass
class ScheduleEntry:
    task: Task
    start_time: int  # minutes from midnight, e.g. 480 = 8:00am
    pet_name: str = ""
    reasoning: str = ""

    def start_time_str(self) -> str:
        """Convert start_time in minutes to a HH:MM string."""
        hours = self.start_time // 60
        minutes = self.start_time % 60
        return f"{hours:02d}:{minutes:02d}"


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


class Scheduler:
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
