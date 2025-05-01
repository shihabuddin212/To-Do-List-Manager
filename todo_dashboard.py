#!/usr/bin/env python3

import os
import time
from datetime import datetime
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.progress_bar import ProgressBar
from rich.text import Text
from rich import box
from todo import TodoList

class TodoDashboard:
    def __init__(self):
        self.console = Console()
        self.todo_list = TodoList()
        self.layout = Layout()
        self.setup_layout()
        
    def setup_layout(self):
        """Initialize the dashboard layout"""
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", size=15),
            Layout(name="footer", size=3)
        )
        
        self.layout["main"].split_row(
            Layout(name="tasks", ratio=2),
            Layout(name="stats", ratio=1),
        )
        
    def generate_header(self):
        """Create the dashboard header"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return Panel(
            Text("Todo List Dashboard", style="bold white", justify="center"),
            subtitle=Text(f"Last Updated: {current_time}", style="cyan"),
            box=box.ROUNDED,
            style="blue"
        )
        
    def generate_task_table(self):
        """Create the tasks table"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            title="Current Tasks",
            expand=True
        )
        
        table.add_column("ID", justify="center", style="cyan", width=4)
        table.add_column("Title", style="white")
        table.add_column("Status", justify="center", width=10)
        table.add_column("Created", justify="center", width=20)
        
        for task in self.todo_list.get_all_tasks():
            status_style = "green" if task["completed"] else "yellow"
            status = "✓ Done" if task["completed"] else "○ Pending"
            
            table.add_row(
                str(task["id"]),
                Text(task["title"], style="bold white"),
                Text(status, style=status_style),
                task["created_at"]
            )
            
        return Panel(table, box=box.ROUNDED, title="Task List", border_style="blue")
        
    def generate_stats(self):
        """Create the statistics panel"""
        tasks = self.todo_list.get_all_tasks()
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task["completed"])
        pending_tasks = total_tasks - completed_tasks
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        stats_table = Table(show_header=False, box=None, expand=True)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", justify="right")
        
        stats_table.add_row("Total Tasks", str(total_tasks))
        stats_table.add_row("Completed", Text(str(completed_tasks), style="green"))
        stats_table.add_row("Pending", Text(str(pending_tasks), style="yellow"))
        
        # Create progress bar for completion rate
        progress_bar = ProgressBar(
            completed=int(completion_rate),
            total=100,
            width=20,
            complete_style="green",
            pulse_style="yellow"
        )
        
        stats_table.add_row("Completion Rate", f"{completion_rate:.1f}%")
        stats_table.add_row("Progress", progress_bar)
        
        return Panel(
            stats_table,
            title="Statistics",
            border_style="blue",
            box=box.ROUNDED
        )
        
    def generate_footer(self):
        """Create the dashboard footer"""
        controls = [
            ("Q", "Quit"),
            ("A", "Add Task"),
            ("C", "Complete Task"),
            ("D", "Delete Task"),
            ("R", "Refresh"),
        ]
        
        footer_text = Text()
        for key, action in controls:
            footer_text.append(f"[{key}]", style="bold cyan")
            footer_text.append(f" {action}  ", style="white")
            
        return Panel(footer_text, box=box.ROUNDED, style="blue")
        
    def update_dashboard(self):
        """Update all dashboard components"""
        self.layout["header"].update(self.generate_header())
        self.layout["tasks"].update(self.generate_task_table())
        self.layout["stats"].update(self.generate_stats())
        self.layout["footer"].update(self.generate_footer())
        
    def add_task(self):
        """Add a new task"""
        self.console.print("\n[bold cyan]Enter task details:[/bold cyan]")
        title = input("Title: ").strip()
        description = input("Description (optional): ").strip()
        
        if title:
            self.todo_list.add_task(title, description)
            self.console.print("[green]Task added successfully![/green]")
        else:
            self.console.print("[red]Task title cannot be empty![/red]")
            
    def complete_task(self):
        """Mark a task as completed"""
        self.console.print("\n[bold cyan]Enter task ID to mark as completed:[/bold cyan]")
        task_id = input("Task ID: ").strip()
        
        if task_id.isdigit():
            if self.todo_list.mark_completed(int(task_id)):
                self.console.print("[green]Task marked as completed![/green]")
            else:
                self.console.print("[red]Task not found![/red]")
        else:
            self.console.print("[red]Invalid task ID![/red]")
            
    def delete_task(self):
        """Delete a task"""
        self.console.print("\n[bold cyan]Enter task ID to delete:[/bold cyan]")
        task_id = input("Task ID: ").strip()
        
        if task_id.isdigit():
            if self.todo_list.delete_task(int(task_id)):
                self.console.print("[green]Task deleted successfully![/green]")
            else:
                self.console.print("[red]Task not found![/red]")
        else:
            self.console.print("[red]Invalid task ID![/red]")
            
    def run(self):
        """Run the dashboard"""
        try:
            with Live(self.layout, refresh_per_second=4, screen=True):
                while True:
                    self.update_dashboard()
                    
                    command = self.console.input("\nEnter command: ").lower()
                    
                    if command == 'q':
                        break
                    elif command == 'a':
                        self.add_task()
                    elif command == 'c':
                        self.complete_task()
                    elif command == 'd':
                        self.delete_task()
                    elif command == 'r':
                        continue
                    else:
                        self.console.print("[red]Invalid command![/red]")
                        
        except KeyboardInterrupt:
            pass
            
        self.console.print("[yellow]Goodbye![/yellow]")


if __name__ == "__main__":
    # Install required packages if missing
    try:
        import rich
    except ImportError:
        import subprocess
        import sys
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
        
    dashboard = TodoDashboard()
    dashboard.run() 