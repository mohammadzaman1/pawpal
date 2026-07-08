from pawpal_system import Owner, Pet, Task


def build_demo_data() -> Owner:
	owner = Owner(name="Jordan", age=32, busy_time="9am-5pm")

	pet_one = Pet(name="Mochi", age=4, species="cat", breed="tabby")
	pet_two = Pet(name="Biscuit", age=7, species="dog", breed="golden retriever")

	pet_one.add_task(Task(title="Morning feeding", duration_minutes=10, priority="high"))
	pet_one.add_task(Task(title="Litter box cleanup", duration_minutes=15, priority="medium"))
	pet_two.add_task(Task(title="Afternoon walk", duration_minutes=30, priority="high"))

	owner.add_pet(pet_one)
	owner.add_pet(pet_two)
	return owner


def print_todays_schedule(owner: Owner) -> None:
	scheduled_tasks = owner.scheduler.schedule_tasks(owner)

	print("Today's Schedule")
	print("-" * 18)

	if not scheduled_tasks:
		print("No tasks scheduled for today.")
		return

	for task in scheduled_tasks:
		pet_name = next((pet.name for pet in owner.pets if pet.pet_id == task.pet_id), "Unknown pet")
		print(f"{pet_name}: {task.title} ({task.duration_minutes} min, priority: {task.priority})")


if __name__ == "__main__":
	owner = build_demo_data()
	print_todays_schedule(owner)