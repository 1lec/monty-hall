VALID_MAIN_MENU_INPUTS = ['1', '2', '3', '4', '5', 'PLAY']
name = ""

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

def main():
    while True:
        print(MAIN_MENU_TEXT)
        main_menu_choice = None
        while main_menu_choice not in VALID_MAIN_MENU_INPUTS:
            main_menu_choice = input(MAIN_MENU_PROMPT)

        if main_menu_choice == '1':
            print("About the Monty Hall Game")
            input("Press enter to return to the main menu.")

        if main_menu_choice == '2' or main_menu_choice == 'PLAY':
            print(DOOR_TEXT)
            door_choice = input(DOOR_PROMPT)

        if main_menu_choice == '3':
            name_confirmation = None
            while name_confirmation != '1':
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

        if main_menu_choice == '4':
            print('Statistics')
            input("Press enter to return to the main menu.")

        if main_menu_choice == '5':
            return


if __name__ == "__main__":
    main()
