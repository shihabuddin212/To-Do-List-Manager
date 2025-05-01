# Todo List Manager

A simple Todo List Manager written in Python, available in both command-line and GUI versions.

## Features

- Add tasks with titles and optional descriptions
- View all tasks with their status
- Mark tasks as completed
- Delete tasks
- Persistent storage using JSON
- Two interfaces: Command-line and GUI

## Requirements

- Python 3.6 or higher
- PyQt5 (for GUI version)

## Installation

Install PyQt5 for the GUI version:

```bash
pip install PyQt5
```

## Usage

### Command-line Version

Run the command-line application with:

```bash
python todo.py
```

#### Menu Options

1. **Add Task**: Add a new task with a title and optional description
2. **View All Tasks**: Display all tasks with their details
3. **Mark Task as Completed**: Mark a task as completed by its ID
4. **Delete Task**: Remove a task by its ID
5. **Exit**: Close the application

### GUI Version

Run the GUI application with:

```bash
python todo_gui.py
```

The GUI provides the following functionality:
- **Add Task**: Click the "Add Task" button to create a new task
- **Mark Completed**: Select a task and click "Mark Completed"
- **Delete Task**: Select a task and click "Delete Task"
- Tasks are displayed in a list with completed tasks shown in green

## Data Storage

Tasks are stored in a `tasks.json` file in the same directory as the script and are shared between both versions. 