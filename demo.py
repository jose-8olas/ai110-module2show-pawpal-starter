from pawpal_system import Task, Scheduler

scheduler = Scheduler(available_time=480)

# Add sample tasks
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

# Generate priority-based schedule
daily_plan = scheduler.generate_daily_plan()

# Display results
print("\n========================================")
print("       PawPal+ Daily Schedule")
print("========================================")
print(f"{'Task':<20}{'Priority':<12}{'Time'}")
print("----------------------------------------")

for task in daily_plan:
    print(f"{task.title:<20}{task.priority:<12}{task.time}")

print("========================================")
print("Tasks sorted by priority, then time.")