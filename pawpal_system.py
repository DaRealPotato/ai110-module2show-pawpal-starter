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


class Availability:
    def __init__(self, start_hour: int, end_hour: int):
        self.start_hour = start_hour
        self.end_hour = end_hour

    def get_total_minutes(self) -> int:
        pass


class Schedule:
    def __init__(self):
        self.entries: list[dict] = []

    def add_entry(self, task: Task, start_time: int) -> None:
        pass

    def display(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pet: Pet = None
        self.availability: Availability = None

    def add_task(self, task: Task) -> None:
        pass

    def get_schedule(self) -> Schedule:
        pass


class Scheduler:
    def generate(self, owner: Owner, tasks: list[Task]) -> Schedule:
        pass
