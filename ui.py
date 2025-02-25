import pydoc

VALID_MAIN_MENU_INPUTS = ['1', '2', '3', '4', '5', 'PLAY']

MAIN_MENU_TEXT = """Welcome to the Monty Hall Game Simulator!
Type PLAY and press enter to start a game, or using your keyboard,
enter a number to select an option from the menu below.

-----------------------------------------------------------
Main Menu
-----------------------------------------------------------
[1] About the Monty Hall Game
[2] Start Game
[3] Enter Name
[4] Statistics
[5] Exit
-----------------------------------------------------------
"""
MAIN_MENU_PROMPT = "Type PLAY or enter a menu option: "

ABOUT_MONTY_HALL_TEXT = """
                                About the Monty Hall Game

The Monty Hall Game is a probability game based off the Monty Hall Problem, which itself originates
from the game show Let's Make a Deal, hosted by Monty Hall. The show first aired in 1963 and features
a series of minigames. One of these minigames is the basis of this program.

During our minigame, the host Monty Hall presents three doors to a contestant. He states that while
one door has a prize (oftentimes a car) behind it, the other two doors have nothing but goats! After
the contestant selects a door, the host, who knows the contents of each door, reveals one of the two
goats behind a door the contestant did not choose.

With only two doors remaining, one with a prize and another with a goat, Monty Hall poses another
question to the contestant: Would you like to stick with your door, or switch to the other?

Press 'q' to return to the main main.
"""

DOOR_TEXT = """
Before you stand three doors, but only one has a prize behind it!

-----------------------------------------------------------
Choose a Door!
-----------------------------------------------------------
[1] Door 1
[2] Door 2
[3] Door 3
[4] Quit Game (Return to Main Menu)
-----------------------------------------------------------
"""
DOOR_PROMPT = "Enter menu option: "

NAME_SELECTION_TEXT = """
Choosing a name is not a requirement to play the Monty Hall Game, but it's easy to do,
and allows you to save your results to be viewed later under the "Statistics" menu option.

If you do not wish to save your results, hit enter without typing a name.
"""
NAME_SELECTION_PROMPT = "Enter a name: "
NAME_NOT_ENTERED_TEXT = "You did not enter a name. You can play without a name, but your game results will not be saved."
NAME_CONFIRMATION_MENU = """
-----------------------------------------------------------
Confirm your Name Selection
-----------------------------------------------------------
[1] Yes
[2] No
-----------------------------------------------------------
"""
NAME_CONFIRMATION_PROMPT = "Confirm name? "

VALID_STATISTICS_MENU_INPUTS = ['1', '2', '3']
STATISTICS_MENU_TEXT = """
Use the menu below to view statistics regarding the Monty Hall Game.

-----------------------------------------------------------
Statistics Menu
-----------------------------------------------------------
[1] Winning Percentage
[2] Leaderboard
[3] Main Menu
-----------------------------------------------------------
"""
STATISTICS_PROMPT = "Enter menu option: "

def main():
    name = ""
    while True:
        print(MAIN_MENU_TEXT)
        main_menu_choice = None
        while main_menu_choice not in VALID_MAIN_MENU_INPUTS:
            main_menu_choice = input(MAIN_MENU_PROMPT)

        if main_menu_choice == '1':
            pydoc.pager(ABOUT_MONTY_HALL_TEXT)

        if main_menu_choice == '2' or main_menu_choice == 'PLAY':
            print(DOOR_TEXT)
            door_choice = input(DOOR_PROMPT)

        if main_menu_choice == '3':
            while True:
                print(NAME_SELECTION_TEXT)
                name = input(NAME_SELECTION_PROMPT).strip()
                if name == "":
                    print(NAME_NOT_ENTERED_TEXT)
                else:
                    print(f"You entered the name {name}.")
                print(NAME_CONFIRMATION_MENU)
                name_confirmation = None
                while name_confirmation != '1' and name_confirmation != '2':
                    name_confirmation = input(NAME_CONFIRMATION_PROMPT)
                if name_confirmation == '1':
                    break

        if main_menu_choice == '4':
            print(STATISTICS_MENU_TEXT)
            stats_choice = input(STATISTICS_PROMPT)
            while stats_choice not in VALID_STATISTICS_MENU_INPUTS:
                stats_choice = input(STATISTICS_PROMPT)
            if stats_choice == '1':
                print("Print name entry")
            if stats_choice == '2':
                print("leaderboard")

        if main_menu_choice == '5':
            return


if __name__ == "__main__":
    main()
