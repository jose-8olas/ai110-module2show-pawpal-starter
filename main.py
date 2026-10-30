
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date


def main():
    """Create pet-care tasks and test scheduling features."""

    owner = Owner(
        owner_id="O001",
        name="Alex",
        preferences={"preferred_start": "08:00"}
    )

    buddy = Pet(pet_id="P001", name="Buddy", species="Dog")
    whiskers = Pet(pet_id="P002", name="Whiskers", species="Cat")

    # Add tasks in a deliberately unsorted order.
    buddy.add_task(Task(
        title="Morning walk",
        task_type="Exercise",
        duration=30,
        priority="High",
        time="08:00",
        frequency="daily"
    ))

    whiskers.add_task(Task(
        title="Feed cat",
        task_type="Feeding",
        duration=10,
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

    # Add a weekly recurring task.
    buddy.add_task(Task(
        title="Weekly bath",
        task_type="Grooming",
        duration=30,
        priority="Medium",
        time="09:00",
        frequency="weekly",
        due_date=date(2026, 10, 30)
    ))

    owner.add_pet(buddy)
    owner.add_pet(whiskers)

    scheduler = Scheduler(available_time=60)
    scheduler.get_tasks_from_owner(owner)

    # Test sorting.
    print("\nTasks sorted by time:")
    for task in scheduler.sort_by_time():
        print(f"{task.time} | {task.title}")

    # Test filtering by completion status.
    print("\nIncomplete tasks:")
    for task in scheduler.filter_by_status(False):
        print(f"{task.time} | {task.title}")

    print("\nCompleted tasks:")
    completed_tasks = scheduler.filter_by_status(True)

    if completed_tasks:
        for task in completed_tasks:
            print(f"{task.time} | {task.title}")
    else:
        print("No completed tasks.")

    # Test filtering by pet.
    print("\nBuddy's tasks:")
    for task in scheduler.filter_by_pet(owner, "P001"):
        print(f"{task.time} | {task.title}")

    # Display the daily schedule.
    daily_plan = scheduler.generate_daily_plan()

    print("\nToday's Schedule")
    print("================")

    for task in daily_plan:
        print(
            f"{task.time} | {task.title} | "
            f"{task.task_type} | {task.duration} min | "
            f"Priority: {task.priority} | "
            f"Frequency: {task.frequency}"
        )

    # Check the available time budget.
    conflicts = scheduler.detect_conflicts()

    if conflicts:
        print("\nTasks exceeding the available time budget:")
        for task in conflicts:
            print(f"- {task.title}")
    else:
        print("\nAll tasks fit within the available time budget.")

    # Check for tasks scheduled at the same time.
    print("\nSame-Time Conflict Check")
    print("========================")

    time_conflicts = scheduler.detect_time_conflicts()

    if time_conflicts:
        for warning in time_conflicts:
            print(f"WARNING: {warning}")
    else:
        print("No same-time conflicts detected.")

    # Test weekly recurring tasks.
    print("\nWeekly Recurring Task Test")
    print("==========================")

    weekly_task = buddy.tasks[-1]

    next_task = scheduler.complete_task(owner, weekly_task)

    if next_task is not None:
        print(f"Completed: {weekly_task.title}")
        print(f"Original date: {weekly_task.due_date}")
        print(f"Next occurrence: {next_task.due_date}")
        print(f"Frequency: {next_task.frequency}")
        print(f"New task completed: {next_task.completed}")

        print("\nVerifying original and new tasks:")
        print(f"Original completed: {weekly_task.completed}")
        print(f"Original still exists: {weekly_task in buddy.tasks}")
        print(f"New task exists: {next_task in buddy.tasks}")

    else:
        print("Task could not be completed or has no recurrence.")


if __name__ == "__main__":
    main()
