from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status() -> None:
	task = Task(title="Morning walk", duration_minutes=20)

	task.mark_complete()

	assert task.completed is True


def test_adding_task_to_pet_increases_task_count() -> None:
	pet = Pet(name="Mochi")
	task = Task(title="Feed breakfast", duration_minutes=10)

	starting_count = len(pet.tasks)
	pet.add_task(task)

	assert len(pet.tasks) == starting_count + 1
	assert pet.tasks[0] is task
