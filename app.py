import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(name=owner_name)
if "generated_schedule" not in st.session_state:
    st.session_state["generated_schedule"] = []

owner = st.session_state["owner"]
owner.name = owner_name

st.markdown("### Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=4)
    pet_species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_breed = st.text_input("Breed", value="tabby")
    add_pet_submitted = st.form_submit_button("Add Pet")

if add_pet_submitted:
    new_pet = Pet(name=pet_name, age=int(pet_age), species=pet_species, breed=pet_breed)
    owner.add_pet(new_pet)
    st.success(f"Added {new_pet.name}.")

st.markdown("### Add a Task")
st.caption("Choose a pet, then add a task that will be sent to that pet's task list.")

pet_options = owner.pets or [Pet(name="No pets yet")]
selected_pet_name = st.selectbox("Assign to pet", [pet.name for pet in pet_options])
selected_pet = next((pet for pet in owner.pets if pet.name == selected_pet_name), None)

with st.form("add_task_form", clear_on_submit=True):
    task_title = st.text_input("Task title", value="Morning walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    add_task_submitted = st.form_submit_button("Add Task")

if add_task_submitted:
    if selected_pet is None:
        st.error("Add a pet first, then assign the task to that pet.")
    else:
        new_task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
        selected_pet.add_task(new_task)
        owner.scheduler.add_task(new_task)
        st.success(f"Added {new_task.title} to {selected_pet.name}.")

if owner.pets:
    st.write("Current pets and tasks:")
    for pet in owner.pets:
        st.markdown(f"**{pet.name}** ({pet.species}, age {pet.age})")
        if pet.tasks:
            st.table(
                [
                    {
                        "title": task.title,
                        "duration_minutes": task.duration_minutes,
                        "priority": task.priority,
                    }
                    for task in pet.tasks
                ]
            )
        else:
            st.caption("No tasks yet.")
else:
    st.info("No pets yet. Add a pet above to start scheduling tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button calls the scheduler and displays today's tasks.")

available_minutes = st.number_input("Available minutes", min_value=0, max_value=1440, value=120)

if st.button("Generate schedule"):
    st.session_state["generated_schedule"] = owner.scheduler.schedule_tasks(
        owner,
        available_minutes=int(available_minutes) if available_minutes else None,
    )

if st.session_state["generated_schedule"]:
    st.write("Today's Schedule")
    for task in st.session_state["generated_schedule"]:
        pet_name = next((pet.name for pet in owner.pets if pet.pet_id == task.pet_id), "Unknown pet")
        st.write(f"{pet_name}: {task.title} ({task.duration_minutes} min, priority: {task.priority})")
else:
    st.info("Generate a schedule to see today's tasks.")
