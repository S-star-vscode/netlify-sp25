
import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class AutoOrganizerHandler(FileSystemEventHandler):
    def __init__(self, app, mode):
        self.app = app
        self.mode = mode

    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)  # Ensure file is fully saved
            self.organize_file(event.src_path)

    def organize_file(self, filepath):
        folder = os.path.dirname(filepath)
        filename = os.path.basename(filepath)

        try:
            if self.mode == "extension":
                ext = os.path.splitext(filename)[1][1:] or "no_extension"
                dest = os.path.join(folder, ext.upper())
            elif self.mode == "date":
                mod_time = os.path.getmtime(filepath)
                dest = os.path.join(folder, datetime.fromtimestamp(mod_time).strftime("%Y-%m"))
            elif self.mode == "size":
                size = os.path.getsize(filepath)
                if size < 1_000_000:
                    dest = os.path.join(folder, "Small")
                elif size < 10_000_000:
                    dest = os.path.join(folder, "Medium")
                else:
                    dest = os.path.join(folder, "Large")
            else:
                return

            os.makedirs(dest, exist_ok=True)
            os.rename(filepath, os.path.join(dest, filename))
            print(f"Moved: {filename}")
        except Exception as e:
            print(f"Error organizing file: {e}")


class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart File Organizer")

        self.current_path = os.path.expanduser("~")
        self.path_var = tk.StringVar(value=self.current_path)

        path_frame = tk.Frame(root)
        path_frame.pack(fill="x", padx=10, pady=5)
        tk.Entry(path_frame, textvariable=self.path_var, width=60).pack(side="left", expand=True, fill="x")
        tk.Button(path_frame, text="Browse", command=self.browse_folder).pack(side="left", padx=5)
        tk.Button(path_frame, text="Up", command=self.go_up).pack(side="left")

        self.tree = ttk.Treeview(root, columns=("Name", "Size", "Modified"), show="headings", selectmode="extended")
        self.tree.heading("Name", text="Name", command=lambda: self.sort_by("Name"))
        self.tree.heading("Size", text="Size", command=lambda: self.sort_by("Size"))
        self.tree.heading("Modified", text="Modified", command=lambda: self.sort_by("Modified"))
        self.tree.column("Name", width=250)
        self.tree.column("Size", width=100)
        self.tree.column("Modified", width=150)
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        self.tree.bind("<Double-1>", self.on_double_click)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Move Selected Files", command=self.move_files).pack(side="left", padx=10)
        tk.Button(button_frame, text="Delete Selected Files", command=self.delete_files).pack(side="left", padx=10)

        organize_frame = tk.Frame(root)
        organize_frame.pack(pady=10)
        tk.Label(organize_frame, text="Smart Organize:").pack(side="left", padx=5)
        tk.Button(organize_frame, text="By Extension", command=self.organize_by_extension).pack(side="left", padx=5)
        tk.Button(organize_frame, text="By Date", command=self.organize_by_date).pack(side="left", padx=5)
        tk.Button(organize_frame, text="By File Size", command=self.organize_by_size).pack(side="left", padx=5)

        watch_frame = tk.Frame(root)
        watch_frame.pack(pady=5)
        self.watch_mode = tk.StringVar(value="extension")
        for text, val in [("Extension", "extension"), ("Date", "date"), ("Size", "size")]:
            tk.Radiobutton(watch_frame, text=text, variable=self.watch_mode, value=val).pack(side="left")

        self.is_watching = False
        self.observer = None
        tk.Button(watch_frame, text="Start Watching", command=self.start_watching).pack(side="left", padx=10)
        tk.Button(watch_frame, text="Stop Watching", command=self.stop_watching).pack(side="left")

        self.load_directory()

    def browse_folder(self):
        path = filedialog.askdirectory(initialdir=self.current_path)
        if path:
            self.current_path = path
            self.path_var.set(path)
            self.load_directory()

    def go_up(self):
        parent = os.path.dirname(self.current_path)
        self.current_path = parent
        self.path_var.set(parent)
        self.load_directory()

    def load_directory(self):
        self.tree.delete(*self.tree.get_children())
        path = self.path_var.get()
        try:
            entries = os.listdir(path)
            for entry in entries:
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    size = "<DIR>"
                else:
                    size = self.format_size(os.path.getsize(full_path))
                modified = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M")
                self.tree.insert("", "end", values=(entry, size, modified))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def format_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes // 1024} KB"
        else:
            return f"{size_bytes // (1024 * 1024)} MB"

    def on_double_click(self, event):
        selected = self.tree.focus()
        values = self.tree.item(selected, "values")
        if not values:
            return
        name = values[0]
        new_path = os.path.join(self.current_path, name)
        if os.path.isdir(new_path):
            self.current_path = new_path
            self.path_var.set(new_path)
            self.load_directory()

    def sort_by(self, key):
        items = [self.tree.item(child)["values"] for child in self.tree.get_children()]
        index = {"Name": 0, "Size": 1, "Modified": 2}[key]

        def size_to_bytes(size_str):
            try:
                if size_str.endswith("KB"):
                    return int(size_str.split()[0]) * 1024
                elif size_str.endswith("MB"):
                    return int(size_str.split()[0]) * 1024 * 1024
                elif size_str.endswith("B"):
                    return int(size_str.split()[0])
                else:
                    return 0
            except:
                return 0

        if key == "Size":
            items.sort(key=lambda x: size_to_bytes(x[1]))
        elif key == "Modified":
            items.sort(key=lambda x: x[2])
        else:
            items.sort(key=lambda x: x[0].lower())

        self.tree.delete(*self.tree.get_children())
        for item in items:
            self.tree.insert("", "end", values=item)

    def move_files(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No selection", "Please select one or more files to move.")
            return
        dest_folder = filedialog.askdirectory(title="Select destination folder")
        if not dest_folder:
            return
        moved = 0
        for item in selected_items:
            filename = self.tree.item(item, "values")[0]
            src_path = os.path.join(self.current_path, filename)
            dest_path = os.path.join(dest_folder, filename)
            if os.path.isdir(src_path):
                continue
            try:
                os.rename(src_path, dest_path)
                moved += 1
            except Exception as e:
                messagebox.showerror("Error", f"Error moving {filename}: {e}")
        if moved:
            messagebox.showinfo("Success", f"{moved} file(s) moved successfully.")
            self.load_directory()

    def delete_files(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No selection", "Please select one or more files to delete.")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected files?")
        if not confirm:
            return
        deleted = 0
        for item in selected_items:
            filename = self.tree.item(item, "values")[0]
            file_path = os.path.join(self.current_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted += 1
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting {filename}: {e}")
        if deleted:
            messagebox.showinfo("Success", f"{deleted} file(s) deleted successfully.")
            self.load_directory()

    def organize_by_extension(self):
        confirm = messagebox.askyesno("Confirm", "Move all files into folders by extension?")
        if not confirm:
            return
        moved = 0
        for entry in os.listdir(self.current_path):
            full_path = os.path.join(self.current_path, entry)
            if os.path.isfile(full_path):
                ext = os.path.splitext(entry)[1][1:] or "no_extension"
                dest_folder = os.path.join(self.current_path, ext.upper())
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder, entry)
                try:
                    os.rename(full_path, dest_path)
                    moved += 1
                except Exception as e:
                    print(f"Error moving {entry}: {e}")
        messagebox.showinfo("Done", f"Organized {moved} files by extension.")
        self.load_directory()

    def organize_by_date(self):
        confirm = messagebox.askyesno("Confirm", "Move files into folders by modified month/year?")
        if not confirm:
            return
        moved = 0
        for entry in os.listdir(self.current_path):
            full_path = os.path.join(self.current_path, entry)
            if os.path.isfile(full_path):
                mod_time = os.path.getmtime(full_path)
                folder_name = datetime.fromtimestamp(mod_time).strftime("%Y-%m")
                dest_folder = os.path.join(self.current_path, folder_name)
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder, entry)
                try:
                    os.rename(full_path, dest_path)
                    moved += 1
                except Exception as e:
                    print(f"Error moving {entry}: {e}")
        messagebox.showinfo("Done", f"Organized {moved} files by date.")
        self.load_directory()

    def organize_by_size(self):
        confirm = messagebox.askyesno("Confirm", "Move files into folders by file size?")
        if not confirm:
            return
        moved = 0
        for entry in os.listdir(self.current_path):
            full_path = os.path.join(self.current_path, entry)
            if os.path.isfile(full_path):
                size = os.path.getsize(full_path)
                if size < 1_000_000:
                    folder_name = "Small"
                elif size < 10_000_000:
                    folder_name = "Medium"
                else:
                    folder_name = "Large"
                dest_folder = os.path.join(self.current_path, folder_name)
                os.makedirs(dest_folder, exist_ok=True)
                dest_path = os.path.join(dest_folder, entry)
                try:
                    os.rename(full_path, dest_path)
                    moved += 1
                except Exception as e:
                    print(f"Error moving {entry}: {e}")
        messagebox.showinfo("Done", f"Organized {moved} files by size.")
        self.load_directory()

    def start_watching(self):
        if self.is_watching:
            messagebox.showinfo("Watcher", "Already watching.")
            return
        mode = self.watch_mode.get()
        folder = self.current_path
        event_handler = AutoOrganizerHandler(self, mode)
        self.observer = Observer()
        self.observer.schedule(event_handler, path=folder, recursive=False)
        self.observer.start()
        self.is_watching = True
        messagebox.showinfo("Watcher", f"Now watching '{folder}' with mode: {mode}")

    def stop_watching(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
            self.is_watching = False
            messagebox.showinfo("Watcher", "Stopped watching.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorer(root)
    root.geometry("700x600")
    root.mainloop()
