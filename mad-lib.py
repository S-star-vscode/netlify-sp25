import tkinter as tk
from tkinter import ttk, messagebox

# Define the story templates and placeholders
story_templates = {
    "Fox Story": {
        "template": "The {adj1} fox jumped over the {adj2} dog.",
        "placeholders": ["adj1", "adj2"]
    },
    "Adventure Story": {
        "template": "One day, a {adj1} explorer found a {noun1} in the {place}.",
        "placeholders": ["adj1", "noun1", "place"]
    },
    "Sci-Fi Story": {
        "template": "In the year {year}, a {adj1} robot named {name} saved {planet} from disaster.",
        "placeholders": ["year", "adj1", "name", "planet"]
    }
}

class MadLibsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mad Libs Generator")
        self.geometry("500x400")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Dropdown for story selection
        self.story_choice = tk.StringVar()
        self.story_menu = ttk.Combobox(self, textvariable=self.story_choice, state="readonly")
        self.story_menu['values'] = list(story_templates.keys())
        self.story_menu.set("Choose a story...")
        self.story_menu.pack(pady=10)
        self.story_menu.bind("<<ComboboxSelected>>", self.generate_inputs)

        # Frame for dynamic inputs
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(pady=10)

        # Button to create the story
        self.generate_button = tk.Button(self, text="Generate Story", command=self.generate_story)
        self.generate_button.pack(pady=10)

        # Text widget to display the story
        self.output = tk.Text(self, height=6, wrap='word')
        self.output.pack(padx=10, pady=10, fill="both", expand=True)

    def generate_inputs(self, event):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        story_key = self.story_choice.get()
        self.fields = {}

        for placeholder in story_templates[story_key]["placeholders"]:
            label = tk.Label(self.input_frame, text=f"Enter {placeholder}:")
            label.pack()
            entry = tk.Entry(self.input_frame)
            entry.pack()
            self.fields[placeholder] = entry

    def generate_story(self):
        story_key = self.story_choice.get()
        template_info = story_templates.get(story_key)

        if not template_info:
            messagebox.showerror("Error", "Please select a valid story.")
            return

        try:
            filled_data = {key: self.fields[key].get() for key in template_info["placeholders"]}
            story = template_info["template"].format(**filled_data)
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, story)
        except KeyError as e:
            messagebox.showerror("Missing Field", f"Missing input for: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = MadLibsApp()
    app.mainloop()
