from pawpal_system import Owner, Pet, Task

owner = Owner(name="Jordan", available_minutes=90)

biscuit = Pet(name="Biscuit", species="dog", age=3)
biscuit.add_task(Task(title="Morning walk", duration_minutes=30, priority="high"))
biscuit.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))

mochi = Pet(name="Mochi", species="cat", age=5)
mochi.add_task(Task(title="Grooming", duration_minutes=15, priority="medium"))
mochi.add_task(Task(title="Playtime", duration_minutes=20, priority="low"))

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
