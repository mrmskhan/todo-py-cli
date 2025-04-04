import click  # to create a CLI
import json   # to save and load tasks from a file
import os     # to check if the file exists

TODO_FILE = "todo.json"

def load_tasks():
    if not os.path.exists(TODO_FILE):  # اگر فائل موجود نہ ہو
        return []
    with open(TODO_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@click.group()
def cli():
    """Simple Todo List Manager"""
    pass

@click.command()
@click.argument("task")
def add(task):         
    """Add a new task to the list"""
    tasks = load_tasks()
    tasks.append({"task": task, "done": False})  # یہاں درست کیا
    save_tasks(tasks)
    click.echo(f"Task added successfully: {task}")



@click.command()
def list():
    """list all the tasks"""
    tasks = load_tasks()
    if not tasks:
        click.echo("No Tasks Found")
        return
    for index, task in enumerate(tasks, 1):
        status = "✅" if task['done'] else '❌'
        click.echo(f"{index}. {task['task']} [{status}]")


@click.command()
@click.argument("task_number", type=int)
def complete(task_number):
    """Mark a task as completed"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        click.echo(f"Task {task_number} marked as completed.")
    else:
        click.echo(f"Invalid task number: {task_number}")

@click.command()
@click.argument("task_number", type=int)
def remove(task_number):
    """Remove a task from the list"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        removed_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        click.echo(f"Removed task: {removed_task['task']}")
    else:
        click.echo(f"Invalid task number")


@click.command()
@click.argument("task_number", type=int)
@click.argument("new_task")
def update(task_number, new_task):
    """Update an existing task"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks):
        old_task = tasks[task_number - 1]["task"]
        tasks[task_number - 1]["task"] = new_task
        save_tasks(tasks)
        click.echo(f"✏️ Updated task {task_number}: '{old_task}' ➡️ '{new_task}'")
    else:
        click.echo("❌ Invalid task number.")


@click.command()
def clear():
    """Remove all tasks"""
    if os.path.exists(TODO_FILE):
        save_tasks([])
        click.echo("🧹 All tasks cleared!")
    else:
        click.echo("📭 No tasks to clear.")


cli.add_command(add)
cli.add_command(list)
cli.add_command(complete)
cli.add_command(remove)
cli.add_command(update)
cli.add_command(clear)


if __name__ == "__main__":
    cli()        