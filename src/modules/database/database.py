import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = os.path.join(current_dir, "tasks.json")

"""
    Trae la lista de tareas del el JSON
"""
def get_tasks():
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error al cargar las tareas: {e}")
        return []

"""
    Guarda la lista de tareas en el JSON
"""
def save_tasks(tasks):
    try:
        with open(DATABASE_FILE, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

"""
    Retorno el siguiente ID
"""
def get_next_id():
    tasks = get_tasks()

    if not tasks:
        return 1

    max_id = max(task['id'] for task in tasks)
    return max_id + 1