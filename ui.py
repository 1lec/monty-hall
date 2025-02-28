import pydoc
import zmq
import textwrap

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
VALID_MAIN_MENU_INPUTS = ['1', '2', '3', '4', '5', 'PLAY']

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
VALID_DOOR_INPUTS = ['1', '2', '3', '4']

NAME_SELECTION_TEXT = """
Choosing a name is not a requirement to play the Monty Hall Game, but it's easy to do,
and lets you save your game results to be viewed later under the "Statistics" menu option.
"""
NO_NAME_SELECTED = "You are not currently playing under a name. Your results will not be saved."
YES_NAME_SELECTED = "You are currently playing under a name: "

NAME_MENU_TEXT = """
-----------------------------------------------------------
Name Selection
-----------------------------------------------------------
[1] Choose a Name
[2] Erase Name
[3] Main Menu
-----------------------------------------------------------
"""
NAME_MENU_PROMPT = "Enter menu option: "
VALID_NAME_MENU_INPUTS = ['1', '2', '3']

NAME_ENTRY_PROMPT = "Enter a name: "
NAME_NOT_ENTERED_TEXT = "You did not enter a name. You can play without a name, but your game results will not be saved."

NAME_CONFIRM_MENU_TEXT = """
-----------------------------------------------------------
Confirm your Name Selection
-----------------------------------------------------------
[1] Yes
[2] No
-----------------------------------------------------------
"""
NAME_CONFIRM_PROMPT = "Confirm name? "
VALID_NAME_CONFIRM_INPUTS = ['1', '2']

STATS_MENU_TEXT = """
Use the menu below to view statistics regarding the Monty Hall Game.

-----------------------------------------------------------
Statistics Menu
-----------------------------------------------------------
[1] Winning Percentage
[2] Leaderboard
[3] Clear Statistics for a Name
[4] Clear All Statistics
[5] Main Menu
-----------------------------------------------------------
"""
STATS_PROMPT = "Enter menu option: "
VALID_STATS_MENU_INPUTS = ['1', '2', '3', '4', '5']

DELETE_CONFIRM_MENU_TEXT = """
WARNING - This action cannot be undone.

-----------------------------------------------------------
Confirm Deletion
-----------------------------------------------------------
[1] Yes
[2] No
-----------------------------------------------------------
"""
DELETE_CONFIRM_PROMPT = "Confirm deletion: "
VALID_DELETE_CONFIRM_INPUTS = ['1', '2']


class Menu:
    """Represents a menu."""
    def __init__(self, title, text, prompt, valid_inputs):
        self.title = title
        self.text = text
        self.prompt = prompt
        self.valid_inputs = valid_inputs


