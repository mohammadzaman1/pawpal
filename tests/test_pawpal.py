from pathlib import Path
import sys
from datetime import date, timedelta


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_scheduler_sort_by_time_orders_hh_mm_strings() -> None:
	scheduler = Scheduler()
	evening = Task(title="Dinner", time="18:30")
	morning = Task(title="Breakfast", time="07:15")
	unscheduled = Task(title="Grooming")

	ordered = scheduler.sort_by_time([evening, unscheduled, morning])

	assert ordered == [morning, evening, unscheduled]


def test_scheduler_handles_owner_with_no_tasks() -> None:
	owner = Owner(name="Jordan")
	pet = Pet(name="Mochi")

	owner.add_pet(pet)

	assert owner.scheduler.get_today_tasks() == []


def test_scheduler_filter_tasks_by_completion_and_pet_name() -> None:
	owner = Owner(name="Jordan")
	mochi = Pet(name="Mochi")
	biscuit = Pet(name="Biscuit")
	open_task = Task(title="Morning walk")
	done_task = Task(title="Feeding", completed=True)
	mochi.add_task(open_task)
	biscuit.add_task(done_task)
	owner.add_pet(mochi)
	owner.add_pet(biscuit)

	scheduler = owner.scheduler

	assert scheduler.filter_tasks(owner=owner, completed=True) == [done_task]
	assert scheduler.filter_tasks(owner=owner, pet_name="Mochi") == [open_task]


def test_scheduler_creates_next_daily_occurrence_when_completed() -> None:
	owner = Owner(name="Jordan")
	pet = Pet(name="Mochi")
	recurring_task = Task(title="Feed breakfast", recurrence="daily")
	pet.add_task(recurring_task)
	owner.add_pet(pet)

	owner.scheduler.mark_task_completed(recurring_task.task_id)

	assert recurring_task.completed is True
	assert len(owner.scheduler.all_tasks) == 2
	next_task = next(task for task in owner.scheduler.all_tasks if task.task_id != recurring_task.task_id)
	assert next_task.title == recurring_task.title
	assert next_task.pet_id == recurring_task.pet_id
	assert next_task.completed is False
	assert next_task.next_due_date == date.today() + timedelta(days=1)


def test_scheduler_detects_time_conflicts_with_warning() -> None:
	owner = Owner(name="Jordan")
	mochi = Pet(name="Mochi")
	biscuit = Pet(name="Biscuit")
	mochi.add_task(Task(title="Morning feeding", time="09:00"))
	biscuit.add_task(Task(title="Afternoon walk", time="09:00"))
	owner.add_pet(mochi)
	owner.add_pet(biscuit)

	warnings = owner.scheduler.detect_time_conflicts(owner=owner)

	assert len(warnings) == 1
	assert "09:00" in warnings[0]
	assert "Mochi: Morning feeding" in warnings[0]
	assert "Biscuit: Afternoon walk" in warnings[0]
