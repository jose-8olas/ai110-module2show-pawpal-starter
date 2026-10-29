
import streamlit as st
from datetime import time

from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="centered"
)

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This app helps pet owners organize daily care tasks and
generate a schedule using the PawPal+ backend classes.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

The app connects the Streamlit interface to the Owner, Pet, Task,
and Scheduler classes.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, the system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan and when each task happens
"""
    )

st.divider()


# Initialize the Owner once per session.
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(
        owner_id="O001",
        name="Jordan",
        preferences={"preferred_start": "08:00"}
    )

owner = st.session_state["owner"]


# Keep the original quick demo inputs.
st.subheader("Quick Demo Inputs")

owner.name = st.text_input(
    "Owner name",
    value=owner.name,
    key="owner_name"
)

pet_name = st.text_input(
    "Pet name",
    value="Mochi",
    key="pet_name"
)

species = st.selectbox(
    "Species",
    ["dog", "cat", "other"],
    key="species"
)

if st.button("Add pet"):
    if pet_name.strip():
        pet = Pet(
            pet_id=f"P{len(owner.pets) + 1:03d}",
            name=pet_name.strip(),
            species=species
        )

        owner.add_pet(pet)
        st.success(f"{pet.name} was added!")
    else:
        st.error("Please enter a pet name.")


# Display pets stored in the Owner object.
if owner.pets:
    st.write("Current pets:")
    for pet in owner.pets:
        st.write(f"🐾 {pet.name} — {pet.species.title()}")
else:
    st.info("No pets yet. Add one above.")


st.markdown("### Tasks")
st.caption(
    "Add a few tasks. Tasks are stored in the backend and associated "
    "with the selected pet."
)

if owner.pets:
    selected_pet_id = st.selectbox(
        "Choose a pet for this task",
        options=[pet.pet_id for pet in owner.pets],
        format_func=lambda pet_id: next(
            pet.name for pet in owner.pets
            if pet.pet_id == pet_id
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        task_title = st.text_input(
            "Task title",
            value="Morning walk"
        )

    with col2:
        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=20
        )

    with col3:
        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            index=2
        )

    task_type = st.selectbox(
        "Task type",
        ["Feeding", "Exercise", "Grooming", "Medication", "Other"]
    )

    task_time = st.time_input(
        "Task time",
        value=time(8, 0)
    )

    frequency = st.selectbox(
        "Frequency",
        ["daily", "weekly", "as needed"]
    )

    if st.button("Add task"):
        if task_title.strip():
            selected_pet = next(
                pet for pet in owner.pets
                if pet.pet_id == selected_pet_id
            )

            task = Task(
                title=task_title.strip(),
                task_type=task_type,
                duration=int(duration),
                priority=priority,
                time=task_time.strftime("%H:%M"),
                frequency=frequency
            )

            selected_pet.add_task(task)
            st.success(
                f"Added '{task.title}' to {selected_pet.name}."
            )
        else:
            st.error("Please enter a task title.")
else:
    st.info("Add a pet before adding tasks.")


# Keep the original table approach: dictionaries are used for display.
task_rows = []

for pet in owner.pets:
    for task in pet.get_tasks():
        task_rows.append({
            "Pet": pet.name,
            "title": task.title,
            "duration_minutes": task.duration,
            "priority": task.priority,
            "time": task.time,
            "type": task.task_type,
            "frequency": task.frequency,
            "completed": task.completed
        })

if task_rows:
    st.write("Current tasks:")
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")


st.divider()

st.subheader("Build Schedule")
st.caption(
    "Generate a daily schedule using your Scheduler class."
)

available_time = st.number_input(
    "Available time (minutes)",
    min_value=1,
    max_value=1440,
    value=60
)

if st.button("Generate schedule"):
    scheduler = Scheduler(available_time=int(available_time))
    scheduler.get_tasks_from_owner(owner)

    daily_plan = scheduler.generate_daily_plan()

    if daily_plan:
        st.markdown("### Today's Schedule")

        for task in daily_plan:
            st.write(
                f"**{task.time}** — {task.title} "
                f"({task.duration} min, {task.priority} priority)"
            )
    else:
        st.info("There are no incomplete tasks to schedule.")

    conflicts = scheduler.detect_conflicts()

    if conflicts:
        st.warning("Some tasks exceed the available time budget.")
        for task in conflicts:
            st.write(f"- {task.title}")
    else:
        st.success(
            "All tasks fit within the available time budget."
        )
