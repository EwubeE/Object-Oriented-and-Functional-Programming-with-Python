from datetime import datetime, timedelta
from typing import List

# Represents a single habit to track
class Habit:
    #initialize habit details and completion history
    def __init__(
            self,
            name: str,
            description: str,
            periodicity: str,
            created_at: datetime = None,
            completions: List[str] = None,
    ):

        #validate habit input
        if not name.strip():
            raise ValueError("Habit name required")
        if periodicity not in ["daily", "weekly"]:
            raise ValueError("Habit periodicity must be 'daily' or 'weekly'")


        #store habit info
        self.name = name.strip()
        self.description = description.strip()
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now()
        self.completions = completions or []


    def mark_complete(self): # marks the habit as completed at the current time
        self.completions.append(datetime.now().isoformat())


    def _period_delta(self):        #time between completions
        if self.periodicity == "daily":
            return timedelta(days=1)
        elif self.periodicity == "weekly":
            return timedelta(weeks=1)
        raise ValueError("Habit periodicity must be 'daily' or 'weekly'")


    def current_streak(self) -> int:      #calculate current streak from completion history
        if not self.completions:
            return 0
        dates = sorted(datetime.fromisoformat(c) for c in self.completions)
        period = self._period_delta()
        today = datetime.now()

        if today - dates[-1] > period:    #reset streak if last completion is old
            return 0

        streak = 1     #count consecutive completions backwards

        for i in range(len(dates) - 1, 0, -1):
            if dates[i] - dates[i - 1] <= period:
                streak += 1
            else:
                break

        return streak

    def longest_streak(self) -> int:      #longest streak achieved
        if not self.completions:
            return 0

        dates = sorted(datetime.fromisoformat(c) for c in self.completions)
        longest = 1
        current = 1
        period = self._period_delta()

        for i in range(1, len(dates)):
            if dates[i] - dates[i - 1] <= period:
                current += 1
                longest = max(longest, current)
            else:
                current = 1

        return longest

    @staticmethod
    def from_dict(data: dict) -> "Habit":  # create a habit object from dictionary data
        return Habit(
            name=data["name"],
            description=data["description"],
            periodicity=data["periodicity"],
            created_at=datetime.fromisoformat(data["created_at"]),
            completions=data.get("completions", [])
        )
    def to_dict(self) -> dict: #convert habit object to dictionary for JSON storage
        return {
            "name": self.name,
            "description": self.description,
            "periodicity": self.periodicity,
            "created_at": self.created_at.isoformat(),
            "completions": self.completions
        }
