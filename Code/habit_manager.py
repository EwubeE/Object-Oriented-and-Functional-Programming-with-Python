import json
from pathlib import Path
from typing import List
from datetime import datetime, timedelta
from habit import Habit

#Manages the creation, deletion, completion, loading from and saving to json
class HabitManager:
    def __init__(self, storage_file: str = "data/habits.json"): #loads existing habits automatically
        self.storage_file = Path(storage_file)
        self.habits: List[Habit] = []
        self.load()

    def find_habit(self, name: str) -> Habit | None:
        for habit in self.habits:
            if habit.name.lower() == name.lower():
                return habit
        return None

    def load(self) -> None: #loads habits from json storage files
        if not self.storage_file.exists():
            self.habits =self._create_default_habits()
            self.save()
            return
        with open(self.storage_file, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                data = []
        self.habits = [Habit.from_dict(item) for item in data]

    def save(self) -> None: #save habits to the json storage file
        self.storage_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([habit.to_dict() for habit in self.habits],file,indent=4)

    def add_habit(self, name: str, description: str,periodicity): #add new habit and stores it
        if any(h.name.lower() == name.lower() for h in self.habits):
            raise ValueError("Habit already exist")
        habit = Habit(name, description, periodicity)
        self.habits.append(habit)
        self.save()

    def update_habit(self, old_name:str, new_name:str = None,new_description:str=None,
                     new_periodicity:str = None) -> bool: #updates an existing habit's name and periodicity
       habit = self.find_habit(old_name)
       if habit is None:
           return False

       if new_name:
           if any (habit.name.lower() == new_name.lower() and h != habit for h in self.habits):
               raise ValueError("A habit with this name already exists.")

           habit.name = new_name

       if new_description:
           habit.description = new_description
       if new_periodicity:
           if new_periodicity not in ["daily", "weekly"]:
               raise ValueError("Invalid periodicity. Choose 'daily' or 'weekly'")

           habit.periodicity = new_periodicity

       self.save()
       return True

    def delete_habit(self, name: str) -> bool:  #deletes a habit by name
        habit = self.find_habit(name)
        if habit is None:
            return False

        self.habits.remove(habit)
        self.save()
        return True


    def complete_habit(self, name: str) -> bool: #marks a habit as complete
        habit = self.find_habit(name)

        if habit is None:
            return False

        habit.mark_complete()
        self.save()
        return True


    def get_all_habits(self) -> List[Habit]: #show all tracked habits
        return self.habits



    #predefined habits
    def _create_default_habits(self) -> List[Habit]:
        now = datetime.now()

        def generate_dates(period_days, count):
            return [
                (now - timedelta(days=period_days * i)).isoformat()
                for i in range(count)
            ]
        return [
            Habit("Take a nap",
                  "Nap for an hour",
                  "daily",
                  created_at=now,
                  completions=[]),

            Habit("Exercise",
                  "Go to the gym",
                  "weekly",
                  created_at=now,
                  completions=[]),

            Habit("Read a book",
                  "Read 10 pages",
                  "daily",
                  created_at=now,
                  completions=[]),

            Habit("Call parents",
                  "Weekly call",
                  "weekly",
                  created_at=now,
                  completions=[]),

            Habit("Clean room",
                  "Weekly cleanup",
                  "weekly",
                  created_at=now,
                  completions=[]),
        ]




