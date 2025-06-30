from modules.database import database
from modules.logger.logger import logger
from modules.utils.constants import PENDING_STATE, COMPLETED_STATE

"""
    Agrega una nueva tarea a la lista
"""
def add_task(title, description, priority):
    tasks = database.get_tasks()

    id = database.get_next_id()

    new_task = {
        "id": id,
        "title": title, # 
        "description": description,
        "priority": priority,
        "state": PENDING_STATE,
    }

    tasks.append(new_task)
    database.save_tasks(tasks)

    logger.info(f"Tarea agregada: ID={new_task['id']}, Título='{title}'")

    return new_task

"""
    Muestra todas las tareas.
"""

def list_tasks():
    return database.get_tasks()


"""
    Borro una tarea por ID
"""
def delete_task(task_id):
    tasks = database.get_tasks()

    new_tasks_list = [task for task in tasks if task['id'] != task_id]

    if len(new_tasks_list) < len(tasks):
        database.save_tasks(new_tasks_list)

        logger.info(f"Tarea eliminada: ID={task_id}")

        return True
    else:
        return False

"""
    Marca una tarea como completada por su ID.
"""
def complete_task(task_id):
    tasks = database.get_tasks()
    task_found = False
    
    for task in tasks:
        if task['id'] == task_id:

            task['state'] = COMPLETED_STATE
            task_found = True
            break

    if task_found:
        database.save_tasks(tasks)

        logger.info(f"Tarea completada: ID={task_id}")

        return True
    else:
        return False