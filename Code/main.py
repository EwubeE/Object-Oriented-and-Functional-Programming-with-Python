
from colorama import Fore, init
from tabulate import tabulate

from habit_manager import HabitManager
from analytics import total_habits, get_longest_streak_all, get_habit_summary, get_habits_by_periodicity,most_completed_habit,count_by_periodicity
init(autoreset=True)


#Creates an instance of your habit manager
manager = HabitManager()


# Display all habits in a table
def display_habits(habits):
    table = [[habit.name, habit.periodicity,
                 ]
                 for habit in habits]
    headers = ["Habit Name",
               "Periodicity"]
    print(tabulate(table, headers=headers, tablefmt="grid"))


# Display habit analysis in a table
def display_analysis(summary):
    table = [
        [habit["name"],
             habit["description"],
             habit["periodicity"],
             habit["current_streak"],
             habit["longest_streak"],
             habit["total_completions"],
             habit["created_at"]
        ]
        for habit in summary
    ]
    headers = [
        "Habit Name",
        "Description",
        "Periodicity",
        "Current Streak",
        "Longest Streak",
        "Total Completions",
        "Created On"
    ]

    print(tabulate(table, headers=headers, tablefmt="grid"))


# Displays the main menu to the user
def main():
    while True:
        print(Fore.WHITE +"=== Welcome to the Habit Tracker===")
        print(Fore.GREEN +"1. Add habit")
        print(Fore.GREEN +"2. Update habit")
        print(Fore.GREEN +"3. Checklist")
        print(Fore.GREEN +"4. View habits")
        print(Fore.GREEN +"5. Analyze habits")
        print(Fore.GREEN +"6. Delete habit")
        print(Fore.RED +"7. Exit")

        choice = input(Fore.YELLOW +"\nEnter your choice: ")

        if choice == '1':
            name = input("Habit name: ").strip()
            description = input("Description: ").strip()
            periodicity = input("Periodicity (daily/weekly): ").strip().lower()

            try:
                manager.add_habit(name=name, description=description, periodicity=periodicity)
                print(Fore.YELLOW + "Habit added successfully!")

            except ValueError as e:
                print(Fore.RED + str(e))

        elif choice == '2':
            old_name = input("Enter current habit name: ")
            new_name = input("Enter new habit name: ")
            new_description = input("Enter new habit description: ")
            new_periodicity = input("Enter new habit periodicity (daily/weekly): ")
            try:
                if  manager.update_habit(old_name, new_name, new_description, new_periodicity):
                    print(Fore.YELLOW +"Habit updated successfully!")
                else:
                    print(Fore.RED+"Habit not found")

            except ValueError as e:
                print(Fore.RED + str(e))

        elif choice == '3':
            name = input("Enter habit name to mark complete: ")
            try:
                if manager.complete_habit(name):
                    print(Fore.GREEN + "Habit marked complete!")
                else:
                    print(Fore.RED + "Habit not found.")
            except ValueError as e:
                print(Fore.RED + str(e))

        elif choice == '4':
            habits = manager.get_all_habits()
            if not habits:
                print(Fore.RED +"No habits found")
            else:
                print(Fore.GREEN +"===Your habits===")
                display_habits(habits)

        elif choice == '5':
            habits = manager.get_all_habits()
            summary = get_habit_summary(habits)

            print(Fore.WHITE +"\n===Habits Analysis===")
            display_analysis(summary)

            print(Fore.GREEN + f"Total Habits:", (total_habits(habits)))
            print(Fore.GREEN + f"Longest Streak:",(get_longest_streak_all(habits)))

            most_habit = most_completed_habit(manager.habits)

            if most_habit:
                names = ", ".join(habit.name for habit in most_habit)
                print(Fore.GREEN + f"Most completed habit:", names)
            else:
                print(Fore.GREEN + "Most completed habit:",  "None")

            daily = get_habits_by_periodicity(habits, "daily")
            weekly = get_habits_by_periodicity(habits, "weekly")
            print(Fore.GREEN +"Daily habits:", len (daily))
            print(Fore.GREEN +"Weekly habits:", len (weekly))




        elif choice == '6':
            name_to_delete = input("Enter habit name to delete: ").strip()

            try:
                if manager.delete_habit(name_to_delete):
                    print(Fore.YELLOW + "Habit Deleted Successfully!")
                else:
                    print(Fore.RED + "Habit Not found")
            except ValueError as e:
                print(Fore.RED + str(e))

        elif choice == '7':
            print (Fore.GREEN +"Goodbye and have a nice day")

            break
        else:
            print(Fore.RED +"Invalid choice. Please try again")

# Start the application
if __name__ == '__main__':
    main()