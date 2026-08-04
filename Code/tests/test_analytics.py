import pytest
from datetime import datetime,timedelta
from habit import Habit
from analytics import (total_habits,longest_streak,get_longest_streak_all,
                       get_longest_streak_for_habit, get_current_streaks, get_habit_summary,
                       get_habits_by_periodicity, count_by_periodicity, most_completed_habit,
                       total_completions)

def test_total_habits():
    habit1 = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
    )
    habit2 = Habit(
        name="Exercise",
        description="Exercise for 30 minutes",
        periodicity="weekly",
    )
    habits = [habit1, habit2]

    assert total_habits(habits) == 2

def test_longest_streak():
    today = datetime.now()
    habit1 = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
        completions=[(today - timedelta(days=2)).isoformat(),
                     (today - timedelta(days=1)).isoformat(),
                     today.isoformat()]
    )
    habit2 = Habit(
        name="Exercise",
        description="Exercise for 30 minutes",
        periodicity="weekly",
        completions=[(today - timedelta(days=1)).isoformat(),
                     today.isoformat()]
    )
    habits = [habit1, habit2]
    result = longest_streak(habits)
    assert result.name == "Drink Water"

def test_get_longest_streak_all():
    today = datetime.now()
    habit1 = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
        completions=[(today - timedelta(days=2)).isoformat(),
                     (today - timedelta(days=1)).isoformat(),
                     today.isoformat()]
    )
    habit2 = Habit(
        name="Exercise",
        description="Exercise for 30 minutes",
        periodicity="weekly",
        completions=[(today - timedelta(days=1)).isoformat(),
                     today.isoformat()]
    )
    habits = [habit1, habit2]
    assert get_longest_streak_all(habits) == 3

def test_get_longest_streak_for_habit():
    today = datetime.now()
    habit = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
        completions=[(today - timedelta(days=2)).isoformat(),
                     (today - timedelta(days=1)).isoformat(),
                     today.isoformat()]
    )
    habit = [habit]
    assert get_longest_streak_for_habit(habit, "Drink Water") == 3

def test_get_current_streaks():
    today = datetime.now()
    habit = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
        completions=[(today - timedelta(days=1)).isoformat(),
                     today.isoformat()]
    )
    habit = [habit]
    result = get_current_streaks(habit)
    assert result[0]["name"] == "Drink Water"
    assert result[0]["current_streak"] == 2

def test_get_habit_summary():
    habit = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily"
    )
    habit = [habit]
    result = get_habit_summary(habit)
    assert result[0]["name"] == "Drink Water"
    assert result[0]["description"] == "Drink 1L of water"
    assert result[0]["periodicity"] == "daily"
    assert result[0]["total_completions"] == 0

def test_get_habits_by_periodicity():
    daily_habit = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily"
    )
    weekly_habit = Habit(
        name="Exercise",
        description="Exercise for 30 minutes",
        periodicity="weekly"
    )
    habits = [daily_habit, weekly_habit]
    result = get_habits_by_periodicity(habits, "daily")
    assert len(result) == 1
    assert result[0].name == "Drink Water"

def test_count_by_periodicity():
    habit1 = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily"
    )
    habit2 = Habit(
        name="Exercise",
        description="Exercise for 30 minutes",
        periodicity="weekly"
    )
    habit3 = Habit(
        name="Plan Meals",
        description="Plan meals for a week",
        periodicity="weekly"
    )
    habits = [habit1, habit2, habit3]
    result = count_by_periodicity(habits)
    assert result["daily"] == 1
    assert result["weekly"] == 2

def test_most_completed_habit():
    today = datetime.now()
    habit1 = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
        completions=[(today - timedelta(days=2)).isoformat(),
                     (today - timedelta(days=1)).isoformat(),
                     today.isoformat()]
    )
    habit2 = Habit(
        name="Exercise",
        description="Exercise for 30 minutes",
        periodicity="weekly",
        completions=[(today - timedelta(days=1)).isoformat(),
                     today.isoformat()]
    )
    habits = [habit1, habit2]
    result = most_completed_habit(habits)
    assert len(result) == 1
    assert result[0].name == "Drink Water"

def test_total_completions():
    habit = Habit(
        name="Drink Water",
        description="Drink 1L of water",
        periodicity="daily",
        completions=[datetime.now().isoformat(),
                     datetime.now().isoformat()]
    )

    assert total_completions(habit) == 2