import pydoc
import zmq

VALID_MAIN_MENU_INPUTS = ['1', '2', '3', '4', '5', 'PLAY']

MAIN_MENU_TEXT = """Welcome to the Monty Hall Game Simulator!
Type PLAY and press enter to start a game, or using your keyboard,
enter a number to select an option from the menu below.

-----------------------------------------------------------
Main Menu
-----------------------------------------------------------
[1] About the Monty Hall Game
[2] Start Game
[3] Name Selection
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

VALID_DOOR_INPUTS = ['1', '2', '3', '4']
DOOR_MENU = """
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

VALID_NAME_MENU_INPUTS = ['1', '2', '3']
NAME_SELECTION_TEXT = """
Choosing a name is not a requirement to play the Monty Hall Game, but it's easy to do,
and lets you save your game results to be viewed later under the "Statistics" menu option.
"""
NO_NAME_SELECTED = "You are not currently playing under a name. Your results will not be saved."
YES_NAME_SELECTED = "You are currently playing under a name: "
NAME_SELECTION_MENU = """
-----------------------------------------------------------
Name Selection
-----------------------------------------------------------
[1] Choose a Name
[2] Erase Name
[3] Main Menu
-----------------------------------------------------------
"""
NAME_MENU_PROMPT = "Enter menu option: "
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

class MontyHall:
    """Represents a game of Monty Hall."""
    def __init__(self, prng_port, msg_port):
        self.name = ""
        self.context = zmq.Context()
        self.prng_socket = self.prng_connect(prng_port)
        self.msg_socket = self.prng_connect(msg_port)

    def prng_connect(self, prng_port):
        """Receives a port number and forms a ZeroMQ connection through the port."""
        prng_socket = self.context.socket(zmq.REQ)
        prng_socket.connect(f"tcp://localhost:{prng_port}")
        return prng_socket
    
    def msg_connect(self, msg_port):
        """Receives a port number and forms a ZeroMQ connection through the port."""
        msg_socket = self.context.socket(zmq.REQ)
        msg_socket.connect(f"tcp://localhost:{msg_port}")
        return msg_socket

    def play(self):
        """This method runs when the user selects option 3 from the main menu."""
        doors = ['1', '2', '3']
        # Randomly place prize behind a door
        self.prng_socket.send_json({"type": "single", "N": 3})
        prize = str(self.prng_socket.recv_json().get("random_number"))

        door_choice = self.get_door_menu_selection()

        if door_choice != '4':
            if prize == door_choice:
                exclusion_request = {"type": "excluded", "N": 3, "X": int(prize)}
                self.prng_socket.send_json(exclusion_request)
                revealed = str(self.prng_socket.recv_json().get("random_number"))
            else:
                for door in doors:
                    if door != prize and door != door_choice:
                        revealed = door
            doors.remove(revealed)
            for door in doors:
                if door != door_choice:
                    unselected_door = door
            final_selection = self.get_final_door_selection(door_choice, unselected_door, revealed)
            if final_selection == prize:
                self.msg_socket.send_string("W")
            else:
                self.msg_socket.send_string("L")
            result = self.msg_socket.recv().decode()
            print(f"""
Initial Selection: {door_choice}
Prize: {prize}
Revealed: {revealed}
Unselected Door: {unselected_door}
Final Choice: {final_selection}
""")
            print(result + '\n')

    def name_selection(self):
        """This method runs when the user selects option 3 from the main menu."""
        name_menu_choice = self.get_name_menu_selection()

        # Choose a Name
        if name_menu_choice == '1':
            while True:
                self.name = input(NAME_SELECTION_PROMPT).strip()
                if self.name == "":
                    print(NAME_NOT_ENTERED_TEXT)
                else:
                    print(f"You entered the name {self.name}.")
                print(NAME_CONFIRMATION_MENU)
                name_confirmation = input(NAME_CONFIRMATION_PROMPT)
                while name_confirmation != '1' and name_confirmation != '2':
                    name_confirmation = input(NAME_CONFIRMATION_PROMPT)
                if name_confirmation == '1':
                    break
        
        # Erase Name
        if name_menu_choice == '2':
            self.name = ""

    def statistics(self):
        """This method runs when the user selects option 4 from the main menu."""
        stats_choice = self.get_statistics_menu_selection()
        if stats_choice == '1':
            print("Print name entry")
        if stats_choice == '2':
            print("leaderboard")

    def get_main_menu_selection(self):
        """Prints the main menu and prompts the user for a selection."""
        print(MAIN_MENU_TEXT)
        main_menu_choice = input(MAIN_MENU_PROMPT)
        while main_menu_choice not in VALID_MAIN_MENU_INPUTS:
            main_menu_choice = input(MAIN_MENU_PROMPT)
        return main_menu_choice

    def get_door_menu_selection(self):
        """Prints the door menu and prompts the user for a selection."""
        print(DOOR_MENU)
        door_choice = input(DOOR_PROMPT)
        while door_choice not in VALID_DOOR_INPUTS:
            door_choice = input(DOOR_PROMPT)
        return door_choice

    def get_name_menu_selection(self):
        """Prints the name menu and prompts the user for a selection."""
        print(NAME_SELECTION_TEXT)
        if self.name:
            print(YES_NAME_SELECTED + self.name)
        else:
            print(NO_NAME_SELECTED)
        print(NAME_SELECTION_MENU)

        name_menu_choice = input(NAME_MENU_PROMPT)
        while name_menu_choice not in VALID_NAME_MENU_INPUTS:
            name_menu_choice = input(NAME_MENU_PROMPT)
        return name_menu_choice

    def get_statistics_menu_selection(self):
        """Prints the statistics menu and prompts the user for a selection."""
        print(STATISTICS_MENU_TEXT)
        stats_choice = input(STATISTICS_PROMPT)
        while stats_choice not in VALID_STATISTICS_MENU_INPUTS:
            stats_choice = input(STATISTICS_PROMPT)
        return stats_choice

    def get_final_door_selection(self, selected_door, unselected_door, revealed):
        """Receives information about the status of each door, prompts the user if they would like to stay
        with their original choice or not, and returns the user's final door selection."""
        final_door_menu = f"""
    Door {revealed} has a goat behind it!

    You originally selected Door {selected_door}, but {unselected_door} is still available.
    Do you want to stay with your first choice, or switch to the other door?

    -----------------------------------------------------------
    Stay or Switch?
    -----------------------------------------------------------
    [STAY]   Stay with Door {selected_door}
    [SWITCH] Switch to Door {unselected_door}
    -----------------------------------------------------------
    """
        print(final_door_menu)
        final_selection = input("Enter STAY or SWTICH: ")
        while final_selection not in ['STAY', 'SWITCH']:
            final_selection = input("Enter STAY or SWTICH: ")
        
        if final_selection == 'STAY':
            return selected_door
        else:
            return unselected_door


    def main_menu(self):
        while True:
            main_menu_choice = self.get_main_menu_selection()

            # About
            if main_menu_choice == '1':
                pydoc.pager(ABOUT_MONTY_HALL_TEXT)

            # Play
            if main_menu_choice == '2' or main_menu_choice == 'PLAY':
                self.play()

            # Name Selection
            if main_menu_choice == '3':
                self.name_selection()

            # Statistics
            if main_menu_choice == '4':
                self.statistics()

            # Exit Program
            if main_menu_choice == '5':
                return


if __name__ == "__main__":
    game = MontyHall('5555', '5556')
    game.main_menu()
