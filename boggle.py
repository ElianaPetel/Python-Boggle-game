##############################################################################
# FILE: boggle.py
# EXERCISE: Intro2cs ex11 2023-2024
# WRITER: LiorHaleli and ElianaPetel
# DESCRIPTION: Game runner for the boggle game
##############################################################################


from boogle_gui import BoggleGui
from boggle_menu import BoggleMenu


class BoggleGame:
    """BoggleGame class responsible to connect all the external elements
    to a complete boggle game !"""

    def __init__(self):
        self.boggle_gui = None  # initialize to None

    def start(self):
        # starts the boggle game
        self.boggle_gui = BoggleGui()
        self.boggle_gui.set_title("Boggle Game")
        self.boggle_gui.run()


if __name__ == "__main__":
    boggle_game = BoggleGame()
    # passing the start method to the boggle menu
    # for starting the game window
    boggle_menu = BoggleMenu(boggle_game.start)
    boggle_menu.run()
