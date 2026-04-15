import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'todos.json')


def load_todos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        try:
            todos = json.load(file)
        except json.JSONDecodeError:
            return []
    normalized = []
    for todo in todos:
        normalized.append({
            'id': str(todo.get('id', '')),
            'title': todo.get('title', ''),
            'description': todo.get('description', ''),
            'priority': todo.get('priority', 'medium'),
            'category': todo.get('category', ''),
            'due_date': todo.get('due_date', ''),
            'completed': bool(todo.get('completed', False)),
            'tags': todo.get('tags', []) or [],
        })
    return normalized


def save_todos(todos):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(todos, file, indent=2)
