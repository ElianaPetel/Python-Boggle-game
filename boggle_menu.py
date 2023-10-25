##############################################################################
# FILE: boggle_menu.py
# EXERCISE: Intro2cs ex11 2023-2024
# WRITER: LiorHaleli and ElianaPetel
# DESCRIPTION: File that creates the homepage for the game.
##############################################################################

import tkinter as tk
import ex11_utils


class BoggleMenu:
    """Generates the homepage menu for strating the boggle game."""

    def __init__(self, start_callback):
        self.start_call = start_callback
        self.window = tk.Tk()
        # set window size
        self.screen_width = self.window.winfo_screenwidth() // 2
        self.screen_height = self.window.winfo_screenheight() // 2
        self.window.minsize(
            height=self.screen_height + 200, width=self.screen_width + 400
        )
        self.window.title("BOGGLE GAME")
        self.window.config(background=ex11_utils.VERY_LIGHT_GREEN)
        # Add background image
        self.bg_img = tk.PhotoImage(file="media/images/bi.png")
        bg_label = tk.Label(self.window, image=self.bg_img)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.complete_text = "Welcome to the Python Boggle Game!"
        self.incomplete_text = ""
        self.index = 0
        self.title_label = tk.Label(
            self.window,
            text="Welcome to the Python Boggle Game!",
            font=("Comic Sans MS", 30),
            padx=40,
            pady=25,
            fg=ex11_utils.VERY_DARK_GREEN,
            bg=ex11_utils.VERY_LIGHT_GREEN,
        )
        self.title_label.pack(pady=100)

        self.play_button = tk.Button(
            self.window,
            text="Start playing",
            font=("Comic Sans MS", 18),
            relief="raised",
            fg=ex11_utils.VERY_LIGHT_GREEN,
            bg=ex11_utils.VERY_DARK_GREEN,
            activebackground=ex11_utils.DARK_GREEN,  # Slightly darker green on click
            command=self.start_game_and_close_menu,
        )

        self.instructions_button = tk.Button(
            self.window,
            text="To instructions",
            font=("Comic Sans MS", 18),
            relief="raised",
            fg=ex11_utils.VERY_DARK_GREEN,
            bg=ex11_utils.LIGHT_YELLOW,
            activebackground=ex11_utils.DARKER_YELLOW,
            activeforeground=ex11_utils.VERY_DARK_GREEN,
            command=self.display_instructions,
        )
        # changes the window icone to boggle icone
        self.img = tk.PhotoImage(file="./media/images/boggle_icon.png")
        self.window.iconphoto(True, self.img)
        self.animation_running = True
        self.after_id = None

    def typing_title(self):
        """Creates a typing effect on the welcoming sentence"""
        if not self.animation_running:
            return
        if self.index >= len(self.complete_text):
            self.title_label.config(text=self.incomplete_text)
        else:
            self.incomplete_text = self.incomplete_text + self.complete_text[self.index]
            self.title_label.config(text=self.incomplete_text)
            self.index += 1
            # storing the after id
            self.after_id = self.title_label.after(80, self.typing_title)

    def display_instructions(self):
        """Creates a new frame for explaining the rules of the game"""
        self.play_button.pack_forget()

        instructions_frame = tk.Frame(
            self.window,
            bg=ex11_utils.VERY_LIGHT_GREEN,
            relief=tk.RAISED,  # Raised border style
        )
        instructions_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        instructions_label = tk.Label(
            instructions_frame,
            text="Boggle is a word-making game that requires exceptional vocabulary. \n You will have 3 minutes to create as many words as possible from the few letters on the board. \n Make sure the words you find are longer than 3 letters. \n The longer your words, the higher your score!",
            font=("Comic Sans MS", 14),
            fg=ex11_utils.VERY_DARK_GREEN,
            bg=ex11_utils.VERY_LIGHT_GREEN,
        )
        instructions_label.pack(pady=20, padx=20)

        after_instructions_play_button = tk.Button(
            instructions_frame,
            text="Start playing",
            font=("Comic Sans MS", 14),
            relief="raised",
            fg=ex11_utils.VERY_LIGHT_GREEN,
            bg=ex11_utils.VERY_DARK_GREEN,
            activebackground=ex11_utils.INTER_LIGHT,
            activeforeground=ex11_utils.VERY_DARK_GREEN,
            command=self.start_game_and_close_menu,
        )
        after_instructions_play_button.pack(pady=10)

    def run(self):
        """Display the homepage menu"""
        self.typing_title()
        self.instructions_button.pack(pady=15)
        self.play_button.pack()
        self.window.mainloop()

    def start_game_and_close_menu(self):
        """Start the game"""
        self.animation_running = False  # stopping animation
        if self.after_id is not None:
            self.title_label.after_cancel(self.after_id)  # canceling animation
        self.window.destroy()  # close the menu window
        self.start_call()  # start the game
