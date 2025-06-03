import tkinter as tk
from tkinter import messagebox
import random

class RockPaperScissorsGUI:
    def __init__(self, master):
        self.master = master
        master.title("Rock-Paper-Scissors")
        master.geometry("400x300")
        master.resizable(False, False)

        self.user_score = 0
        self.computer_score = 0

        self.user_choice = tk.StringVar()
        self.computer_choice_str = tk.StringVar()
        self.result_str = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Instructions
        instructions = tk.Label(self.master, text="Choose your move:", font=("Arial", 14))
        instructions.pack(pady=10)

        # Buttons for choices
        button_frame = tk.Frame(self.master)
        button_frame.pack()

        rock_button = tk.Button(button_frame, text="Rock", width=10, height=2, command=lambda: self.play_round("rock"))
        rock_button.pack(side=tk.LEFT, padx=5)

        paper_button = tk.Button(button_frame, text="Paper", width=10, height=2, command=lambda: self.play_round("paper"))
        paper_button.pack(side=tk.LEFT, padx=5)

        scissors_button = tk.Button(button_frame, text="Scissors", width=10, height=2, command=lambda: self.play_round("scissors"))
        scissors_button.pack(side=tk.LEFT, padx=5)

        # Display choices
        choices_frame = tk.Frame(self.master)
        choices_frame.pack(pady=10)

        user_choice_label = tk.Label(choices_frame, text="Your choice:", font=("Arial", 12))
        user_choice_label.pack(side=tk.LEFT, padx=5)
        self.user_choice_display = tk.Label(choices_frame, textvariable=self.user_choice, font=("Arial", 12, "bold"))
        self.user_choice_display.pack(side=tk.LEFT, padx=5)

        computer_choice_label = tk.Label(choices_frame, text="Computer's choice:", font=("Arial", 12))
        computer_choice_label.pack(side=tk.LEFT, padx=5)
        self.computer_choice_display = tk.Label(choices_frame, textvariable=self.computer_choice_str, font=("Arial", 12, "bold"))
        self.computer_choice_display.pack(side=tk.LEFT, padx=5)

        # Display result
        result_label = tk.Label(self.master, text="Result:", font=("Arial", 14))
        result_label.pack()
        self.result_display = tk.Label(self.master, textvariable=self.result_str, font=("Arial", 14, "bold"))
        self.result_display.pack()

        # Display scores
        score_frame = tk.Frame(self.master)
        score_frame.pack(pady=10)

        user_score_label = tk.Label(score_frame, text="Your Score:", font=("Arial", 12))
        user_score_label.pack(side=tk.LEFT, padx=10)
        self.user_score_display_label = tk.Label(score_frame, text=self.user_score, font=("Arial", 12, "bold"))
        self.user_score_display_label.pack(side=tk.LEFT)

        computer_score_label = tk.Label(score_frame, text="Computer Score:", font=("Arial", 12))
        computer_score_label.pack(side=tk.LEFT, padx=10)
        self.computer_score_display_label = tk.Label(score_frame, text=self.computer_score, font=("Arial", 12, "bold"))
        self.computer_score_display_label.pack(side=tk.LEFT)

        # Play Again button
        play_again_button = tk.Button(self.master, text="Play Again", command=self.reset_game)
        play_again_button.pack(pady=10)

    def play_round(self, user_selection):
        choices = ["rock", "paper", "scissors"]
        computer_selection = random.choice(choices)

        self.user_choice.set(user_selection.capitalize())
        self.computer_choice_str.set(computer_selection.capitalize())

        if user_selection == computer_selection:
            self.result_str.set("It's a tie!")
        elif (user_selection == "rock" and computer_selection == "scissors") or \
             (user_selection == "scissors" and computer_selection == "paper") or \
             (user_selection == "paper" and computer_selection == "rock"):
            self.result_str.set("You win!")
            self.user_score += 1
        else:
            self.result_str.set("Computer wins!")
            self.computer_score += 1

        self.update_scores()

    def update_scores(self):
        self.user_score_display_label.config(text=self.user_score)
        self.computer_score_display_label.config(text=self.computer_score)

    def reset_game(self):
        self.user_score = 0
        self.computer_score = 0
        self.update_scores()
        self.user_choice.set("")
        self.computer_choice_str.set("")
        self.result_str.set("")

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissorsGUI(root)
    root.mainloop()