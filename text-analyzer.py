import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import re

# Function to process the text file and extract statistics
def analyze_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            text = file.read()
        
        words = re.findall(r'\b\w+\b', text.lower())
        word_count = len(words)
        average_word_length = sum(len(word) for word in words) / word_count if word_count else 0
        most_common_word, freq = Counter(words).most_common(1)[0] if words else ("", 0)

        return word_count, most_common_word, freq, average_word_length
    except Exception as e:
        return None, None, None, None

# Function to handle file selection and trigger analysis
def select_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        wc, common_word, freq, avg_len = analyze_file(filepath)
        if wc is not None:
            result = (
                f"File: {filepath}\n"
                f"Total words: {wc}\n"
                f"Most common word: '{common_word}' ({freq} times)\n"
                f"Average word length: {avg_len:.2f}"
            )
            messagebox.showinfo("Analysis Results", result)
        else:
            messagebox.showerror("Error", "Failed to process file.")

# Main GUI setup
def main():
    root = tk.Tk()
    root.title("Text File Analyzer")

    select_btn = tk.Button(root, text="Select Text File", command=select_file, width=30)
    select_btn.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
