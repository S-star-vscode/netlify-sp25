import tkinter as tk
from tkinter import messagebox
import random

class WordGuessGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Word Guessing Game")
        self.geometry("400x300")
        self.resizable(False, False)

        self.words = self.load_words("guess-game-key.txt")
        self.secret_word = random.choice(self.words).lower()
        self.masked_word = ["_" for _ in self.secret_word]
        self.remaining_tries = 6
        self.guessed_letters = set()

        self.create_widgets()

    def load_words(self, filename):
        try:
            with open(filename, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            messagebox.showerror("Error", f"'{filename}' not found.")
            self.destroy()

    def create_widgets(self):
        self.info_label = tk.Label(self, text="Guess a letter or the full word:", font=("Arial", 12))
        self.info_label.pack(pady=10)

        self.word_display = tk.Label(self, text=" ".join(self.masked_word), font=("Courier", 20))
        self.word_display.pack(pady=10)

        self.entry = tk.Entry(self, font=("Arial", 14))
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda event: self.make_guess())

        self.guess_button = tk.Button(self, text="Guess", command=self.make_guess)
        self.guess_button.pack(pady=5)

        self.status_label = tk.Label(self, text=f"Tries left: {self.remaining_tries}", font=("Arial", 10))
        self.status_label.pack(pady=10)

    def make_guess(self):
        guess = self.entry.get().lower().strip()
        self.entry.delete(0, tk.END)

        if not guess:
            return

        if len(guess) == 1:  # Letter guess
            if guess in self.guessed_letters:
                messagebox.showinfo("Repeat", f"You already guessed '{guess}'.")
                return
            self.guessed_letters.add(guess)
            if guess in self.secret_word:
                for i, letter in enumerate(self.secret_word):
                    if letter == guess:
                        self.masked_word[i] = guess
            else:
                self.remaining_tries -= 1
        else:  # Full word guess
            if guess == self.secret_word:
                self.masked_word = list(self.secret_word)
            else:
                self.remaining_tries -= 1

        self.update_display()

    def update_display(self):
        self.word_display.config(text=" ".join(self.masked_word))
        self.status_label.config(text=f"Tries left: {self.remaining_tries}")

        if "_" not in self.masked_word:
            messagebox.showinfo("Victory!", f"You guessed it! The word was '{self.secret_word}'.")
            self.reset_game()
        elif self.remaining_tries <= 0:
            messagebox.showerror("Game Over", f"You're out of tries. The word was '{self.secret_word}'.")
            self.reset_game()

    def reset_game(self):
        self.secret_word = random.choice(self.words).lower()
        self.masked_word = ["_" for _ in self.secret_word]
        self.remaining_tries = 6
        self.guessed_letters.clear()
        self.update_display()

if __name__ == "__main__":
    game = WordGuessGame()
    game.mainloop()
