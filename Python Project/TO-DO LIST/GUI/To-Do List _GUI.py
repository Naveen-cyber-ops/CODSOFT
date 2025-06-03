import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

class TodoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        self.tasks = self.load_tasks()

        self.task_list_frame = tk.Frame(self.root)
        self.task_list_frame.pack(pady=10)

        self.task_list = tk.Listbox(self.task_list_frame, width=60, height=15)
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.task_list.bind('<<ListboxSelect>>', self.show_task_details)

        self.scrollbar = tk.Scrollbar(self.task_list_frame, orient=tk.VERTICAL, command=self.task_list.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_list.config(yscrollcommand=self.scrollbar.set)

        self.details_frame = tk.Frame(self.root)
        self.details_frame.pack(pady=5)

        tk.Label(self.details_frame, text="Details:").grid(row=0, column=0, sticky=tk.W)
        self.details_text = tk.Text(self.details_frame, width=58, height=5, state=tk.DISABLED)
        self.details_text.grid(row=1, column=0, sticky="ew")

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        tk.Button(self.button_frame, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Mark Complete", command=self.mark_complete).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Save Tasks", command=self.save_tasks).pack(side=tk.LEFT, padx=5)

        self.update_task_list()

    def load_tasks(self, filename="todo_gui.json"):
        """Loads tasks from a JSON file."""
        tasks = []
        try:
            with open(filename, "r") as f:
                tasks = json.load(f)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding the to-do list file.")
        return tasks

    def save_tasks(self, filename="todo_gui.json"):
        """Saves tasks to a JSON file."""
        try:
            with open(filename, "w") as f:
                json.dump(self.tasks, f, indent=4)
            messagebox.showinfo("Info", "Tasks saved successfully!")
        except IOError:
            messagebox.showerror("Error", "Error saving tasks.")

    def update_task_list(self):
        """Updates the listbox with the current tasks."""
        self.task_list.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            status = "[X]" if task.get('completed', False) else "[ ]"
            description = task.get('description', 'No description')
            priority = f"(P:{task.get('priority', 'N/A')})" if task.get('priority') else ""
            due_date = f"(D:{task.get('due_date', 'N/A')})" if task.get('due_date') else ""
            tags_str = f"(T:{', '.join(task.get('tags', []))})" if task.get('tags') else ""
            self.task_list.insert(tk.END, f"{status} {description} {priority} {due_date} {tags_str}")
            if task.get('completed'):
                self.task_list.itemconfig(i, fg="gray")

    def show_task_details(self, event):
        """Shows detailed information about the selected task."""
        selected_index = self.task_list.curselection()
        if selected_index:
            index = selected_index[0]
            task = self.tasks[index]
            details = f"Description: {task.get('description', 'N/A')}\n"
            details += f"Priority: {task.get('priority', 'N/A')}\n"
            details += f"Due Date: {task.get('due_date', 'N/A')}\n"
            details += f"Tags: {', '.join(task.get('tags', []))}\n"
            details += f"Completed: {'Yes' if task.get('completed', False) else 'No'}"
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert(tk.END, details)
            self.details_text.config(state=tk.DISABLED)

    def add_task(self):
        """Opens a dialog to add a new task."""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Task")

        tk.Label(add_window, text="Description:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        description_entry = tk.Entry(add_window, width=40)
        description_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(add_window, text="Priority:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        priority_entry = tk.Entry(add_window, width=40)
        priority_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(add_window, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        due_date_entry = tk.Entry(add_window, width=40)
        due_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(add_window, text="Tags (comma-separated):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        tags_entry = tk.Entry(add_window, width=40)
        tags_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        def save_new_task():
            description = description_entry.get().strip()
            if not description:
                messagebox.showerror("Error", "Description cannot be empty.")
                return
            priority = priority_entry.get().strip().capitalize()
            due_date = due_date_entry.get().strip()
            tags = [tag.strip() for tag in tags_entry.get().split(',') if tag.strip()]

            self.tasks.append({'description': description, 'completed': False, 'priority': priority, 'due_date': due_date, 'tags': tags})
            self.update_task_list()
            add_window.destroy()

        tk.Button(add_window, text="Save", command=save_new_task).grid(row=4, column=0, columnspan=2, pady=10)

    def edit_task(self):
        """Opens a dialog to edit the selected task."""
        selected_index = self.task_list.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a task to edit.")
            return

        index = selected_index[0]
        task = self.tasks[index].copy()  # Edit a copy to avoid direct modification

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")

        tk.Label(edit_window, text="Description:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        description_entry = tk.Entry(edit_window, width=40)
        description_entry.insert(0, task.get('description', ''))
        description_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(edit_window, text="Priority:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        priority_entry = tk.Entry(edit_window, width=40)
        priority_entry.insert(0, task.get('priority', ''))
        priority_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(edit_window, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        due_date_entry = tk.Entry(edit_window, width=40)
        due_date_entry.insert(0, task.get('due_date', ''))
        due_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        tk.Label(edit_window, text="Tags (comma-separated):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        tags_entry = tk.Entry(edit_window, width=40)
        tags_entry.insert(0, ', '.join(task.get('tags', [])))
        tags_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        completed_var = tk.BooleanVar(value=task.get('completed', False))
        completed_check = tk.Checkbutton(edit_window, text="Completed", variable=completed_var)
        completed_check.grid(row=4, column=0, columnspan=2, pady=5)

        def save_edited_task():
            description = description_entry.get().strip()
            if not description:
                messagebox.showerror("Error", "Description cannot be empty.")
                return
            priority = priority_entry.get().strip().capitalize()
            due_date = due_date_entry.get().strip()
            tags = [tag.strip() for tag in tags_entry.get().split(',') if tag.strip()]
            completed = completed_var.get()

            self.tasks[index] = {'description': description, 'completed': completed, 'priority': priority, 'due_date': due_date, 'tags': tags}
            self.update_task_list()
            edit_window.destroy()

        tk.Button(edit_window, text="Save", command=save_edited_task).grid(row=5, column=0, columnspan=2, pady=10)

    def mark_complete(self):
        """Marks the selected task as complete."""
        selected_index = self.task_list.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a task to mark as complete.")
            return
        index = selected_index[0]
        self.tasks[index]['completed'] = not self.tasks[index].get('completed', False)
        self.update_task_list()

    def delete_task(self):
        """Deletes the selected task after confirmation."""
        selected_index = self.task_list.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a task to delete.")
            return
        index = selected_index[0]
        task_to_delete = self.tasks[index].get('description', 'Task')
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{task_to_delete}'?"):
            del self.tasks[index]
            self.update_task_list()
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete("1.0", tk.END)
            self.details_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    gui = TodoGUI(root)
    root.mainloop()