from pawpal_system import Owner, Pet, Task, Scheduler, Schedule

owner = Owner(name="Jordan", available_minutes=90)

biscuit = Pet(name="Biscuit", species="dog", age=3)
biscuit.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", time=7 * 60, recurrence="daily"))
biscuit.add_task(Task(title="Feeding", duration_minutes=10, priority="high", time=7 * 60 + 30))

mochi = Pet(name="Mochi", species="cat", age=5)
mochi.add_task(Task(title="Grooming", duration_minutes=15, priority="medium", time=9 * 60, recurrence="weekly"))
mochi.add_task(Task(title="Playtime", duration_minutes=20, priority="low", time=9 * 60))

owner.add_pet(biscuit)
owner.add_pet(mochi)

schedule = owner.get_schedule()

width = 65
print("=" * width)
print(f"  Today's Schedule for {owner.name}")
print("=" * width)
print(f"  {'#':<4} {'TIME':<6}  {'PET':<12} {'TASK':<22} {'DUR':>6}  PRIORITY")
print("-" * width)
print(schedule.display())
print("=" * width)

scheduler = Scheduler()

# --- Sort tasks by their preferred time ---
print("\nTasks sorted by time:")
for task in scheduler.sort_by_time(owner.get_all_tasks()):
    label = f"{task.time // 60:02d}:{task.time % 60:02d}" if task.time is not None else "--:--"
    print(f"  {label}  {task.title}")

# --- Filter tasks by pet name / completion status ---
print("\nBiscuit's pending tasks:")
for task, pet_name in owner.filter_tasks(completed=False, pet_name="Biscuit"):
    print(f"  {pet_name}: {task.title}")

# --- Recurring tasks: completing one queues up its next occurrence ---
print("\nCompleting 'Morning walk' (daily) for Biscuit...")
biscuit.complete_task("Morning walk")
for task in biscuit.tasks:
    status = "done" if task.completed else "pending"
    due = task.due_date if task.due_date else "n/a"
    print(f"  {task.title:<15} [{status}]  due={due}  recurrence={task.recurrence}")

# --- Conflict detection: two tasks double-booked at the same time ---
print("\nConflict detection demo:")
conflict_schedule = Schedule()
conflict_schedule.add_entry(Task(title="Vet visit", duration_minutes=30, priority="high"), start_time=9 * 60, pet_name="Biscuit")
conflict_schedule.add_entry(Task(title="Grooming", duration_minutes=15, priority="medium"), start_time=9 * 60, pet_name="Mochi")

warnings = scheduler.detect_conflicts(conflict_schedule)
if warnings:
    for warning in warnings:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts found.")
