
from datetime import date

from pawpal_system import Owner, Pet, Task


def test_save_and_load_json(tmp_path):
    filename = tmp_path / "data.json"

    owner = Owner("O001", "Alex")
    pet = Pet("P001", "Buddy", "Dog")

    task = Task(
        title="Morning Walk",
        task_type="Exercise",
        duration=30,
        priority="High",
        time="08:00",
        frequency="daily",
        completed=False,
        due_date=date(2026, 10, 30)
    )

    pet.add_task(task)
    owner.add_pet(pet)

    owner.save_to_json(str(filename))

    loaded_owner = Owner("O002", "Temporary")
    loaded_owner.load_from_json(str(filename))

    assert loaded_owner.owner_id == "O001"
    assert loaded_owner.name == "Alex"
    assert len(loaded_owner.pets) == 1
    assert loaded_owner.pets[0].name == "Buddy"
    assert loaded_owner.pets[0].tasks[0].title == "Morning Walk"
    assert loaded_owner.pets[0].tasks[0].due_date == date(2026, 10, 30)
    assert loaded_owner.pets[0].tasks[0].priority == "High"
