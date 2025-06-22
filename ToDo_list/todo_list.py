import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date
from tkcalendar import DateEntry
import json
import os

class Task:
    def __init__(self, text, due_date, completed=False):
        self.text = text
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return {
            "text": self.text,
            "due_date": self.due_date.strftime('%Y-%m-%d'),
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(
            text=data["text"],
            due_date=datetime.strptime(data["due_date"], '%Y-%m-%d').date(),
            completed=data["completed"]
        )

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 To-Do List with Save")
        self.root.geometry("520x600")
        self.root.configure(bg="#2C3E50")

        self.tasks = []
        self.file_path = "tasks.json"

        self.create_widgets()
        self.load_tasks()

    def create_widgets(self):
        tk.Label(self.root, text="To-Do List", font=("Helvetica", 22, "bold"), fg="#ECF0F1", bg="#2C3E50").pack(pady=20)

        input_frame = tk.Frame(self.root, bg="#2C3E50")
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=22)
        self.task_entry.grid(row=0, column=0, padx=5)

        self.due_date_picker = DateEntry(
            input_frame,
            font=("Helvetica", 12),
            width=12,
            mindate=date.today(),
            date_pattern="yyyy-mm-dd",
            background="darkblue",
            foreground="white",
            borderwidth=2
        )
        self.due_date_picker.grid(row=0, column=1, padx=5)

        tk.Button(input_frame, text="Add Task", command=self.add_task, bg="#27AE60", fg="white", width=12).grid(row=0, column=2, padx=5)

        self.task_frame = tk.Frame(self.root, bg="#34495E", bd=2)
        self.task_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    def add_task(self):
        text = self.task_entry.get().strip()
        due_date = self.due_date_picker.get_date()

        if not text:
            messagebox.showwarning("Missing Info", "Please enter a task.")
            return

        task = Task(text, due_date)
        self.tasks.append(task)

        self.task_entry.delete(0, tk.END)
        self.due_date_picker.set_date(date.today())

        self.save_tasks()
        self.update_tasks()

    def display_task(self, index, task):
        task_row = tk.Frame(self.task_frame, bg="#34495E")
        task_row.pack(fill="x", pady=5, padx=5)

        var = tk.BooleanVar(value=task.completed)
        checkbox = tk.Checkbutton(task_row, variable=var, bg="#34495E", command=lambda i=index: self.toggle_complete(i))
        checkbox.pack(side="left")

        due_str = f" (Due: {task.due_date.strftime('%Y-%m-%d')})"
        label_text = f"{task.text}{due_str}"

        task_label = tk.Label(task_row, text=label_text, font=("Helvetica", 12, "italic" if task.completed else "normal"),
                              fg="#95A5A6" if task.completed else "white", bg="#34495E")
        task_label.pack(side="left", padx=5)

        del_btn = tk.Button(task_row, text="❌", bg="#C0392B", fg="white", command=lambda i=index: self.delete_task(i))
        del_btn.pack(side="right", padx=5)

    def update_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        for index, task in enumerate(self.tasks):
            self.display_task(index, task)

    def toggle_complete(self, index):
        self.tasks[index].completed = not self.tasks[index].completed
        self.save_tasks()
        self.update_tasks()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()
        self.update_tasks()

    def save_tasks(self):
        with open(self.file_path, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
        self.update_tasks()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
