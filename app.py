
import streamlit as st
from datetime import date, time

from pawpal_system import Owner, Pet, Task, Scheduler


# Formatting helper functions
def format_task_type(task_type):
    emojis = {
        "Exercise": "🐕",
        "Feeding": "🍖",
        "Medication": "💊",
        "Grooming": "🛁"
    }
    return f"{emojis.get(task_type, '🐾')} {task_type}"


def format_priority(priority):
    indicators = {
        "high": "🔴 High",
        "medium": "🟡 Medium",
        "low": "🟢 Low"
    }
    return indicators.get(priority.lower(), priority)


def format_status(completed):
    return "✅ Completed" if completed else "⏳ Pending"


DATA_FILE = "data.json"


st.set_page_config(
    page_title="PawPal+",
    page_icon="🐾",
    layout="centered"
)

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+!

Organize your pets' care tasks, manage recurring activities,
and generate a daily schedule with conflict warnings.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps pet owners
plan care tasks for their pets based on duration, priority, and
available time.

The app connects the Streamlit interface to the Owner, Pet, Task,
and Scheduler classes.
"""
    )

with st.expander("Features", expanded=False):
    st.markdown(
        """
- Add and manage pets.
- Create pet care tasks with duration, priority, and scheduled time.
- Choose a due date for each task.
- Mark tasks as completed.
- Automatically create the next daily or weekly recurring task.
- Preserve completed tasks and their original due dates.
- Sort tasks by priority and scheduled time.
- Filter tasks by completion status and pet.
- Detect tasks scheduled for the same date and time.
- Identify tasks that exceed the available time budget.
- Save and load pets and tasks using JSON persistence.
- Display task types using emojis.
- Show visual priority indicators.
- Display task completion status.
- Format task tables for improved readability.
"""
    )

st.divider()


# Initialize the Owner and load saved data once per session.
if "owner" not in st.session_state:
    owner = Owner(
        owner_id="O001",
        name="Jordan",
        preferences={"preferred_start": "08:00"}
    )

    try:
        owner.load_from_json(DATA_FILE)
        st.session_state["owner"] = owner
        st.session_state["data_loaded"] = True
    except FileNotFoundError:
        st.session_state["owner"] = owner
        st.session_state["data_loaded"] = True

owner = st.session_state["owner"]


# Pet input section.
st.subheader("Add a Pet")

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
        owner.save_to_json(DATA_FILE)

        st.success(f"{pet.name} was added!")
        st.rerun()
    else:
        st.error("Please enter a pet name.")


# Display pets belonging to the owner.
st.subheader("Your Pets")

if owner.pets:
    for pet in owner.pets:
        st.write(f"🐾 **{pet.name}** — {pet.species.title()}")
else:
    st.info("No pets yet. Add one above.")


st.divider()


# Task input section.
st.subheader("Tasks")
st.caption(
    "Add care tasks and associate each task with a pet."
)

if owner.pets:
    selected_pet_id = st.selectbox(
        "Choose a pet for this task",
        options=[pet.pet_id for pet in owner.pets],
        format_func=lambda pet_id: next(
            pet.name for pet in owner.pets
            if pet.pet_id == pet_id
        ),
        key="selected_pet_id"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        task_title = st.text_input(
            "Task title",
            value="Morning walk",
            key="task_title"
        )

    with col2:
        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=240,
            value=20,
            key="task_duration"
        )

    with col3:
        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            index=2,
            key="task_priority"
        )

    task_type = st.selectbox(
        "Task type",
        ["Feeding", "Exercise", "Grooming", "Medication", "Other"],
        key="task_type"
    )

    task_time = st.time_input(
        "Task time",
        value=time(8, 0),
        key="task_time"
    )

    task_date = st.date_input(
        "Due date",
        value=date.today(),
        key="task_date"
    )

    frequency = st.selectbox(
        "Frequency",
        ["daily", "weekly", "as needed"],
        key="task_frequency"
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
                frequency=frequency,
                due_date=task_date
            )

            selected_pet.add_task(task)
            owner.save_to_json(DATA_FILE)

            st.success(
                f"Added '{task.title}' to {selected_pet.name}."
            )
            st.rerun()
        else:
            st.error("Please enter a task title.")
else:
    st.info("Add a pet before adding tasks.")


# Display all existing tasks with formatting.
st.subheader("All Tasks")

task_rows = []

for pet in owner.pets:
    for task in pet.get_tasks():
        task_rows.append({
            "Pet": pet.name,
            "Task": task.title,
            "Due Date": task.due_date,
            "Duration (min)": task.duration,
            "Priority": format_priority(task.priority),
            "Time": task.time,
            "Type": format_task_type(task.task_type),
            "Frequency": task.frequency,
            "Status": format_status(task.completed)
        })

if task_rows:
    st.table(task_rows)
else:
    st.info("No tasks yet. Add a task above.")


# Update task completion status.
st.divider()
st.subheader("Update Task Status")

incomplete_tasks = [
    (pet, task)
    for pet in owner.pets
    for task in pet.get_tasks()
    if not task.completed
]

if incomplete_tasks:
    selected_index = st.selectbox(
        "Select a task to mark as completed",
        options=range(len(incomplete_tasks)),
        format_func=lambda index: (
            f"{incomplete_tasks[index][0].name} - "
            f"{incomplete_tasks[index][1].title} "
            f"({incomplete_tasks[index][1].due_date}, "
            f"{incomplete_tasks[index][1].time})"
        ),
        key="task_to_complete"
    )

    if st.button("Mark as Completed"):
        selected_task = incomplete_tasks[selected_index][1]

        scheduler = Scheduler(available_time=1440)
        scheduler.get_tasks_from_owner(owner)

        next_task = scheduler.complete_task(owner, selected_task)

        # Save the completed task and any recurring occurrence.
        owner.save_to_json(DATA_FILE)

        st.success(
            f"'{selected_task.title}' marked as completed!"
        )

        if next_task is not None:
            st.info(
                f"Next {next_task.frequency} occurrence scheduled "
                f"for {next_task.due_date} at {next_task.time}."
            )
        else:
            st.caption(
                "No recurring occurrence was created."
            )

        st.rerun()
else:
    st.info("There are no incomplete tasks to update.")


st.divider()


# Build a daily schedule using the Scheduler class.
st.subheader("Build Schedule")
st.caption(
    "Generate a priority-based daily plan and check for scheduling conflicts."
)

available_time = st.number_input(
    "Available time (minutes)",
    min_value=1,
    max_value=1440,
    value=60,
    key="available_time"
)

if st.button("Generate schedule"):
    scheduler = Scheduler(
        available_time=int(available_time)
    )
    scheduler.get_tasks_from_owner(owner)

    daily_plan = scheduler.generate_daily_plan()

    if daily_plan:
        st.markdown("### Today's Schedule")

        schedule_rows = []

        for task in daily_plan:
            pet_name_for_task = next(
                (
                    pet.name
                    for pet in owner.pets
                    if task in pet.get_tasks()
                ),
                "Unknown"
            )

            schedule_rows.append({
                "Due Date": task.due_date,
                "Time": task.time,
                "Pet": pet_name_for_task,
                "Task": task.title,
                "Duration (min)": task.duration,
                "Priority": format_priority(task.priority),
                "Type": format_task_type(task.task_type),
                "Status": format_status(task.completed)
            })

        st.table(schedule_rows)
    else:
        st.info("There are no incomplete tasks to schedule.")

    time_conflicts = scheduler.detect_time_conflicts()

    st.markdown("### Same-Time Conflict Check")

    if time_conflicts:
        st.warning(
            "Scheduling conflicts found. Review the tasks below "
            "to avoid scheduling care activities at the same time."
        )

        for conflict in time_conflicts:
            st.write(f"⚠️ {conflict}")
    else:
        st.success("No same-time scheduling conflicts detected.")

    budget_conflicts = scheduler.detect_conflicts()

    st.markdown("### Available-Time Check")

    if budget_conflicts:
        st.warning(
            "Some tasks exceed the available time budget. "
            "Consider adjusting your schedule."
        )

        for task in budget_conflicts:
            st.write(f"- {task.title}")
    else:
        st.success(
            "All tasks fit within the available time budget."
        )
