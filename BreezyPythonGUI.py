""" BreezyPythonGUI.py

A simplified wrapper for Tkinter
Provides a simple object-oriented 
framework for writing GUI programs.
"""

import tkinter
from tkinter import messagebox

class EasyFrame(tkinter.Tk):
    """Basic window class for BreezyPythonGUI."""

    def __init__(self, title="Window", width=400, height=200, resizable=True):
        tkinter.Tk.__init__(self)
        self.title(title)
        self.geometry(f"{width}x{height}")
        if not resizable:
            self.resizable(False, False)
        self.widgets = {}

    def addLabel(self, text, row, column, sticky="w"):
        label = tkinter.Label(self, text=text)
        label.grid(row=row, column=column, sticky=sticky)
        return label

    def addButton(self, text, row, column, command, sticky="w"):
        button = tkinter.Button(self, text=text, command=command)
        button.grid(row=row, column=column, sticky=sticky)
        return button

    def addTextField(self, text="", row=0, column=0, width=10, sticky="w"):
        entry = tkinter.Entry(self, width=width)
        entry.insert(0, text)
        entry.grid(row=row, column=column, sticky=sticky)
        return entry

    def addIntegerField(self, value=0, row=0, column=0, width=10, sticky="w"):
        entry = tkinter.Entry(self, width=width)
        entry.insert(0, str(value))
        entry.grid(row=row, column=column, sticky=sticky)
        return entry

    def addFloatField(self, value=0.0, row=0, column=0, width=10, sticky="w"):
        entry = tkinter.Entry(self, width=width)
        entry.insert(0, str(value))
        entry.grid(row=row, column=column, sticky=sticky)
        return entry

    def addTextArea(self, text="", row=0, column=0, width=40, height=5, sticky="w"):
        textArea = tkinter.Text(self, width=width, height=height)
        textArea.insert("1.0", text)
        textArea.grid(row=row, column=column, sticky=sticky)
        return textArea

    def messageBox(self, title, message):
        messagebox.showinfo(title, message)
