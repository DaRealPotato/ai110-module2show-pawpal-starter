from datetime import date

import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Session State Setup ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# ── SECTION 1: Owner Setup ─────────────────────────────────────────────────────
st.subheader("1. Owner Info")

owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes today", min_value=10, max_value=480, value=90)

if st.button("Save owner"):
    if st.session_state.owner is None:
        st.session_state.owner = Owner(name=owner_name, available_minutes=available_minutes)
    else:
        # Update in place instead of replacing, so existing pets/tasks aren't wiped out.
        st.session_state.owner.name = owner_name
        st.session_state.owner.available_minutes = available_minutes
    st.success(f"Owner '{owner_name}' saved with {available_minutes} min available.")

if st.session_state.owner is None:
    st.info("Save owner info above to continue.")
    st.stop()

st.divider()

# ── SECTION 2: Add a Pet ───────────────────────────────────────────────────────
# Calls: owner.add_pet(pet)
st.subheader("2. Add a Pet")

col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species, age=age)
    st.session_state.owner.add_pet(new_pet)      # ← Phase 2 method
    st.success(f"Added {pet_name} the {species}.")

if st.session_state.owner.pets:
    st.write("Your pets:")
    st.table([
        {"name": p.name, "species": p.species, "age": p.age, "tasks": len(p.tasks)}
        for p in st.session_state.owner.pets
    ])
else:
    st.info("No pets added yet.")
    st.stop()

st.divider()

# ── SECTION 3: Add a Task ──────────────────────────────────────────────────────
# Calls: pet.add_task(task)
st.subheader("3. Add a Task")

pet_names = [p.name for p in st.session_state.owner.pets]
selected_pet_name = st.selectbox("Assign task to", pet_names)
selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    has_preferred_time = st.checkbox("Set a preferred time?")
    preferred_time = st.time_input("Preferred time", disabled=not has_preferred_time)
with col5:
    recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])

if st.button("Add task"):
    task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=priority,
        time=(preferred_time.hour * 60 + preferred_time.minute) if has_preferred_time else None,
        recurrence=None if recurrence == "none" else recurrence,
        due_date=date.today() if recurrence != "none" else None,
    )
    selected_pet.add_task(task)                  # ← Phase 2 method
    st.success(f"Added '{task_title}' to {selected_pet_name}.")

all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("All tasks across pets:")
    st.table([
        {
            "pet": p.name,
            "task": t.title,
            "duration (min)": t.duration_minutes,
            "priority": t.priority,
            "recurrence": t.recurrence or "-",
            "completed": t.completed,
        }
        for p in st.session_state.owner.pets
        for t in p.tasks
    ])

    st.write("Mark a task complete:")
    pending_pairs = [(p, t) for p in st.session_state.owner.pets for t in p.tasks if not t.completed]
    if pending_pairs:
        labels = [f"{p.name} — {t.title}" for p, t in pending_pairs]
        selected_label = st.selectbox("Task to complete", labels)
        if st.button("Mark complete"):
            pet, task = pending_pairs[labels.index(selected_label)]
            pet.complete_task(task.title)          # ← auto-queues next occurrence if recurring
            st.success(f"Marked '{task.title}' complete for {pet.name}.")
            st.rerun()
    else:
        st.info("No pending tasks to complete.")
else:
    st.info("No tasks yet.")

st.divider()

# ── SECTION 4: Generate Schedule ──────────────────────────────────────────────
# Calls: owner.get_schedule() → Scheduler.generate(owner)
st.subheader("4. Generate Schedule")

scheduler = Scheduler()

with st.expander("Preview tasks by preferred time (Scheduler.sort_by_time)"):
    time_sorted = scheduler.sort_by_time(all_tasks)
    if time_sorted:
        st.table([
            {
                "preferred time": f"{t.time // 60:02d}:{t.time % 60:02d}" if t.time is not None else "no preference",
                "task": t.title,
                "priority": t.priority,
            }
            for t in time_sorted
        ])
    else:
        st.info("No tasks yet.")

if st.button("Generate schedule"):
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        schedule = st.session_state.owner.get_schedule()   # ← Phase 2 method
        if not schedule.entries:
            st.warning("No tasks fit within the available time.")
        else:
            conflicts = scheduler.detect_conflicts(schedule)
            conflicting_titles = set()
            for warning in conflicts:
                for entry in schedule.entries:
                    if f"'{entry.task.title}'" in warning:
                        conflicting_titles.add(entry.task.title)

            st.success("Here is today's plan:")
            st.table([
                {
                    "⚠️": "⚠️" if entry.task.title in conflicting_titles else "",
                    "time": entry.start_time_str(),
                    "pet": entry.pet_name,
                    "task": entry.task.title,
                    "duration (min)": entry.task.duration_minutes,
                    "priority": entry.task.priority,
                    "reasoning": entry.reasoning,
                }
                for entry in schedule.entries
            ])

            if conflicts:
                st.warning(
                    f"⏰ {len(conflicts)} scheduling conflict(s) found — rows marked ⚠️ above overlap in time."
                )
                for warning in conflicts:
                    st.markdown(f"- {warning}")
                st.caption("Tip: give one of the overlapping tasks a different preferred time, or shorten its duration, then regenerate the schedule.")
            else:
                st.info("✅ No scheduling conflicts — every task has a clear time slot.")
