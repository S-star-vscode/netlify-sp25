import tkinter as tk
from tkinter import messagebox, filedialog
import os
import glob
from datetime import datetime
from docx import Document

class DailyJournalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Daily Journal with Tags & Formatting")
        self.geometry("700x650")

        # Date Entry
        tk.Label(self, text="Date (YYYY-MM-DD):").pack()
        self.date_entry = tk.Entry(self)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.pack(pady=5)

        # Formatting Buttons
        format_frame = tk.Frame(self)
        format_frame.pack()
        tk.Button(format_frame, text="Bold", command=self.make_bold).pack(side=tk.LEFT, padx=5)
        tk.Button(format_frame, text="Italic", command=self.make_italic).pack(side=tk.LEFT, padx=5)
        tk.Button(format_frame, text="Underline", command=self.make_underline).pack(side=tk.LEFT, padx=5)
        tk.Button(format_frame, text="Strikethrough", command=self.make_strikethrough).pack(side=tk.LEFT, padx=5)
        tk.Button(format_frame, text="Remove Formatting", command=self.remove_formatting).pack(side=tk.LEFT, padx=5)


        # Text Area
        self.text_area = tk.Text(self, wrap=tk.WORD, font=("Helvetica", 12))
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)

        # Define Tags
        self.text_area.tag_configure("bold", font=("Helvetica", 12, "bold"))
        self.text_area.tag_configure("italic", font=("Helvetica", 12, "italic"))
        self.text_area.tag_configure("underline", font=("Helvetica", 12, "underline"))
        self.text_area.tag_configure("strikethrough", overstrike=True)

        # Save / Load / Export Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Load Entry", command=self.load_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save Entry", command=self.save_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Export to .docx", command=self.export_to_docx).pack(side=tk.LEFT, padx=5)

        # Tag Search
        tk.Label(self, text="Search by Tag (e.g., #mood):").pack(pady=5)
        self.tag_entry = tk.Entry(self)
        self.tag_entry.pack()
        tk.Button(self, text="Search Entries", command=self.search_by_tag).pack(pady=5)

    def get_filename(self):
        date_str = self.date_entry.get().strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Use format YYYY-MM-DD.")
            return None
        return f"{date_str}.txt"

    def save_entry(self):
        filename = self.get_filename()
        if filename:
            content = self.text_area.get(1.0, tk.END).strip()
            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Saved", f"Saved: {filename}")

    def load_entry(self):
        filename = self.get_filename()
        if filename and os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
        elif filename:
            self.text_area.delete(1.0, tk.END)
            messagebox.showinfo("No Entry", "No entry found. Start writing!")

    def make_bold(self):
        self.apply_tag("bold")

    def make_italic(self):
        self.apply_tag("italic")

    def make_underline(self):
        self.apply_tag("underline")

    def make_strikethrough(self):
        self.apply_tag("strikethrough")


    def remove_formatting(self):
        tags_to_remove = ["bold", "italic", "underline", "strikethrough"]
        try:
            start = self.text_area.index("sel.first")
            end = self.text_area.index("sel.last")
            for tag in tags_to_remove:
                self.text_area.tag_remove(tag, start, end)
        except tk.TclError:
            messagebox.showwarning("No Selection", "Please select text to remove formatting.")

    def apply_tag(self, tag_name):
        try:
            start, end = self.text_area.index("sel.first"), self.text_area.index("sel.last")
            self.text_area.tag_add(tag_name, start, end)
        except tk.TclError:
            messagebox.showwarning("Select Text", "Please highlight text to format.")

    def search_by_tag(self):
        tag = self.tag_entry.get().strip()
        if not tag.startswith("#"):
            messagebox.showerror("Invalid Tag", "Tags must start with '#'")
            return

        matching_files = []
        for file in glob.glob("*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                if tag in f.read():
                    matching_files.append(file)

        if matching_files:
            result = "\n".join(matching_files)
            messagebox.showinfo("Entries Found", f"Entries with {tag}:\n{result}")
        else:
            messagebox.showinfo("No Matches", f"No entries found with {tag}.")

    def export_to_docx(self):
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Empty", "Nothing to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word files", "*.docx")])
        if file_path:
            doc = Document()
            doc.add_paragraph(content)
            doc.save(file_path)
            messagebox.showinfo("Exported", f"Exported to {file_path}")

if __name__ == "__main__":
    app = DailyJournalApp()
    app.mainloop()