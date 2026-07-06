"""Logic layer where all PawPal+ backend classes live."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Owner:
	name: str
	age: int
	busy_time: str
	pets: list[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		pass

	def update_busy_time(self, busy_time: str) -> None:
		pass


@dataclass
class Pet:
	name: str
	age: int
	type: str
	breed: str

	def update_info(self, name: str, age: int, type: str, breed: str) -> None:
		pass


@dataclass
class Task:
	title: str
	duration_minutes: int
	priority: str
	completed: bool = False

	def edit_task(self, title: str, duration_minutes: int, priority: str) -> None:
		pass

	def mark_completed(self) -> None:
		pass


@dataclass
class Scheduler:
	today_tasks: list[Task] = field(default_factory=list)
	tasks_left: list[Task] = field(default_factory=list)
	completed_tasks: list[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		pass

	def edit_task(self, task: Task) -> None:
		pass

	def schedule_tasks(self, owner: Owner, pet: Pet) -> list[Task]:
		pass

	def get_today_tasks(self) -> list[Task]:
		pass

	def mark_task_completed(self, task: Task) -> None:
		pass
