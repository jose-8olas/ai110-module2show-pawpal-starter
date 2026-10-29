
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    """Create pet-care tasks and display the daily schedule."""
    owner = Owner(
        owner_id="O001",
        name="Alex",
        preferences={"preferred_start": "08:00"}
    )

    buddy = Pet(pet_id="P001", name="Buddy", species="Dog")
    whiskers = Pet(pet_id="P002", name="Whiskers", species="Cat")

    buddy.add_task(Task(
        title="Morning walk",
        task_type="Exercise",
        duration=30,
        priority="High",
        time="08:00",
        frequency="daily"
    ))

    buddy.add_task(Task(
        title="Breakfast",
        task_type="Feeding",
        duration=10,
        priority="High",
        time="08:30",
        frequency="daily"
    ))

    whiskers.add_task(Task(
        title="Feed cat",
        task_type="Feeding",
        duration=10,
        priority="High",
        time="09:00",
        frequency="daily"
    ))

    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    scheduler = Scheduler(available_time=60)
    scheduler.get_tasks_from_owner(owner)
    daily_plan = scheduler.generate_daily_plan()

    print("Today's Schedule")
    print("================")

    for task in daily_plan:
        print(
            f"{task.time} | {task.title} | "
            f"{task.task_type} | {task.duration} min | "
            f"Priority: {task.priority} | "
            f"Frequency: {task.frequency}"
        )

    conflicts = scheduler.detect_conflicts()

    if conflicts:
        print("\nTasks exceeding the available time budget:")
        for task in conflicts:
            print(f"- {task.title}")
    else:
        print("\nAll tasks fit within the available time budget.")


if __name__ == "__main__":
    main()
