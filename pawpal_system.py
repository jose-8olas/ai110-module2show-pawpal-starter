from dataclasses import dataclass, field


@dataclass
class Task:
    """Represents one pet-care activity."""
    title: str
    task_type: str
    duration: int
    priority: str
    completed: bool = False

    def mark_completed(self) -> None:
        pass


@dataclass
class Pet:
    """Stores information about a pet and its care tasks."""
    pet_id: str
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Owner:
    """Stores owner information and manages pets."""

    def __init__(self, owner_id: str, name: str) -> None:
        self.owner_id = owner_id
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet_id: str) -> None:
        pass


class Scheduler:
    """Manages care tasks and prepares a daily plan."""

    def __init__(self, available_time: int) -> None:
        self.tasks: list[Task] = []
        self.available_time = available_time

    def schedule_task(self, task: Task) -> None:
        pass

    def sort_tasks(self) -> None:
        pass

    def detect_conflicts(self) -> None:
        pass

    def generate_daily_plan(self) -> None:
        pass