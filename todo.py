#!/usr/bin/env python3

import os
import json
from datetime import datetime

class TodoList:
    def __init__(self, file_path="tasks.json"):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []

    def save_tasks(self):
        """Save tasks to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(self.tasks, file, indent=2)

    def add_task(self, title, description=""):
        """Add a new task to the list."""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": None
        }
        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_all_tasks(self):
        """Return all tasks."""
        return self.tasks

    def get_task_by_id(self, task_id):
        """Get a task by its ID."""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def mark_completed(self, task_id):
        """Mark a task as completed."""
        task = self.get_task_by_id(task_id)
        if task:
            task["completed"] = True
            task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            # Reassign IDs to maintain order
            for i, task in enumerate(self.tasks):
                task["id"] = i + 1
            self.save_tasks()
            return True
        return False

def print_task(task):
    """Format and print a task."""
    status = "✓" if task["completed"] else "✗"
    print(f"[{status}] {task['id']}. {task['title']}")
    if task["description"]:
        print(f"   Description: {task['description']}")
    print(f"   Created: {task['created_at']}")
    if task["completed"]:
        print(f"   Completed: {task['completed_at']}")
    print()

def main():
    todo_list = TodoList()
    
    while True:
        print("\n===== Todo List Manager =====")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description (optional): ")
            task = todo_list.add_task(title, description)
            print(f"\nTask added with ID: {task['id']}")
            
        elif choice == "2":
            tasks = todo_list.get_all_tasks()
            if not tasks:
                print("\nNo tasks found.")
            else:
                print("\n--- Your Tasks ---")
                for task in tasks:
                    print_task(task)
                    
        elif choice == "3":
            task_id = input("Enter task ID to mark as completed: ")
            if task_id.isdigit():
                if todo_list.mark_completed(int(task_id)):
                    print(f"\nTask {task_id} marked as completed.")
                else:
                    print(f"\nTask with ID {task_id} not found.")
            else:
                print("\nInvalid task ID.")
                
        elif choice == "4":
            task_id = input("Enter task ID to delete: ")
            if task_id.isdigit():
                if todo_list.delete_task(int(task_id)):
                    print(f"\nTask {task_id} deleted.")
                else:
                    print(f"\nTask with ID {task_id} not found.")
            else:
                print("\nInvalid task ID.")
                
        elif choice == "5":
            print("\nGoodbye!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main() 