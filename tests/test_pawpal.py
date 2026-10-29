
from pawpal_system import Pet, Task


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
