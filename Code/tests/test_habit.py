import pytest
from habit import Habit
from datetime import datetime, timedelta

def test_create_valid_habit():
    habit = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity= "daily",
    )
    assert habit.name == "Drink Water"
    assert habit.description == "Drink 1L of water"
    assert habit.periodicity == "daily"
    assert habit.completions == []

def test_empty_habit():
    with pytest.raises(ValueError):
        Habit(
            name="",
            description="Drink 1L of water",
            periodicity="daily",
        )

def test_invalid_periodicity():
    with pytest.raises(ValueError):
        Habit(
            name="Drink Water",
            description="Drink 1L of water",
            periodicity="yearly"
        )

def test_mark_complete():
    habit = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
    )
    habit.mark_complete()
    assert len(habit.completions) == 1

def test_current_streak():
    today = datetime.now()
    completions = [
        (today - timedelta(days=2)).isoformat(),
        (today - timedelta(days=1)).isoformat(),
        today.isoformat(),
    ]
    habit = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
        completions=completions
    )
    assert habit.current_streak() == 3

def test_longest_streak():
    today = datetime.now()
    completions = [
        (today - timedelta(days=6)).isoformat(),
        (today - timedelta(days=5)).isoformat(),
        (today - timedelta(days=4)).isoformat(),
        (today - timedelta(days=3)).isoformat(),
        (today - timedelta(days=2)).isoformat(),
        (today - timedelta(days=1)).isoformat(),
        today.isoformat(),
    ]
    habit = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
        completions=completions
    )
    assert habit.longest_streak() == 7

def test_current_streak_reset_after_missed_day():
    today = datetime.now()
    completions = [
        (today - timedelta(days=3)).isoformat(),
        (today - timedelta(days=2)).isoformat(),
    ]
    habit = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
        completions=completions
    )
    assert habit.current_streak() == 0

