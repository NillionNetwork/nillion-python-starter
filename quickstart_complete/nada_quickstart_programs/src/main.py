from datetime import datetime

def display_tasks(tasks):
    if not tasks:
        print("Your to-do list is empty.")
        return
    
    print("Your To-Do List:")
    for index, task in enumerate(tasks, start=1):
        status = "Done" if task['done'] else "Not done"
        priority = task['priority']
        due_date = task['due_date'] if task['due_date'] else "No due date"
        print(f"{index}. {task['task']} - [{status}] (Priority: {priority}) (Due: {due_date})")

def add_task(tasks):
    task = input("Enter a new task: ")
    priority = input("Enter priority (low, medium, high): ").lower()
    if priority not in ["low", "medium", "high"]:
        priority = "low"
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
    try:
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date() if due_date else None
    except ValueError:
        print("Invalid date format. No due date set.")
        due_date = None
    tasks.append({"task": task, "done": False, "priority": priority, "due_date": due_date})
    print(f"Task '{task}' added with priority '{priority}' and due date '{due_date}'.")

def remove_task(tasks):
    task_number = int(input("Enter the number of the task to remove: "))
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        print(f"Task '{removed_task['task']}' removed.")
    else:
        print("Invalid task number.")

def mark_task_done(tasks):
    task_number = int(input("Enter the number of the task to mark as done: "))
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]['done'] = True
        print(f"Task '{tasks[task_number - 1]['task']}' marked as done.")
    else:
        print("Invalid task number.")

def edit_task(tasks):
    task_number = int(input("Enter the number of the task to edit: "))
    if 0 < task_number <= len(tasks):
        task = tasks[task_number - 1]
        new_task = input(f"Enter new task description (current: '{task['task']}') or press Enter to keep it: ")
        new_priority = input(f"Enter new priority (low, medium, high) (current: '{task['priority']}') or press Enter to keep it: ").lower()
        new_due_date = input(f"Enter new due date (YYYY-MM-DD) (current: '{task['due_date']}') or press Enter to keep it: ")
        
        if new_task:
            task['task'] = new_task
        if new_priority in ["low", "medium", "high"]:
            task['priority'] = new_priority
        if new_due_date:
            try:
                task['due_date'] = datetime.strptime(new_due_date, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Due date not changed.")
        print("Task updated.")
    else:
        print("Invalid task number.")

def sort_tasks(tasks, by):
    if by == 'priority':
        tasks.sort(key=lambda x: ['low', 'medium', 'high'].index(x['priority']))
    elif by == 'status':
        tasks.sort(key=lambda x: x['done'])
    elif by == 'due_date':
        tasks.sort(key=lambda x: (x['due_date'] is None, x['due_date']))
    print(f"Tasks sorted by {by}.")

def save_tasks(tasks, filename="tasks.txt"):
    with open(filename, "w") as file:
        for task in tasks:
            file.write(f"{task['task']}|{task['done']}|{task['priority']}|{task['due_date']}\n")
    print("Tasks saved to file.")

def load_tasks(filename="tasks.txt"):
    tasks = []
    try:
        with open(filename, "r") as file:
            for line in file:
                task, done, priority, due_date = line.strip().split("|")
                due_date = datetime.strptime(due_date, "%Y-%m-%d").date() if due_date != 'None' else None
                tasks.append({"task": task, "done": done == "True", "priority": priority, "due_date": due_date})
    except FileNotFoundError:
        print("No saved tasks found.")
    return tasks

def main():
    tasks = load_tasks()
    while True:
        print("\nOptions:")
        print("1. View tasks")
        print("2. Add task")
        print("3. Remove task")
        print("4. Mark task as done")
        print("5. Edit task")
        print("6. Sort tasks by priority")
        print("7. Sort tasks by status")
        print("8. Sort tasks by due date")
        print("9. Save tasks")
        print("10. Quit")
        
        choice = input("Select an option (1-10): ")
        
        if choice == '1':
            display_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            remove_task(tasks)
        elif choice == '4':
            mark_task_done(tasks)
        elif choice == '5':
            edit_task(tasks)
        elif choice == '6':
            sort_tasks(tasks, 'priority')
        elif choice == '7':
            sort_tasks(tasks, 'status')
        elif choice == '8':
            sort_tasks(tasks, 'due_date')
        elif choice == '9':
            save_tasks(tasks)
        elif choice == '10':
            save_tasks(tasks)
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()