class MontyHall:
    """Represents a game of Monty Hall."""
    def __init__(self, prng_port, msg_port, db_port):
        self.name = ""
        self.context = zmq.Context()
        self.prng_socket = self.prng_connect(prng_port)
        self.msg_socket = self.prng_connect(msg_port)
        self.db_socket = self.prng_connect(db_port)
        self.menus = {
            "main": Menu("main", MAIN_MENU_TEXT, MAIN_MENU_PROMPT, VALID_MAIN_MENU_INPUTS),
            "door": Menu("door", DOOR_MENU, DOOR_PROMPT, VALID_DOOR_INPUTS),
            "name": Menu("name", NAME_MENU_TEXT, NAME_MENU_PROMPT, VALID_NAME_MENU_INPUTS),
            "name_confirm": Menu("name_confirm", NAME_CONFIRM_MENU_TEXT, NAME_CONFIRM_PROMPT, VALID_NAME_CONFIRM_INPUTS),
            "stats": Menu("stats", STATS_MENU_TEXT, STATS_PROMPT, VALID_STATS_MENU_INPUTS),
            "delete": Menu("delete", DELETE_CONFIRM_MENU_TEXT, DELETE_CONFIRM_PROMPT, VALID_DELETE_CONFIRM_INPUTS)
        }

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

    def db_connect(self, db_port):
        """Receives a port number and forms a ZeroMQ connection through the port."""
        msg_socket = self.context.socket(zmq.REQ)
        msg_socket.connect(f"tcp://localhost:{db_port}")
        return msg_socket
    
    def get_prn(self, exclude=None):
        """Returns a pseudorandom number in the range 1 to 3, inclusive. If the exclude parameter
        is provided, that number cannot be returned."""
        # Returns a number 1 to 3 inclusive, excluding the number in the exclude parameter
        if exclude:
            exclusion_request = {"type": "excluded", "N": 3, "X": int(exclude)}
            self.prng_socket.send_json(exclusion_request)
            return str(self.prng_socket.recv_json().get("random_number"))
        # Returns a number 1 to 3 inclusive
        self.prng_socket.send_json({"type": "single", "N": 3})
        return str(self.prng_socket.recv_json().get("random_number"))
    
    def main_menu(self):
        while True:
            main_menu_choice = self.get_menu_selection(self.menus["main"])

            # About
            if main_menu_choice == '1':
                pydoc.pager(ABOUT_MONTY_HALL_TEXT)

            # Play
            if main_menu_choice in ['2', 'PLAY']:
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
        
    def play(self):
        """This method runs when the user selects option 3 from the main menu."""
        doors = ['1', '2', '3']
        prize = self.get_prn()
        door_choice = self.get_menu_selection(self.menus["door"])

        if door_choice in doors:
            if prize == door_choice:
                revealed = self.get_prn(prize)
            else:
                for door in doors:
                    if door != prize and door != door_choice:
                        revealed = door
            doors.remove(revealed)
            for door in doors:
                if door != door_choice:
                    unselected_door = door
            final_selection = self.get_final_door_selection(door_choice, unselected_door, revealed)
            self.determine_result(final_selection, prize)

    def name_selection(self):
        """This method runs when the user selects option 3 from the main menu."""
        name_menu_choice = self.get_menu_selection(self.menus["name"])

        # Choose a Name
        if name_menu_choice == '1':
            while True:
                self.name = input(NAME_ENTRY_PROMPT).strip()
                if self.name == "":
                    print(NAME_NOT_ENTERED_TEXT)
                else:
                    print(f"You entered the name {self.name}.")
                name_confirm = self.get_menu_selection(self.menus["name_confirm"])
                if name_confirm == '1':
                    break
        
        # Erase Name
        if name_menu_choice == '2':
            self.name = ""

        # Main Menu
        if name_menu_choice == '3':
            return
        
        # Repeat Name Selection Menu
        self.name_selection()

    def statistics(self):
        """This method runs when the user selects option 4 from the main menu."""
        stats_choice = self.get_menu_selection(self.menus["stats"])
        if stats_choice == '1':
            print("View Winning Percentage")
        if stats_choice == '2':
            print("View Leaderboard")
        if stats_choice == '3':
            name_to_delete = input("Enter a name to be cleared: ")
            while not name_to_delete:
                name_to_delete = input("Enter a name to be cleared: ")
            confirmation = self.get_menu_selection(self.menus["delete"], name_to_delete)
            if confirmation == '1':
                self.db_socket.send_json({"type": "delete", "name": name_to_delete})
                print(self.db_socket.recv().decode())

        if stats_choice == '4':
            print("Clear All Statistics")
        if stats_choice == '5':
            return
        
        self.statistics()

    def get_menu_selection(self, menu, name_to_delete=None):
        """Receives a menu object, prompts the user for valid input, and returns the user's selection.
        """
        if menu.title == "name":
            print(NAME_SELECTION_TEXT)
            if self.name:
                print(YES_NAME_SELECTED + self.name)
            else:
                print(NO_NAME_SELECTED)

        if menu.title == "delete":
            print(f"You are requesting to delete all records of the name {name_to_delete}.")

        print(menu.text)
        menu_choice = input(menu.prompt)
        while menu_choice not in menu.valid_inputs:
            menu_choice = input(menu.prompt)
        return menu_choice

    def get_final_door_selection(self, selected_door, unselected_door, revealed):
        """Receives information about the status of each door, prompts the user if they would like to stay
        with their original choice or not, and returns the user's final door selection."""

        final_door_menu_text = textwrap.dedent(f"""
        Door {revealed} has a goat behind it!

        You originally selected Door {selected_door}, but {unselected_door} is still available.
        Do you want to stay with your first choice, or switch to the other door?

        -----------------------------------------------------------
        Stay or Switch?
        -----------------------------------------------------------
        [STAY]   Stay with Door {selected_door}
        [SWITCH] Switch to Door {unselected_door}
        -----------------------------------------------------------
        """)
        final_door_menu = Menu("door", final_door_menu_text, "Enter STAY or SWTICH: ", ['STAY', 'SWITCH'])
        final_selection = self.get_menu_selection(final_door_menu)
        
        if final_selection == 'STAY':
            return selected_door
        else:
            return unselected_door
        
    def determine_result(self, final_selection, prize):
        """Receives the user's final door selection and the prize location to determines the game result. Prints a
        random congratulatory/failure message depending on the result, and if the user is playing under a name,
        saves the game result to a database."""
        if final_selection == prize:
            self.msg_socket.send_string("W")
            if self.name:
                self.db_socket.send_json({"type": "game", "name": self.name, "result": 1})
        else:
            self.msg_socket.send_string("L")
            if self.name:
                self.db_socket.send_json({"type": "game", "name": self.name, "result": 0})

        result_message = self.msg_socket.recv().decode()
        if self.name:
            db_message = self.db_socket.recv_string()
        else:
            db_message = "Game result was not saved. Play under a name to save results."
        print(result_message)
        print(db_message + '\n')


if __name__ == "__main__":
    game = MontyHall('5555', '5556', '5557')
    game.main_menu()
