
from typing import List
from habit import Habit


#Total number of habits
def total_habits(habits : List[Habit]) -> int:
    return len(habits)

#Return habit with the longest streak
def longest_streak(habits: List[Habit]) -> Habit | None:
    if not habits:
        return None

    return max(
        habits,
        key=lambda habit: habit.longest_streak(),
        default=None
    )

#Return longest streak among all habits
def get_longest_streak_all(habit: List[Habit]) -> int:
    return max(map(lambda h: h.longest_streak(), habit), default=0)


#Return longest streak of a specific habit
def get_longest_streak_for_habit(habits: List[Habit], name: str) -> int:
    for habit in habits:
        if habit.name.lower() == name.lower():
            return habit.longest_streak()
    return 0

#Return the current streak for each habit
def get_current_streaks(habits: List[Habit]) -> List[dict]:
    return [{
            "name": habit.name,
            "current_streak": habit.current_streak()}
        for habit in habits
    ]

#Habit summary with all habit info
def get_habit_summary(habits: List[Habit]) -> List[dict]:
    return [
        {
            "name": habit.name,
            "description": habit.description,
            "periodicity": habit.periodicity,
            "current_streak": habit.current_streak(),
            "longest_streak": habit.longest_streak(),
            "total_completions": len(habit.completions),
            "created_at": habit.created_at.strftime("%d/%m/%Y")
        }
        for habit in habits
        ]

#filter habits by periodicity
def get_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    return list(filter(lambda h: h.periodicity.lower() == periodicity.lower(), habits))


#count daily and weekly habits
def count_by_periodicity(habits: List[Habit]) -> dict[str, int]:
    daily = sum(1 for habit in habits if habit.periodicity.lower() == "daily")
    weekly = sum(1 for habit in habits if habit.periodicity.lower() == "weekly")
    return {"daily": daily, "weekly": weekly}

#get most completed habit
def most_completed_habit(habit: List[Habit]):
    if not habit:
        return []
    max_count = max(len(habit.completions) for habit in habit)
    return [habit for habit in habit
        if len(habit.completions) == max_count
    ]
#get total number of completions for a specific habit
def total_completions(habit: Habit) -> int:
    return len(habit.completions)