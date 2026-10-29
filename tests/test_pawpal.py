from datetime import date, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


def test_task_completion():
    task = Task(
        title="Feed dog",
        task_type="Feeding",
        duration=10,
        priority="High",
        time="08:00"
    )

    task.mark_completed()

    assert task.completed is True


def test_adding_task_to_pet():
    pet = Pet(
        pet_id="P001",
        name="Buddy",
        species="Dog"
    )

    task = Task(
        title="Morning walk",
        task_type="Exercise",
        duration=30,
        priority="High",
        time="08:00"
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] == task


def test_sort_by_time():
    scheduler = Scheduler(60)

    late_task = Task(
        "Evening walk", "Exercise", 20, "High", "18:00"
    )
    early_task = Task(
        "Breakfast", "Feeding", 10, "High", "08:00"
    )

    scheduler.schedule_task(late_task)
    scheduler.schedule_task(early_task)

    result = scheduler.sort_by_time()

    assert [task.time for task in result] == ["08:00", "18:00"]


def test_daily_recurring_task():
    owner = Owner("O001", "Alex")
    pet = Pet("P001", "Buddy", "Dog")
    owner.add_pet(pet)

    original_date = date(2026, 10, 29)

    task = Task(
        "Feed dog", "Feeding", 10, "High", "08:00",
        frequency="daily",
        due_date=original_date
    )
    pet.add_task(task)

    scheduler = Scheduler(60)
    scheduler.get_tasks_from_owner(owner)

    next_task = scheduler.complete_task(owner, task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == original_date + timedelta(days=1)
    assert next_task.completed is False


def test_same_time_conflict_detection():
    scheduler = Scheduler(60)
    today = date(2026, 10, 29)

    task1 = Task(
        "Feed dog", "Feeding", 10, "High", "08:00",
        due_date=today
    )
    task2 = Task(
        "Give medication", "Medication", 5, "High", "08:00",
        due_date=today
    )

    scheduler.schedule_task(task1)
    scheduler.schedule_task(task2)

    warnings = scheduler.detect_time_conflicts()

    assert len(warnings) == 1
    assert "Feed dog" in warnings[0]
    assert "Give medication" in warnings[0]
