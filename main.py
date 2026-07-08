from pawpal_system import Owner, Pet, Task


def build_demo_data() -> Owner:
	owner = Owner(name="Jordan", age=32, busy_time="9am-5pm")

	pet_one = Pet(name="Mochi", age=4, species="cat", breed="tabby")
	pet_two = Pet(name="Biscuit", age=7, species="dog", breed="golden retriever")

	pet_one.add_task(Task(title="Litter box cleanup", time="18:00", duration_minutes=15, priority="medium"))
	pet_one.add_task(Task(title="Morning feeding", time="07:30", duration_minutes=10, priority="high"))
	pet_one.add_task(Task(title="Brush coat", time="09:00", duration_minutes=5, priority="low"))
	pet_two.add_task(Task(title="Afternoon walk", time="15:00", duration_minutes=30, priority="high"))
	pet_two.add_task(Task(title="Vet follow-up", time="09:00", duration_minutes=20, priority="low", completed=True))

	owner.add_pet(pet_one)
	owner.add_pet(pet_two)
	return owner


def print_demo_results(owner: Owner) -> None:
	scheduler = owner.scheduler
	sorted_tasks = scheduler.sort_by_time()
	completed_tasks = scheduler.filter_tasks(owner=owner, completed=True)
	mochi_tasks = scheduler.filter_tasks(owner=owner, pet_name="Mochi")
	conflict_warnings = scheduler.detect_time_conflicts(owner=owner)

	print("Tasks sorted by time")
	print("-" * 22)
	for task in sorted_tasks:
		pet_name = next((pet.name for pet in owner.pets if pet.pet_id == task.pet_id), "Unknown pet")
		print(f"{task.time or 'No time'} | {pet_name}: {task.title}")

	print()
	print("Completed tasks")
	print("-" * 16)
	for task in completed_tasks:
		pet_name = next((pet.name for pet in owner.pets if pet.pet_id == task.pet_id), "Unknown pet")
		print(f"{pet_name}: {task.title}")

	print()
	print("Mochi tasks")
	print("-" * 12)
	for task in mochi_tasks:
		print(f"{task.title} ({task.time or 'No time'})")

	print()
	print("Schedule warnings")
	print("-" * 17)
	if conflict_warnings:
		for warning in conflict_warnings:
			print(warning)
	else:
		print("No time conflicts found.")


if __name__ == "__main__":
	owner = build_demo_data()
	print_demo_results(owner)