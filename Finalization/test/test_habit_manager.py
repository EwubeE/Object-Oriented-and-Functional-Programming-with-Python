import pytest
from habit_manager import HabitManager

def test_add_habit(tmp_path):
    storage = tmp_path / "test_habits.json"
    manager = HabitManager(storage_file=storage)
    manager.habits.clear()
    manager.add_habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily"
    )
    assert len(manager.habits) == 1
    assert manager.habits[0].name == "Drink Water"

def test_add_duplicate_habit(tmp_path):
    storage = tmp_path / "test_habits.json"
    manager = HabitManager(storage_file=storage)
    manager.habits.clear()
    manager.add_habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily"
    )
    with pytest.raises(ValueError):
        manager.add_habit(
            name="Drink Water",
            description="Drink 1L of water",
            periodicity="daily"
        )

def test_update_habit(tmp_path):
    storage = tmp_path / "test_habits.json"
    manager = HabitManager(storage_file=storage)
    manager.habits.clear()
    manager.add_habit(
        name="Drink water",
        description="Drink 1L of water",
        periodicity="daily"
    )
    updated = manager.update_habit(
        old_name="Drink water",
        new_name="Drink more water",
        new_description="Drink 3L of water",
        new_periodicity="weekly"
    )
    assert updated is True
    habit = manager.find_habit("Drink more water")
    assert habit is not None
    assert habit.name == "Drink more water"
    assert habit.description == "Drink 3L of water"
    assert habit.periodicity == "weekly"

def test_delete_habit(tmp_path):
    storage = tmp_path / "test_habits.json"
    manager = HabitManager(storage_file=storage)
    manager.habits.clear()
    manager.add_habit(
        name="Drink water",
        description="Drink 1L of water",
        periodicity="daily"
    )
    deleted = manager.delete_habit("Drink water")
    assert deleted is True
    assert len(manager.habits) == 0

def test_complete_habit(tmp_path):
    storage = tmp_path / "test_habits.json"
    manager = HabitManager(storage_file=storage)
    manager.habits.clear()
    manager.add_habit(
        name="Drink water",
        description="Drink 1L of water",
        periodicity="daily"
    )
    completed = manager.complete_habit("Drink water")
    assert completed is True
    assert len(manager.habits[0].completions) == 1

def test_save_load(tmp_path):
    storage = tmp_path / "test_habits.json"
    manager = HabitManager(storage_file=storage)
    manager.habits.clear()
    manager.add_habit(
        name="Drink water",
        description="Drink 1L of water",
        periodicity="daily"
    )
    manager.save()
    new_manager = HabitManager(storage_file=storage)
    assert len(new_manager.habits) == 1
    assert new_manager.habits[0].name == "Drink water"
    assert new_manager.habits[0].description == "Drink 1L of water"
    assert new_manager.habits[0].periodicity == "daily"
