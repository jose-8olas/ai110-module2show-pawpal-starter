
import json
from dataclasses import dataclass, field
from datetime import date, timedelta, datetime


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
    due_date: date = field(default_factory=date.today)

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
        self.preferences = (
            preferences if preferences is not None else {}
        )
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_id: str) -> None:
        """Remove a pet using its ID."""
        self.pets = [
            pet for pet in self.pets
            if pet.pet_id != pet_id
        ]

    def get_all_tasks(self) -> list[Task]:
        """Return tasks belonging to all of the owner's pets."""
        return [
            task
            for pet in self.pets
            for task in pet.get_tasks()
        ]

    def save_to_json(self, filename: str = "data.json") -> None:
        """Save owner, pets, and tasks to a JSON file."""

        data = {
            "owner_id": self.owner_id,
            "name": self.name,
            "preferences": self.preferences,
            "pets": []
        }

        for pet in self.pets:
            pet_data = {
                "pet_id": pet.pet_id,
                "name": pet.name,
                "species": pet.species,
                "tasks": []
            }

            for task in pet.tasks:
                task_data = {
                    "title": task.title,
                    "task_type": task.task_type,
                    "duration": task.duration,
                    "priority": task.priority,
                    "time": task.time,
                    "frequency": task.frequency,
                    "completed": task.completed,
                    "due_date": task.due_date.isoformat()
                }

                pet_data["tasks"].append(task_data)

            data["pets"].append(pet_data)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_from_json(self, filename: str = "data.json") -> None:
        """Load owner, pets, and tasks from a JSON file."""

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.owner_id = data["owner_id"]
        self.name = data["name"]
        self.preferences = data.get("preferences", {})
        self.pets = []

        for pet_data in data["pets"]:
            pet = Pet(
                pet_id=pet_data["pet_id"],
                name=pet_data["name"],
                species=pet_data["species"]
            )

            for task_data in pet_data["tasks"]:
                task = Task(
                    title=task_data["title"],
                    task_type=task_data["task_type"],
                    duration=task_data["duration"],
                    priority=task_data["priority"],
                    time=task_data["time"],
                    frequency=task_data["frequency"],
                    completed=task_data["completed"],
                    due_date=date.fromisoformat(task_data["due_date"])
                )

                pet.add_task(task)

            self.add_pet(pet)


class Scheduler:
    """Organize tasks into a daily care schedule."""

    def __init__(self, available_time: int) -> None:
        """Initialize the scheduler with a time budget."""
        self.available_time = available_time
        self.tasks: list[Task] = []

    def schedule_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        self.tasks.append(task)

    def get_tasks_from_owner(self, owner: Owner) -> list[Task]:
        """Retrieve tasks from all pets belonging to an owner."""
        self.tasks = owner.get_all_tasks()
        return self.tasks.copy()

    def sort_by_time(self) -> list[Task]:
        """Return tasks sorted by scheduled time."""
        return sorted(
            self.tasks,
            key=lambda task: task.time
        )

    def sort_by_priority(self) -> list[Task]:
        """Sort tasks by priority first, then by time."""
        priority_order = {
            "high": 1,
            "medium": 2,
            "low": 3
        }

        return sorted(
            self.tasks,
            key=lambda task: (
                priority_order.get(task.priority.lower(), 4),
                task.time
            )
        )

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Return tasks matching the requested completion status."""
        return [
            task for task in self.tasks
            if task.completed == completed
        ]

    def filter_by_pet(
        self, owner: Owner, pet_id: str
    ) -> list[Task]:
        """Return tasks belonging to a specific pet."""
        for pet in owner.pets:
            if pet.pet_id == pet_id:
                return pet.get_tasks()

        return []

    def complete_task(
        self, owner: Owner, task: Task
    ) -> Task | None:
        """Complete a task and create its next recurring occurrence."""

        pet_found = None

        # Find the pet that owns the task.
        for pet in owner.pets:
            if task in pet.tasks:
                pet_found = pet
                break

        # Make sure the task belongs to this owner.
        if pet_found is None:
            return None

        # Prevent duplicate recurring tasks.
        if task.completed:
            return None

        # Mark the original task as completed.
        task.mark_completed()

        # Calculate the next occurrence.
        if task.frequency.lower() == "daily":
            next_date = task.due_date + timedelta(days=1)

        elif task.frequency.lower() == "weekly":
            next_date = task.due_date + timedelta(days=7)

        else:
            return None

        # Create a separate task with the original details.
        next_task = Task(
            title=task.title,
            task_type=task.task_type,
            duration=task.duration,
            priority=task.priority,
            time=task.time,
            frequency=task.frequency,
            completed=False,
            due_date=next_date
        )

        # Add the new task to the pet and scheduler.
        pet_found.add_task(next_task)
        self.tasks.append(next_task)

        return next_task

    def detect_conflicts(self) -> list[Task]:
        """Return tasks exceeding the available time budget."""
        conflicts = []
        total_duration = 0

        for task in self.sort_by_time():
            total_duration += task.duration

            if total_duration > self.available_time:
                conflicts.append(task)

        return conflicts

    def detect_time_conflicts(self) -> list[str]:
        """Return warnings for incomplete tasks scheduled at the same time."""
        warnings = []
        seen_times = {}

        for task in self.tasks:
            if task.completed:
                continue

            key = (task.due_date, task.time)

            if key in seen_times:
                other_task = seen_times[key]

                warnings.append(
                    f"Conflict: '{other_task.title}' and "
                    f"'{task.title}' are both scheduled for "
                    f"{task.time} on {task.due_date}."
                )
            else:
                seen_times[key] = task

        return warnings

    def generate_daily_plan(self) -> list[Task]:
        """Generate a daily plan sorted by priority and time."""
        return [
            task for task in self.sort_by_priority()
            if not task.completed
        ]

    def find_next_available_slot(
        self,
        requested_date: date,
        start_time: str,
        duration: int
    ) -> str | None:
        """Find the earliest available time slot for a task."""

        if duration <= 0:
            raise ValueError("Duration must be greater than zero.")

        current_time = datetime.strptime(
            start_time, "%H:%M"
        )

        daily_tasks = sorted(
            [
                task for task in self.tasks
                if task.due_date == requested_date
                and not task.completed
            ],
            key=lambda task: task.time
        )

        for task in daily_tasks:
            task_start = datetime.strptime(
                task.time, "%H:%M"
            )

            task_end = task_start + timedelta(
                minutes=task.duration
            )

            requested_end = current_time + timedelta(
                minutes=duration
            )

            if current_time < task_end and requested_end > task_start:
                current_time = task_end

        if current_time + timedelta(minutes=duration) > datetime.strptime(
            "23:59", "%H:%M"
        ):
            return None

        return current_time.strftime("%H:%M")
