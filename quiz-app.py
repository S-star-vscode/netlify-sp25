import tkinter as tk
from tkinter import messagebox
import random
import winsound

# Load questions from file
def load_questions(filename):
    questions = []
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
        for i in range(0, len(lines), 5):
            question = lines[i]
            choices = lines[i+1:i+5]
            questions.append((question, choices))
    return questions

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Quiz Game")
        self.original_questions = load_questions("quiz-questions.txt")

        self.score = 0
        self.current_question = 0

        self.question_label = tk.Label(root, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(root, text="", width=40, command=lambda idx=i: self.check_answer(idx))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.status_label = tk.Label(root, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.try_again_button = tk.Button(root, text="Try Again", command=self.start_quiz)
        self.try_again_button.pack(pady=10)
        self.try_again_button.pack_forget()

        self.incorrect_frame = tk.Frame(root)
        self.incorrect_frame.pack(pady=5)

        self.start_quiz()

    def start_quiz(self):
        self.score = 0
        self.current_question = 0
        self.incorrect_questions = []
        for widget in self.incorrect_frame.winfo_children():
            widget.destroy()
        self.questions = random.sample(self.original_questions, 5)
        self.try_again_button.pack_forget()
        self.load_next_question()

    def load_next_question(self):
        if self.current_question >= len(self.questions):
            self.show_result()
            return

        q_text, choices = self.questions[self.current_question]
        self.correct_answer = choices[0]
        self.current_q_text = q_text
        self.current_choices = choices.copy()
        random.shuffle(choices)

        self.question_label.config(text=f"Q{self.current_question + 1}: {q_text}")
        for i in range(4):
            self.buttons[i].config(text=choices[i], state=tk.NORMAL)

    def check_answer(self, idx):
        selected = self.buttons[idx].cget("text")
        if selected == self.correct_answer:
            self.score += 1
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        else:
            winsound.MessageBeep(winsound.MB_ICONHAND)
            self.incorrect_questions.append((self.current_q_text, self.correct_answer, selected))
        self.current_question += 1
        self.load_next_question()

    def show_result(self):
        self.question_label.config(text=f"Quiz Completed! Your score is: {self.score}/{len(self.questions)}")
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

        for widget in self.incorrect_frame.winfo_children():
            widget.destroy()

        if self.incorrect_questions:
            title = tk.Label(self.incorrect_frame, text="Incorrect Questions (with correct and your answers):", font=("Arial", 12, "bold"))
            title.pack(anchor="w")
            for q, correct, user in self.incorrect_questions:
                tk.Label(self.incorrect_frame, text=f"- {q}", font=("Arial", 11)).pack(anchor="w")
                tk.Label(self.incorrect_frame, text=f"  Correct Answer: {correct}", font=("Arial", 11), fg="green").pack(anchor="w")
                tk.Label(self.incorrect_frame, text=f"  Your Answer: {user}", font=("Arial", 11), fg="red").pack(anchor="w")

        self.try_again_button.pack()

if __name__ == '__main__':
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()