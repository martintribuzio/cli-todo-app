# main.py

import sys
import os
import questionary

from questionary import Choice
from rich.console import Console
from rich.table import Table

src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)

from modules.tasks import tasks
from modules.logger.logger import logger
from modules.utils.constants import HIGH_PRIORITY, MEDIUM_PRIORITY, LOW_PRIORITY, COMPLETED_STATE, COMPLETE_TASK, DELETE_TASK, SHOW_TASKS_OPTION, ADD_TASK_OPTION, COMPLETE_TASK_OPTION, DELETE_TASK_OPTION, EXIT_OPTION

console = Console()

def show_tasks():
    task_list = tasks.list_tasks()

    if not task_list:
        console.print("\n [yellow] No hay tareas para mostrar! [/yellow]☹️ \n")
        return

    table = Table(title="Gestor de tareas")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Título", style="cyan", no_wrap=True)
    table.add_column("Descripcion", style="magenta", no_wrap=True)
    table.add_column("Prioridad", style="magenta", justify="right")
    table.add_column("Estado", style="green", justify="right")

    for task in task_list:
        priority_color = ""

        if task['priority'] == HIGH_PRIORITY:
            priority_color = "red"
        elif task['priority'] == MEDIUM_PRIORITY:
            priority_color = "yellow"
        else:
            priority_color = "green"

        state_color = "bold green" if task['state'] == COMPLETED_STATE else "bold"
        
        table.add_row(
            str(task['id']),
            task['title'],
            task['description'],
            f"[{priority_color}]{task['priority']}[/{priority_color}]",
            f"[{state_color}]{task['state']}[/{state_color}]"
        )
    
    console.print(table)

def add_task():
    console.print("\n[bold blue] Agregando nueva tarea... [/bold blue] ✏️\n")

    title = questionary.text("Titulo de la tarea:").ask()
    description = questionary.text("Descripcion de la tarea:").ask()

    priority = questionary.select(
        "Prioridad de la tarea:",
        choices=[HIGH_PRIORITY, MEDIUM_PRIORITY, LOW_PRIORITY],
        default=MEDIUM_PRIORITY
    ).ask()

    if title and description and priority:
        tasks.add_task(title, description, priority)
        console.print("[bold green] Tarea agregada con exito [/bold green] ✅😁\n")
    else:
        console.print("[bold red] Falto completar algunos datos [/bold red] 🤔\n")

def get_and_update_task(action):
    tasks_list = tasks.list_tasks()

    if not tasks_list:
        console.print("[yellow]No hay tareas para modificar[/yellow] 😅\n")
        return
    
    tasks_options = [
        Choice(
            title=f"{task['id']}: {task['title']} - {task['priority']} - {task['state']}", 
            value=task['id']
        ) for task in tasks_list
    ]
    
    selected_task = questionary.select(f"Elige la tarea a {action}: 🧐", choices=tasks_options).ask()
    
    if selected_task is not None:
        if action == COMPLETE_TASK:
            tasks.complete_task(selected_task)
            console.print(f"[green] Tarea marcada como completada [/green]✅🤟")

        elif action == DELETE_TASK:
            tasks.delete_task(selected_task)
            console.print(f"[green] Tarea eliminada con exito![/green]✅🤟")

def main():
    logger.info("App iniciada")

    try:
        while True:
            console.print("[green] ###### Gestor de tareas CLI ###### 📃✏️ [/green]\n")

            option = questionary.select(
                "Elegi una opcion:",
                choices=[
                    Choice(title='1. Ver todas las tareas', value=SHOW_TASKS_OPTION),
                    Choice(title='2. Agregar una nueva tarea', value=ADD_TASK_OPTION),
                    Choice(title='3. Marcar una tarea como completada', value=COMPLETE_TASK_OPTION),
                    Choice(title='4. Eliminar una tarea', value=DELETE_TASK_OPTION),
                    Choice(title='5. Salir', value=EXIT_OPTION)
                ]
            ).ask()

            if option is None:
                break

            if option == SHOW_TASKS_OPTION:
                show_tasks()
            elif option == ADD_TASK_OPTION:
                add_task()
            elif option == COMPLETE_TASK_OPTION:
                get_and_update_task(COMPLETE_TASK)
            elif option == DELETE_TASK_OPTION:
                get_and_update_task(DELETE_TASK)
            elif option == EXIT_OPTION or option is None:
                break

    except KeyboardInterrupt:
        console.print("\n[bold red] Saliendo de la aplicacion... [/bold red]\n")

    finally:
        logger.info("App cerrada")

if __name__ == "__main__":
    main()