from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    is_recurring: bool = False

    def fits_in(self, minutes_remaining: int) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def edit_task(self, title: str, updated_task: Task) -> None:
        pass


@dataclass
class ScheduleEntry:
    task: Task
    start_time: int   # minutes from start of day, e.g. 480 = 8:00am
    reasoning: str = ""


class Schedule:
    def __init__(self):
        self.entries: list[ScheduleEntry] = []

    def add_entry(self, task: Task, start_time: int, reasoning: str = "") -> None:
        pass

    def display(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pet: Pet = None

    def get_schedule(self) -> Schedule:
        return Scheduler().generate(self)


class Scheduler:
    def generate(self, owner: Owner) -> Schedule:
        pass
