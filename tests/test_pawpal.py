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


def test_find_next_available_slot():
    scheduler = Scheduler(available_time=480)

    today = date(2026, 10, 29)

    scheduler.schedule_task(
        Task(
            "Morning Walk", "Exercise", 30, "High", "08:00",
            due_date=today
        )
    )

    scheduler.schedule_task(
        Task(
            "Feeding", "Feeding", 15, "Medium", "09:00",
            due_date=today
        )
    )

    scheduler.schedule_task(
        Task(
            "Grooming", "Grooming", 30, "Low", "10:00",
            due_date=today
        )
    )

    available_slot = scheduler.find_next_available_slot(
        requested_date=today,
        start_time="08:00",
        duration=20
    )

    assert available_slot == "08:30"

def test_find_next_available_slot_multiple_conflicts():
    scheduler = Scheduler(available_time=480)

    today = date(2026, 10, 29)

    scheduler.schedule_task(
        Task("Morning Walk", "Exercise", 30, "High", "08:00",
             due_date=today)
    )

    scheduler.schedule_task(
        Task("Feeding", "Feeding", 15, "Medium", "08:30",
             due_date=today)
    )

    scheduler.schedule_task(
        Task("Grooming", "Grooming", 30, "Low", "08:45",
             due_date=today)
    )

    available_slot = scheduler.find_next_available_slot(
        requested_date=today,
        start_time="08:00",
        duration=20
    )

    assert available_slot == "09:15"


    
def test_sort_by_priority_then_time():
    scheduler = Scheduler(available_time=480)

    scheduler.schedule_task(
        Task("Grooming", "Grooming", 30, "Low", "08:00")
    )

    scheduler.schedule_task(
        Task("Feeding", "Feeding", 15, "Medium", "07:00")
    )

    scheduler.schedule_task(
        Task("Medication", "Medication", 10, "High", "10:00")
    )

    scheduler.schedule_task(
        Task("Morning Walk", "Exercise", 30, "High", "08:00")
    )

    result = scheduler.sort_by_priority()

    assert [task.title for task in result] == [
        "Morning Walk",
        "Medication",
        "Feeding",
        "Grooming"
    ]


def test_weekly_recurring_task():
    owner = Owner("O001", "Alex")
    pet = Pet("P001", "Buddy", "Dog")
    owner.add_pet(pet)

    original_date = date(2026, 10, 30)

    task = Task(
        "Weekly bath", "Grooming", 30, "Medium", "09:00",
        frequency="weekly",
        due_date=original_date
    )

    pet.add_task(task)

    scheduler = Scheduler(60)
    scheduler.get_tasks_from_owner(owner)

    next_task = scheduler.complete_task(owner, task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == original_date + timedelta(days=7)
    assert next_task.completed is False


def test_completed_task_cannot_be_completed_twice():
    owner = Owner("O001", "Alex")
    pet = Pet("P001", "Buddy", "Dog")
    owner.add_pet(pet)

    task = Task(
        "Weekly bath", "Grooming", 30, "Medium", "09:00",
        frequency="weekly",
        due_date=date(2026, 10, 30)
    )

    pet.add_task(task)

    scheduler = Scheduler(60)
    scheduler.get_tasks_from_owner(owner)

    next_task = scheduler.complete_task(owner, task)

    assert next_task is not None

    original_task_count = len(pet.tasks)

    second_attempt = scheduler.complete_task(owner, task)

    assert second_attempt is None
    assert len(pet.tasks) == original_task_count


def test_as_needed_task_does_not_reschedule():
    owner = Owner("O001", "Alex")
    pet = Pet("P001", "Buddy", "Dog")
    owner.add_pet(pet)

    task = Task(
        "Extra grooming", "Grooming", 20, "Low", "10:00",
        frequency="as needed",
        due_date=date(2026, 10, 30)
    )

    pet.add_task(task)

    scheduler = Scheduler(60)
    scheduler.get_tasks_from_owner(owner)

    next_task = scheduler.complete_task(owner, task)

    assert task.completed is True
    assert next_task is None
    assert len(pet.tasks) == 1


def test_recurring_task_preserves_original_details():
    owner = Owner("O001", "Alex")
    pet = Pet("P001", "Buddy", "Dog")
    owner.add_pet(pet)

    task = Task(
        "Weekly bath", "Grooming", 30, "Medium", "09:00",
        frequency="weekly",
        due_date=date(2026, 10, 30)
    )

    pet.add_task(task)

    scheduler = Scheduler(60)
    scheduler.get_tasks_from_owner(owner)

    next_task = scheduler.complete_task(owner, task)

    assert next_task.title == task.title
    assert next_task.task_type == task.task_type
    assert next_task.duration == task.duration
    assert next_task.priority == task.priority
    assert next_task.time == task.time
    assert next_task.frequency == task.frequency
