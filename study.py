from BreezyPythonGUI import EasyFrame
from tkinter.filedialog import askopenfilename
import random

class FlashcardApp(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="Flashcard Quiz App")

        self.addLabel(text="Question:", row=0, column=0)
        self.questionLabel = self.addLabel(text="", row=0, column=1)

        self.addLabel(text="Your Answer:", row=1, column=0)
        self.answerField = self.addTextField("", row=1, column=1, width=40)

        self.addButton("Check Answer", 2, 0, self.checkAnswer)
        self.addButton("Next Card", 2, 1, self.nextCard)
        self.addButton("Load Flashcards", 3, 0, self.loadFlashcards)

        self.outputArea = self.addTextArea("", row=5, column=0, width=50, height=4)
        self.outputArea["state"] = "disabled"

        self.flashcards = []
        self.remainingCards = []
        self.currentCard = None
        self.correct = 0
        self.incorrect = 0

    def loadFlashcards(self):
        filename = askopenfilename(title="Select flashcard file")
        if filename:
            with open(filename, "r") as file:
                self.flashcards = []
                for line in file:
                    if ':' in line:
                        q, a = line.strip().split(":", 1)
                        self.flashcards.append((q.strip(), a.strip()))
            random.shuffle(self.flashcards)
            self.remainingCards = self.flashcards[:]
            self.correct = 0
            self.incorrect = 0
            self.nextCard()

    def nextCard(self):
        if not self.remainingCards:
            self.showOutput("No more flashcards. Quiz complete!\nCorrect: {} | Incorrect: {}".format(self.correct, self.incorrect))
            self.questionLabel["text"] = ""
            return
        self.currentCard = self.remainingCards.pop()
        self.questionLabel["text"] = self.currentCard[0]
        self.answerField.setValue("")
        self.showOutput("")

    def checkAnswer(self):
        if not self.currentCard:
            self.showOutput("No card selected.")
            return
        userAnswer = self.answerField.get().strip()
        correctAnswer = self.currentCard[1]
        if userAnswer.lower() == correctAnswer.lower():
            self.correct += 1
            result = "Correct!"
        else:
            self.incorrect += 1
            result = f"Incorrect. The correct answer was: {correctAnswer}"
        score = f"Correct: {self.correct} | Incorrect: {self.incorrect}"
        self.showOutput(f"{result}\n{score}")

    def showOutput(self, message):
        self.outputArea["state"] = "normal"
        self.outputArea.delete("1.0", "end"); self.outputArea.insert("end", message)
        self.outputArea["state"] = "disabled"

if __name__ == "__main__":
    FlashcardApp().mainloop()
