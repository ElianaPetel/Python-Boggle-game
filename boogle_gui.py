##############################################################################
# FILE: boggle_gui.py
# EXERCISE: Intro2cs ex11 2023-2024
# WRITER: LiorHaleli and ElianaPetel
# DESCRIPTION: File that creates the user interface.
##############################################################################

from tkinter import *
from boggle_board_randomizer import *
import ex11_utils
from tkinter import simpledialog

with open("boggle_dict.txt", "r") as f:
    DICT_BOGGLE = {line.strip() for line in f}


class BoggleGui:
    """boggle gui class builds all the visuals elements needed
    to have user-friendly graphical interface"""

    def __init__(self):
        self._init_variables()
        self._init_home_page()

    def _init_home_page(self):
        self._root = Tk()
        # set window size
        self.screen_width = self._root.winfo_screenwidth() // 2
        self.screen_height = self._root.winfo_screenheight() // 2
        self._root.minsize(
            height=self.screen_height + 200, width=self.screen_width + 400
        )
        self.board = randomize_board()
        self.board_size = len(self.board)

        self.set_top_frame()
        self.set_main_screen()
        self.setup_start_screen()

    def _init_variables(self):
        self._score = 0
        self.remaining_time = 180  # 3 minutes in seconds
        self.selected_letters = []
        self.selected_buttons = []
        self.words_found = []  # valid words that the user found
        self.words_tried = []  # words that the user tried (non-valid\not in dict)
        self._dictionary = DICT_BOGGLE
        # when building an instance, the game doesn't start immediately
        self.game_started = False

    def setup_start_screen(self):
        # start button
        self.start_button = Button(
            self.center_main,
            text="START PLAYING",
            font=("Comic Sans MS", 12, "bold"),
            bg=ex11_utils.DARK_GREEN,
            fg=ex11_utils.VERY_LIGHT_GREEN,
            relief="sunken",
            padx=10,
            pady=10,
            command=self.start_game,
        )
        self.start_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    def start_game(self):
        # removing the start button
        self.start_button.destroy()
        # deleting found_words and tried words list
        self.found_words.delete("1.0", "end")
        self.tried_words.delete("1.0", "end")

        # activating the game board and widgets
        self.set_board_frame()
        self.game_started = True
        self.update_timer()  # starting the watch
        self.draw_timer_arc(40, 40, 35, 0, 360, ex11_utils.INTER_LIGHT)

    def reset_game(self):
        # restarting game if we in the middle
        if self.game_started:
            # destroy the game board frame and its contents
            self.board_frame.destroy()
            self.words_format.config(text="")
            self.display_game_results()  # show player his results
            self._init_variables()
            # deleting found_words and tried words list
            self.found_words.config(state="normal")
            self.tried_words.config(state="normal")

            self.found_words.delete("1.0", "end")
            self.tried_words.delete("1.0", "end")
            self.found_words.config(state="disabled")
            self.tried_words.config(state="disabled")
            # creating new board
            self.board = randomize_board()
            # formatting points label back to 0
            self.points_score.config(text=0)
            # showing start button once again and changing game started to false
            self.setup_start_screen()
            self.game_started = False

    def on_button_click(self, event):
        # each button in the board is bind to <button-1>
        button = event.widget

        # check if the button is already selected or not neighboring
        if not self.is_neighbor(button):
            return
        # checking if useer selected same button twice in a row
        if button in self.selected_buttons:
            if self.selected_buttons and self.selected_buttons[-1] == button:
                # if true, remove it
                last_button = self.selected_buttons.pop()
                last_button["state"] = "normal"
                last_button["bg"] = ex11_utils.VERY_LIGHT_GREEN
            else:
                return

        else:
            # if user selected neighbor button, disable it and change color
            self.selected_buttons.append(button)
            button["state"] = "disabled"
            button["bg"] = ex11_utils.LIGHT_GREEN

        # update words format label text and colors
        self.update_words_format()
        self.update_button_colors()

    def is_neighbor(self, button):
        #  check if the button is a neighbor of the last selected button
        if not self.selected_buttons:
            return True  # user can select any button at the start

        last_button = self.selected_buttons[-1]
        last_row, last_col = (
            last_button.grid_info()["row"],
            last_button.grid_info()["column"],
        )
        row, col = button.grid_info()["row"], button.grid_info()["column"]
        # return true if last button and current button row and col
        # is 1 or less (which mean they are neighbors), false otherwise
        return abs(row - last_row) <= 1 and abs(col - last_col) <= 1

    def update_button_colors(self):
        # updates colors of buttons each time the user pressed
        # a button in the board. (buttons are stored in a 2d list)
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[row][col]
                if button in self.selected_buttons:
                    button["bg"] = ex11_utils.LIGHT_GREEN
                elif self.is_neighbor(button):
                    button["bg"] = ex11_utils.VERY_LIGHT_GREEN
                else:
                    button["bg"] = ex11_utils.INTER_LIGHT

    def reset_buttons(self):
        # for each button in the board, change it back to a default values
        for row in range(self.board_size):
            for col in range(self.board_size):
                button = self.buttons[row][col]
                button["state"] = "normal"
                button["bg"] = "white"
        # resetting the selected buttons the user pressed
        self.selected_buttons = []

    def reset_board(self):
        """run when user clicked the check button.
        clears board and checks the word created"""
        if self.game_started:
            if len(self.words_format.cget("text")) < 3:
                self.status_label.config(text="Words must be at least 3 letters long.")
                self._root.after(
                    3000, lambda: self.status_label.config(text="")
                )  # Clear message after 3 seconds
                return

            self.reset_buttons()
            # extraction of the word in the words_format label
            word = self.words_format.cget("text")
            self.found_words.tag_configure("custom_tag", font=("Comic Sans MS", 12))
            self.tried_words.tag_configure("custom_tag_try", font=("Comic Sans MS", 12))
            # if word in dict and was not already selected, add it to score and list
            if self.is_valid_word(word) and (word not in self.words_found):
                self.found_words.config(state="normal")
                self.found_words.insert(END, word, "custom_tag", "\n")
                self.words_found.append(word)
                self._score += len(word) ** 2
                self.points_score.config(text=self._score)
                self.found_words.config(state="disabled")
                # Show message in status label
                if len(word) <= 4:
                    self.status_label.config(
                        text=f"Congratulations! You've earned {len(word) ** 2} points for finding the word '{word}'."
                    )
                else:
                    self.status_label.config(
                        text=f"That was a hard one, good job! \n You've earned {len(word) ** 2} points for finding the word '{word}'."
                    )
                self._root.after(3000, lambda: self.status_label.config(text=""))

            # if word is not in tried words and length above 1, add to tried list
            elif word not in self.words_tried and len(word) >= 2:
                self.tried_words.config(state="normal")
                self.tried_words.insert(END, word, "custom_tag_try", "\n")
                self.words_tried.append(word)
                self.tried_words.config(state="disabled")

            # else: do nothing
            # clearing words format from any text
            self.words_format.config(text="")

    def update_words_format(self):
        # iterating over all the selected buttons and adding the letters
        # associated with each button to a variable word
        word = "".join(button.cget("text") for button in self.selected_buttons)
        self.words_format.config(text=word)

    def set_title(self, title):
        self._root.title(title)

    def run(self) -> None:
        self._root.mainloop()

    "main screen with all the widgets and accessories"

    def set_main_screen(self):
        """Create and display all fixed elements of the window"""
        self.center_main = Frame(self._root, bg=ex11_utils.LIGHT_GREEN)
        self.center_main.place(
            rely=ex11_utils.SPLIT,
            relx=0.25,
            relheight=(1 - ex11_utils.SPLIT - 0.15),
            relwidth=0.5,
        )
        self.status_label = Label(
            self.center_main,
            text="",
            font=("Comic Sans MS", 12, "bold"),
            bg=ex11_utils.LIGHT_GREEN,
            fg="#54278f",
            anchor="center",
        )
        self.status_label.pack(side=BOTTOM, fill=X)

        self.set_word_formation()
        self.set_check_word()

        self.left_frame = Frame(self._root, bg=ex11_utils.LIGHT_GREEN, padx=10, pady=10)
        self.left_frame.place(
            rely=ex11_utils.SPLIT,
            relx=0,
            relheight=(1 - ex11_utils.SPLIT - 0.15),
            relwidth=0.25,
        )

        self.right_frame = Frame(
            self._root, bg=ex11_utils.LIGHT_GREEN, padx=10, pady=10
        )
        self.right_frame.place(
            rely=ex11_utils.SPLIT,
            relx=0.75,
            relheight=(1 - ex11_utils.SPLIT - 0.15),
            relwidth=0.25,
        )

        self.bottom_frame = Frame(self._root, bg=ex11_utils.LIGHT_GREEN)
        self.bottom_frame.place(rely=0.85, relx=0, relwidth=1, relheight=1)
        self.set_bottom_buttons()

        self.set_time_widget()
        self.set_points_frame()
        self.set_words_tried()
        self.set_words_found()

    def set_check_word(self):
        # Create button for checking found words
        self.check_word = Button(
            self.center_main,
            text="CHECK",
            font=("Comic Sans MS", 10, "bold"),
            bg=ex11_utils.VERY_DARK_GREEN,
            fg=ex11_utils.VERY_LIGHT_GREEN,
            relief="sunken",
            command=self.reset_board,
        )

        self.check_word.place(relx=0.7, rely=0.03, relwidth=0.1, relheight=0.1)

    def is_valid_word(self, word):
        return word in self._dictionary

    def set_board_frame(self):
        # Create the boggle board
        self.board_frame = Frame(
            self.center_main,
            padx=10,
            pady=10,
            bg=ex11_utils.VERY_DARK_GREEN,
        )
        self.board_frame.pack(expand=True, pady=(40, 0))

        # saving each button of the board to a 2d list
        self.buttons = []
        for row in range(self.board_size):
            button_row = []
            for col in range(self.board_size):
                letter = self.board[row][col]
                button = Button(
                    self.board_frame,
                    text=letter,
                    font=("Comic Sans MS", 16),
                    fg=ex11_utils.VERY_DARK_GREEN,
                    relief="raised",
                    width=3,
                    height=1,
                )
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    ipadx=12,
                    ipady=6,
                )
                button.bind("<Button-1>", self.on_button_click)
                button["state"] = "normal"
                button["disabledforeground"] = "black"
                button_row.append(button)
            self.buttons.append(button_row)

    def find_words_of_length_n(self):
        if self.game_started:
            self.reset_buttons()
            self.words_format.config(text="")
            n = simpledialog.askinteger(
                "Find word of certain length",
                "Please enter the length of the word you would like to find:",
            )
            if n is not None and n > 2:
                valid_paths = ex11_utils.find_length_n_words(
                    n, self.board, self._dictionary
                )
                if valid_paths != []:
                    selected_word_and_path = self.selected_word_and_path(valid_paths)
                    if selected_word_and_path != None:
                        word, selected_path = selected_word_and_path
                        if word and selected_path:
                            for row, col in selected_path:
                                button = self.buttons[row][col]
                                button["bg"] = ex11_utils.DARKER_YELLOW
                            self.words_format.config(text=word)
                else:
                    self.status_label.config(
                        text=(f"No {n}-letter-word found on this board.")
                    )
                    self._root.after(
                        3000, lambda: self.status_label.config(text="")
                    )  # Clear message after 3 seconds
            else:
                self.status_label.config(
                    text="The length of the word should be \n at least 3 letters!"
                )
                self._root.after(
                    3000, lambda: self.status_label.config(text="")
                )  # Clear message after 3 seconds

    def set_bottom_buttons(self):
        # Create the buttons on the bottom of the page
        self.end_game_btn = Button(
            self.bottom_frame,
            text="End Game",
            font=("Comic Sans MS", 12, "bold"),
            bg=ex11_utils.DARK_GREEN,
            fg=ex11_utils.VERY_LIGHT_GREEN,
            relief="sunken",
            command=self.reset_game,
        )
        self.reveal_word_btn = Button(
            self.bottom_frame,
            text="Reveal word",
            font=("Comic Sans MS", 12, "bold"),
            bg=ex11_utils.DARK_GREEN,
            fg=ex11_utils.VERY_LIGHT_GREEN,
            relief="sunken",
            command=self.reveal_word,
        )

        self.find_words_btn = Button(
            self.bottom_frame,
            text="Word length",
            font=("Comic Sans MS", 12, "bold"),
            bg=ex11_utils.DARK_GREEN,
            fg=ex11_utils.VERY_LIGHT_GREEN,
            relief="sunken",
            command=self.find_words_of_length_n,
        )
        # Set the buttons centered and equally spaced
        button_width = 0.2  # Adjust the width as needed
        spacing = (1 - 3 * button_width) / 4  # Calculate spacing between buttons
        self.end_game_btn.place(
            relx=spacing, rely=0.04, relwidth=button_width, relheight=0.08
        )
        self.reveal_word_btn.place(
            relx=2 * spacing + button_width,
            rely=0.04,
            relwidth=button_width,
            relheight=0.08,
        )
        self.find_words_btn.place(
            relx=3 * spacing + 2 * button_width,
            rely=0.04,
            relwidth=button_width,
            relheight=0.08,
        )

    def selected_word_and_path(self, valid_paths):
        # Randomly select a path from a list of valid paths
        # on the board and returns the corresponding word and path.
        if valid_paths != []:
            selected_path = random.choice(valid_paths)
            word = ex11_utils.create_word(selected_path, self.board)
            if word in self.words_found:
                valid_paths.remove(selected_path)
                return self.selected_word_and_path(valid_paths)
            else:
                return word, selected_path
        else:
            self.status_label.config(
                text=(f"No word of this length found on this board.")
            )
            self._root.after(
                3000, lambda: self.status_label.config(text="")
            )  # Clear message after 3 seconds

    def reveal_word(self):
        # Reveal a word on the board that is not already found
        if self.game_started:
            self.reset_buttons()
            valid_paths = ex11_utils.max_score_paths(self.board, self._dictionary)

            if valid_paths:
                selected_word_result = self.selected_word_and_path(valid_paths)
                if selected_word_result:
                    word, selected_path = selected_word_result
                    # Highlight the corresponding cells on the board
                    for row, col in selected_path:
                        button = self.buttons[row][col]
                        button["bg"] = ex11_utils.DARKER_YELLOW

                    # Update the word_format label
                    self.words_format.config(text=word)

    def set_points_frame(self):
        self.frame = Frame(self.top)
        self.frame.place(relx=0.07, rely=0.2, relwidth=0.08, relheight=0.6)
        self.points_score = Label(
            self.frame,
            text=self._score,
            font=("Comic Sans MS", 14),
            bg=ex11_utils.LIGHT_GREEN,
            fg=ex11_utils.VERY_DARK_GREEN,
        )
        self.points = Label(
            self.frame,
            text="POINTS",
            font=("Comic Sans MS", 10),
            bg=ex11_utils.LIGHT_GREEN,
            fg=ex11_utils.VERY_DARK_GREEN,
        )
        self.points_score.pack(side=TOP, fill=X)
        self.points.pack(side=TOP, fill=X)

    def set_words_found(self):
        # Add found word to the right board
        self.pane_r = PanedWindow(self.right_frame, orient=VERTICAL)
        self.pane_r.place(
            relwidth=0.9, relheight=0.9, relx=0.5, rely=0.5, anchor=CENTER
        )
        self.found_words = Text(self.pane_r, state="disabled")
        self.found_words_label = Label(
            self.pane_r,
            text="DISCOVERED WORDS",
            font=("Comic Sans MS", 12),
            bg=ex11_utils.LIGHT_GREEN,
            fg=ex11_utils.VERY_DARK_GREEN,
        )
        self.pane_r.add(self.found_words_label)
        self.pane_r.add(self.found_words)
        self.scrollbar_r = Scrollbar(self.found_words, orient=VERTICAL)
        self.scrollbar_r.pack(side=RIGHT, fill=Y)
        self.found_words.config(yscrollcommand=self.scrollbar_r.set)
        self.scrollbar_r.config(command=self.found_words.yview)

    def set_words_tried(self):
        # Add tried word to the right board
        self.pane_l = PanedWindow(self.left_frame, orient=VERTICAL)
        self.pane_l.place(
            relwidth=0.9, relheight=0.9, relx=0.5, rely=0.5, anchor=CENTER
        )
        self.tried_words = Text(self.pane_l, state="disabled")
        self.tried_words_label = Label(
            self.pane_l,
            text="INVALID TRIED WORDS",
            font=("Comic Sans MS", 12),
            bg=ex11_utils.LIGHT_RED,
            fg="white",
        )
        self.pane_l.add(self.tried_words_label)
        self.pane_l.add(self.tried_words)
        self.scrollbar_l = Scrollbar(self.tried_words, orient=VERTICAL)
        self.scrollbar_l.pack(side=RIGHT, fill=Y)
        self.tried_words.config(yscrollcommand=self.scrollbar_l.set)
        self.scrollbar_l.config(command=self.tried_words.yview)

    def set_word_formation(self):
        # Create the bar for validating a new found word
        frame = Frame(
            self.center_main,
            bg="white",
        )
        frame.place(relx=0.20, rely=0.03, relwidth=0.6, relheight=0.1)

        self.words_format = Label(frame, text="", font=("Comic Sans MS", 14))
        self.words_format.pack(fill=BOTH, expand=True)

    def set_top_frame(self):
        self.top = Frame(self._root, bg=ex11_utils.LIGHT_GREEN)
        self.top.place(rely=0, relheight=ex11_utils.SPLIT, relwidth=1.0)
        self.label = Label(
            self.top,
            text="BOGGLE GAME",
            font=("Comic Sans MS", 25, "bold"),
            bg=ex11_utils.LIGHT_GREEN,
            fg=ex11_utils.VERY_DARK_GREEN,
        )
        self.label.place(relx=0.5, rely=0.5, anchor=CENTER)

    def update_timer(self):
        if self.remaining_time >= 0 and self.game_started:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60

            self.time_widget.delete("all")

            # Change color to red when 20 seconds or less are remaining
            if self.remaining_time <= 20:
                self.draw_timer_arc(
                    40,
                    40,
                    35,
                    0,
                    360 - (self.remaining_time / 180) * 360,
                    ex11_utils.LIGHT_RED,
                )
            else:
                self.draw_timer_arc(
                    40,
                    40,
                    35,
                    0,
                    360 - (self.remaining_time / 180) * 360,
                    ex11_utils.INTER_LIGHT,
                )
            self.time_widget.create_text(
                40,
                40,
                text=f"{minutes:02}:{seconds:02}",
                font=("Comic Sans MS", 18),
                fill=ex11_utils.VERY_DARK_GREEN,
            )
            self.remaining_time -= 1
            self._root.after(1000, self.update_timer)
        else:
            self.reset_game()

    def draw_timer_arc(self, x, y, r, start_deg, end_deg, color):
        # Draw the timer circle and fill it
        if start_deg == end_deg:
            return  # skip the drawing when start_deg is equal to end_deg
        self.time_widget.create_arc(
            x - r,
            y - r,
            x + r,
            y + r,
            start=start_deg,
            extent=end_deg - start_deg,
            fill=color,
            outline=color,
            width=2,
        )

    def set_time_widget(self):
        time_widget_bg_color = self.top["bg"]
        self.time_widget = Canvas(
            self.top,
            width=130,
            height=130,
            bg=time_widget_bg_color,
            highlightthickness=0,
        )
        self.time_widget.place(relx=0.85, rely=0.05)
        self.time_widget.create_oval(0, 0, 80, 80, width=2, outline="")

    def display_game_results(self):
        # creates a frame to hold the results
        results_frame = Frame(self.center_main, bg=ex11_utils.LIGHT_GREEN)
        results_frame.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.4)

        # create a label to display the score
        score_label = Label(
            results_frame,
            text=f"Score: {self._score}",
            font=("Comic Sans MS", 16),
            bg=ex11_utils.LIGHT_GREEN,
            fg=ex11_utils.VERY_DARK_GREEN,
        )
        score_label.pack(side=TOP, pady=10)

        # calculate the number of valid words found
        num_valid_words = len(self.words_found)

        # create a label to display the number of valid words found
        valid_words_label = Label(
            results_frame,
            text=f"Valid Words Found: {num_valid_words}",
            font=("Comic Sans MS", 14),
            bg=ex11_utils.LIGHT_GREEN,
            fg=ex11_utils.VERY_DARK_GREEN,
        )
        valid_words_label.pack(side=TOP, pady=10)
