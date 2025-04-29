# Import required modules
from BreezyPythonGUI import EasyFrame
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.ttk import Combobox
import tkinter as tk

class BookTracker(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="Book Tracker")
        self.bookList = []

        # Title input
        self.addLabel("Title:", row=0, column=0, sticky="w")
        self.titleField = self.addTextField("", row=0, column=1)

        # Author input
        self.addLabel("Author:", row=1, column=0, sticky="w")
        self.authorField = self.addTextField("", row=1, column=1)

        # Reading status dropdown
        self.addLabel("Status:", row=2, column=0, sticky="w")
        self.statusOptions = ["Not Started", "In Progress", "Completed"]
        self.statusVar = tk.StringVar()
        self.statusField = Combobox(self, textvariable=self.statusVar, values=self.statusOptions, state="readonly")
        self.statusField.current(0)
        self.statusField.grid(row=2, column=1, sticky="w", padx=6, pady=2)

        # Action buttons
        self.addButton("Add Book", row=3, column=0, command=self.addBook)
        self.addButton("Mark as Read", row=3, column=1, command=self.markAsRead)
        self.addButton("Load List", row=4, column=0, command=self.loadBooks)
        self.addButton("Save List", row=4, column=1, command=self.saveBooks)
        self.addButton("Delete Book", row=4, column=2, command=self.deleteBook)

        # Create search panel using tkinter.Frame manually
        searchFrame = tk.Frame(self, bg="black", bd=2, relief="solid", padx=10, pady=6)
        searchFrame.grid(row=5, column=0, columnspan=4, sticky="w")

        # Search UI inside frame
        tk.Label(searchFrame, text="Search:", bg="black", fg="white").grid(row=0, column=0, sticky="w")
        self.searchField = tk.Entry(searchFrame, width=40)
        self.searchField.grid(row=0, column=1, padx=4)
        tk.Button(searchFrame, text="Search", command=self.searchBook).grid(row=0, column=2, padx=4)
        tk.Button(searchFrame, text="Clear Search", command=self.clearSearch).grid(row=0, column=3, padx=4)

        # Display area
        self.bookArea = self.addTextArea("", row=6, column=0, width=100, height=18)
        self.bookArea["state"] = "disabled"

    def addBook(self):
        title = self.titleField.get().strip()
        author = self.authorField.get().strip()
        status = self.statusVar.get()
        if title and author:
            self.bookList.append({"title": title, "author": author, "status": status})
            self.updateDisplay()
            self.clearFields()
        else:
            self.messageBox("Error", "Title and Author are required.")

    def markAsRead(self):
        title = self.titleField.get().strip().lower()
        found = False
        for book in self.bookList:
            if book["title"].lower() == title:
                book["status"] = "Completed"
                found = True
                break
        if found:
            self.updateDisplay()
        else:
            self.messageBox("Error", "Book not found.")

    def loadBooks(self):
        filename = askopenfilename()
        if not filename:
            return
        try:
            with open(filename, "r") as file:
                self.bookList = []
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) == 3:
                        title, author, status = parts
                        self.bookList.append({"title": title, "author": author, "status": status})
                self.updateDisplay()
        except Exception as e:
            self.messageBox("Error", f"Could not load file: {e}")

    def saveBooks(self):
        filename = asksaveasfilename(defaultextension=".txt")
        if not filename:
            return
        try:
            with open(filename, "w") as file:
                for book in self.bookList:
                    line = f"{book['title']}|{book['author']}|{book['status']}\n"
                    file.write(line)
        except Exception as e:
            self.messageBox("Error", f"Could not save file: {e}")

    def updateDisplay(self):
        self.bookArea["state"] = "normal"
        self.bookArea.delete("1.0", "end")
        header = f"{'Title':<30}|{'Author':<30}|{'Reading Status':<20}\n"
        separator = f"{'-'*30}+{'-'*30}+{'-'*20}\n"
        self.bookArea.insert("end", header + separator)
        for book in self.bookList:
            entry = f"{book['title']:<30}|{book['author']:<30}|{book['status']:<20}\n"
            self.bookArea.insert("end", entry)
        self.bookArea.see("end")
        self.bookArea["state"] = "disabled"

    def deleteBook(self):
        if self.bookList:
            deleted = self.bookList.pop()
            self.updateDisplay()
            self.messageBox("Success", f"Deleted most recent book: {deleted['title']}")
            self.clearFields()
        else:
            self.messageBox("Error", "Book not found.")

    def searchBook(self):
        query = self.searchField.get().strip().lower()
        self.bookArea["state"] = "normal"
        self.bookArea.delete("1.0", "end")

        header = f"{'Title':<30}|{'Author':<30}|{'Reading Status':<20}\n"
        separator = f"{'-'*30}+{'-'*30}+{'-'*20}\n"
        self.bookArea.insert("end", header + separator)

        for book in self.bookList:
            line = f"{book['title']:<30}|{book['author']:<30}|{book['status']:<20}\n"
            if query and (query in book['title'].lower() or query in book['author'].lower()):
                self.bookArea.insert("end", line, "highlight")
            else:
                self.bookArea.insert("end", line)

        self.bookArea.tag_configure("highlight", background="yellow")
        self.bookArea.see("end")
        self.bookArea["state"] = "disabled"

    def clearSearch(self):
        """Clear the search box and reset the book list display."""
        self.searchField.delete(0, tk.END)
        self.updateDisplay()

    def clearFields(self):
        self.titleField.setText("")
        self.authorField.setText("")
        self.statusField.current(0)

if __name__ == "__main__":
    BookTracker().mainloop()
