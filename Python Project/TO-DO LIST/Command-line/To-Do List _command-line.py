import os
import json  # For more robust saving/loading

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_tasks(tasks):
    """Displays the current to-do list with index and status summary."""
    if not tasks:
        print("\nYour to-do list is empty!\n")
        return

    print("\n--- Your To-Do List ---")
    completed_count = sum(1 for task in tasks if task.get('completed', False))
    print(f"Total tasks: {len(tasks)}, Completed: {completed_count}")
    for index, task in enumerate(tasks):
        status = "[X]" if task.get('completed', False) else "[ ]"
        description = task.get('description', 'No description')
        priority = f"(Priority: {task.get('priority', 'N/A')})" if task.get('priority') else ""
        due_date = f"(Due: {task.get('due_date', 'N/A')})" if task.get('due_date') else ""
        tags_str = f"(Tags: {', '.join(task.get('tags', []))})" if task.get('tags') else ""
        print(f"{index + 1}. {status} {description} {priority} {due_date} {tags_str}")
    print("-----------------------\n")

def get_valid_input(prompt, input_type=str, error_message="Invalid input. Please try again."):
    """Gets valid input from the user with type checking."""
    while True:
        user_input = input(prompt).strip()
        try:
            if input_type == int:
                return int(user_input)
            elif input_type == str:
                return user_input
            elif input_type == list:
                return [tag.strip() for tag in user_input.split(',')] if user_input else []
            else:
                return user_input  # Default to string
        except ValueError:
            print(error_message)

def add_task(tasks):
    """Adds a new task with description, priority, due date, and tags."""
    description = get_valid_input("Enter the task description: ")
    if not description:
        print("Task description cannot be empty.\n")
        return

    priority = get_valid_input("Enter priority (High, Medium, Low, or leave blank): ").strip().capitalize()
    if priority not in ["High", "Medium", "Low", ""]:
        print("Invalid priority level.\n")
        priority = None

    due_date = get_valid_input("Enter due date (YYYY-MM-DD or leave blank): ").strip()
    # Basic due date validation (you could use a more robust date parsing library)
    if due_date and not all(part.isdigit() and len(part) in [2, 4] for i, part in enumerate(due_date.split('-')) if i < 3 and (i == 0 and len(part) == 4 or len(part) == 2) and len(due_date.split('-')) == 3):
        print("Invalid date format. Please use YYYY-MM-DD.\n")
        due_date = None

    tags = get_valid_input("Enter tags (comma-separated, or leave blank): ", input_type=list)

    tasks.append({'description': description, 'completed': False, 'priority': priority, 'due_date': due_date, 'tags': tags})
    print(f"Task '{description}' added successfully!\n")

def mark_complete(tasks):
    """Marks a task as complete with error handling."""
    display_tasks(tasks)
    if not tasks:
        return
    try:
        task_number = get_valid_input("Enter the number of the task to mark as complete: ", input_type=int) - 1
        if 0 <= task_number < len(tasks):
            tasks[task_number]['completed'] = True
            print(f"Task '{tasks[task_number].get('description', 'Task')}' marked as complete!\n")
        else:
            print("Invalid task number. Please enter a number from the list.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")

def delete_task(tasks):
    """Deletes a task from the to-do list with confirmation."""
    display_tasks(tasks)
    if not tasks:
        return
    try:
        task_number = get_valid_input("Enter the number of the task to delete: ", input_type=int) - 1
        if 0 <= task_number < len(tasks):
            task_to_delete = tasks[task_number].get('description', 'Task')
            confirm = get_valid_input(f"Are you sure you want to delete task '{task_to_delete}'? (y/n): ").lower()
            if confirm == 'y':
                deleted_task = tasks.pop(task_number)
                print(f"Task '{deleted_task.get('description', 'Task')}' deleted successfully!\n")
            else:
                print("Deletion cancelled.\n")
        else:
            print("Invalid task number. Please enter a number from the list.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")

def edit_task(tasks):
    """Allows the user to edit the description, priority, and due date of an existing task."""
    display_tasks(tasks)
    if not tasks:
        return
    try:
        task_number = get_valid_input("Enter the number of the task to edit: ", input_type=int) - 1
        if 0 <= task_number < len(tasks):
            task = tasks[task_number]
            print(f"\nEditing task: {task.get('description', 'Task')}")
            new_description = get_valid_input(f"Enter new description (leave blank to keep '{task.get('description', '')}'): ")
            if new_description:
                task['description'] = new_description

            priority = get_valid_input(f"Enter new priority (High, Medium, Low, blank to keep '{task.get('priority', 'N/A')}'): ").strip().capitalize()
            if priority in ["High", "Medium", "Low", ""]:
                task['priority'] = priority or None
            elif priority is not None:
                print("Invalid priority level.\n")

            due_date = get_valid_input(f"Enter new due date (YYYY-MM-DD, blank to keep '{task.get('due_date', 'N/A')}'): ").strip()
            if due_date and not all(part.isdigit() and len(part) in [2, 4] for i, part in enumerate(due_date.split('-')) if i < 3 and (i == 0 and len(part) == 4 or len(part) == 2) and len(due_date.split('-')) == 3):
                print("Invalid date format. Please use YYYY-MM-DD.\n")
            else:
                task['due_date'] = due_date or None

            tags = get_valid_input(f"Enter new tags (comma-separated, blank to keep '{', '.join(task.get('tags', [])) if task.get('tags') else 'N/A'}'): ", input_type=list)
            if tags is not None:
                task['tags'] = tags

            print("Task updated successfully!\n")
        else:
            print("Invalid task number. Please enter a number from the list.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")

def save_tasks(tasks, filename="todo.json"):
    """Saves the to-do list to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump(tasks, f, indent=4)
        print(f"Tasks saved to {filename}\n")
    except IOError:
        print(f"Error saving tasks to {filename}\n")

def load_tasks(filename="todo.json"):
    """Loads the to-do list from a JSON file."""
    tasks = []
    try:
        with open(filename, "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        print("No existing to-do list found. Starting with an empty list.\n")
    except json.JSONDecodeError:
        print("Error decoding the to-do list file. Starting with an empty list.\n")
    return tasks

def main():
    """Main function to run the to-do list application with numbered choices."""
    todo_list = load_tasks()

    while True:
        clear_screen()
        display_tasks(todo_list)

        print("Available actions:")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark as complete")
        print("4. Delete task")
        print("5. Edit task")
        print("6. Save tasks")
        print("7. Exit")

        choice = get_valid_input("Enter your choice: ", input_type=int, error_message="Invalid choice. Please enter a number from the menu.")

        if choice == 1:
            add_task(todo_list)
        elif choice == 2:
            pass  # display_tasks() is already called at the beginning of the loop
        elif choice == 3:
            mark_complete(todo_list)
        elif choice == 4:
            delete_task(todo_list)
        elif choice == 5:
            edit_task(todo_list)
        elif choice == 6:
            save_tasks(todo_list)
        elif choice == 7:
            print("Exiting the to-do list application. Goodbye!\n")
            break
        else:
            print("Invalid choice. Please enter a number from the menu.\n")

        input("Press Enter to continue...")

if __name__ == "__main__":
    main()