
from dataclasses import dataclass, field


@dataclass
class Task:
    """Represent a pet-care activity."""
    title: str
    task_type: str
    duration: int
    priority: str
    time: str
    frequency: str = "daily"
    completed: bool = False

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    """Store pet details and assigned care tasks."""
    pet_id: str
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return this pet's care tasks."""
        return self.tasks.copy()


class Owner:
    """Manage an owner's pets and their care tasks."""

    def __init__(
        self,
        owner_id: str,
        name: str,
        preferences: dict | None = None
    ) -> None:
        """Initialize the owner and their preferences."""
        self.owner_id = owner_id
        self.name = name
        self.preferences = preferences if preferences is not None else {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet using its ID."""
        self.pets = [
            pet for pet in self.pets if pet.pet_id != pet_id
        ]

    def get_all_tasks(self) -> list[Task]:
        """Return tasks belonging to all of the owner's pets."""
        return [
            task
            for pet in self.pets
            for task in pet.get_tasks()
        ]


class Scheduler:
    """Organize tasks into a daily care schedule."""

    def __init__(self, available_time: int) -> None:
        """Initialize the scheduler with an available time budget."""
        self.available_time = available_time
        self.tasks: list[Task] = []

    def schedule_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        self.tasks.append(task)

    def get_tasks_from_owner(self, owner: Owner) -> list[Task]:
        """Retrieve tasks from all pets belonging to an owner."""
        self.tasks = owner.get_all_tasks()
        return self.tasks.copy()

    def sort_tasks(self) -> list[Task]:
        """Sort tasks by time."""
        return sorted(self.tasks, key=lambda task: task.time)

    def detect_conflicts(self) -> list[Task]:
        """Return tasks that exceed the available time budget."""
        conflicts = []
        total_duration = 0

        for task in self.sort_tasks():
            total_duration += task.duration
            if total_duration > self.available_time:
                conflicts.append(task)

        return conflicts

    def generate_daily_plan(self) -> list[Task]:
        """Generate a time-ordered daily care plan."""
        return [
            task for task in self.sort_tasks()
            if not task.completed
        ]
