"""Logic layer where all PawPal+ backend classes live."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from uuid import uuid4


def _priority_rank(priority: str) -> int:
	order = {"high": 0, "medium": 1, "low": 2}
	return order.get(priority.lower(), 1)


def _recurrence_days(recurrence: str, recurrence_interval_days: int) -> int:
	if recurrence_interval_days > 0:
		return recurrence_interval_days
	defaults = {
		"daily": 1,
		"weekly": 7,
		"monthly": 30,
	}
	return defaults.get(recurrence.lower(), 0)


@dataclass
class Task:
	task_id: str = field(default_factory=lambda: str(uuid4()))
	pet_id: str = ""
	title: str = ""
	duration_minutes: int = 0
	priority: str = "medium"
	recurrence: str = "none"
	recurrence_interval_days: int = 0
	next_due_date: date | None = None
	completed: bool = False

	def edit_task(
		self,
		title: str | None = None,
		duration_minutes: int | None = None,
		priority: str | None = None,
		recurrence: str | None = None,
		recurrence_interval_days: int | None = None,
	) -> None:
		"""Update the task details in place."""
		if title is not None:
			self.title = title
		if duration_minutes is not None:
			self.duration_minutes = duration_minutes
		if priority is not None:
			self.priority = priority
		if recurrence is not None:
			self.recurrence = recurrence
		if recurrence_interval_days is not None:
			self.recurrence_interval_days = recurrence_interval_days

		if self.recurrence.lower() == "none":
			self.recurrence_interval_days = 0

	def mark_completed(self, completed_on: date | None = None) -> None:
		"""Mark the task complete and advance recurring tasks."""
		completion_date = completed_on or date.today()
		self.completed = True

		interval_days = _recurrence_days(self.recurrence, self.recurrence_interval_days)
		if interval_days > 0:
			self.next_due_date = completion_date + timedelta(days=interval_days)
			self.completed = False

	def mark_complete(self, completed_on: date | None = None) -> None:
		"""Alias for mark_completed()."""
		self.mark_completed(completed_on=completed_on)


@dataclass
class Pet:
	pet_id: str = field(default_factory=lambda: str(uuid4()))
	name: str = ""
	age: int = 0
	species: str = ""
	breed: str = ""
	tasks: list[Task] = field(default_factory=list)

	def update_info(self, name: str, age: int, species: str, breed: str) -> None:
		"""Replace the stored pet profile details."""
		self.name = name
		self.age = age
		self.species = species
		self.breed = breed

	def add_task(self, task: Task) -> None:
		"""Attach a task to this pet and set its pet ID."""
		task.pet_id = self.pet_id
		if all(existing.task_id != task.task_id for existing in self.tasks):
			self.tasks.append(task)


@dataclass
class Scheduler:
	all_tasks: list[Task] = field(default_factory=list)
	today_tasks: list[Task] = field(default_factory=list)
	tasks_left: list[Task] = field(default_factory=list)
	completed_tasks: list[Task] = field(default_factory=list)

	def _find_task(self, task_id: str) -> Task | None:
		"""Return the task with the matching ID if it exists."""
		for task in self.all_tasks:
			if task.task_id == task_id:
				return task
		return None

	def _sync_owner_tasks(self, owner: Owner) -> None:
		"""Pull in tasks from all pets owned by the given owner."""
		for pet in owner.pets:
			for task in pet.tasks:
				if task.pet_id != pet.pet_id:
					task.pet_id = pet.pet_id
				if all(existing.task_id != task.task_id for existing in self.all_tasks):
					self.all_tasks.append(task)

	def _refresh_views(self, reference_date: date | None = None) -> None:
		"""Rebuild the scheduler's cached task views."""
		today = reference_date or date.today()
		due_tasks = [
			task
			for task in self.all_tasks
			if not task.completed and (task.next_due_date is None or task.next_due_date <= today)
		]
		due_tasks.sort(
			key=lambda task: (
				_priority_rank(task.priority),
				task.next_due_date or today,
				task.duration_minutes,
				task.title.lower(),
			)
		)
		self.today_tasks = list(due_tasks)
		self.tasks_left = []
		self.completed_tasks = [task for task in self.all_tasks if task.completed]

	def add_task(self, task: Task) -> None:
		"""Add a task to the scheduler and refresh cached views."""
		if all(existing.task_id != task.task_id for existing in self.all_tasks):
			self.all_tasks.append(task)
		self._refresh_views()

	def edit_task(
		self,
		task_id: str,
		title: str | None = None,
		duration_minutes: int | None = None,
		priority: str | None = None,
		recurrence: str | None = None,
		recurrence_interval_days: int | None = None,
	) -> None:
		"""Edit an existing task by ID."""
		task = self._find_task(task_id)
		if task is None:
			raise ValueError(f"Task not found: {task_id}")
		task.edit_task(
			title=title,
			duration_minutes=duration_minutes,
			priority=priority,
			recurrence=recurrence,
			recurrence_interval_days=recurrence_interval_days,
		)
		self._refresh_views()

	def schedule_tasks(self, owner: Owner, available_minutes: int | None = None) -> list[Task]:
		"""Choose the highest-priority tasks that fit in the available time."""
		self._sync_owner_tasks(owner)
		today = date.today()
		due_tasks = [
			task
			for task in self.all_tasks
			if not task.completed and (task.next_due_date is None or task.next_due_date <= today)
		]
		due_tasks.sort(
			key=lambda task: (
				_priority_rank(task.priority),
				task.next_due_date or today,
				task.duration_minutes,
				task.title.lower(),
			)
		)

		selected: list[Task] = []
		minutes_used = 0
		for task in due_tasks:
			if available_minutes is not None and minutes_used + task.duration_minutes > available_minutes:
				continue
			selected.append(task)
			minutes_used += task.duration_minutes

		self.today_tasks = selected
		self.tasks_left = [task for task in due_tasks if task not in selected]
		self.completed_tasks = [task for task in self.all_tasks if task.completed]
		return selected

	def get_today_tasks(self, pet_id: str | None = None) -> list[Task]:
		"""Return today's tasks, optionally filtered by pet."""
		if not self.today_tasks:
			self._refresh_views()

		if pet_id is None:
			return list(self.today_tasks)
		return [task for task in self.today_tasks if task.pet_id == pet_id]

	def mark_task_completed(self, task_id: str) -> None:
		"""Mark the task with the given ID as completed."""
		task = self._find_task(task_id)
		if task is None:
			raise ValueError(f"Task not found: {task_id}")
		task.mark_completed()
		self._refresh_views()


@dataclass
class Owner:
	name: str = ""
	age: int = 0
	busy_time: str = ""
	scheduler: Scheduler = field(default_factory=Scheduler)
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to the owner and sync its tasks to the scheduler."""
		if all(existing.pet_id != pet.pet_id for existing in self.pets):
			self.pets.append(pet)
		for task in pet.tasks:
			self.scheduler.add_task(task)

	def update_busy_time(self, busy_time: str) -> None:
		"""Update the owner's busy-time note."""
		self.busy_time = busy_time
