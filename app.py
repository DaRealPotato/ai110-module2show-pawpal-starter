import streamlit as st
from pawpal_system import Owner, Pet, Task

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
    st.session_state.owner = Owner(name=owner_name, available_minutes=available_minutes)
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

if st.button("Add task"):
    task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
    selected_pet.add_task(task)                  # ← Phase 2 method
    st.success(f"Added '{task_title}' to {selected_pet_name}.")

all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("All tasks across pets:")
    st.table([
        {"pet": p.name, "task": t.title, "duration (min)": t.duration_minutes, "priority": t.priority}
        for p in st.session_state.owner.pets
        for t in p.tasks
    ])
else:
    st.info("No tasks yet.")

st.divider()

# ── SECTION 4: Generate Schedule ──────────────────────────────────────────────
# Calls: owner.get_schedule() → Scheduler.generate(owner)
st.subheader("4. Generate Schedule")

if st.button("Generate schedule"):
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        schedule = st.session_state.owner.get_schedule()   # ← Phase 2 method
        if not schedule.entries:
            st.warning("No tasks fit within the available time.")
        else:
            st.success("Here is today's plan:")
            for i, entry in enumerate(schedule.entries, start=1):
                st.markdown(
                    f"**{i}. {entry.start_time_str()} — [{entry.pet_name}] {entry.task.title}**  \n"
                    f"{entry.task.duration_minutes} min · {entry.task.priority} priority  \n"
                    f"_{entry.reasoning}_"
                )
