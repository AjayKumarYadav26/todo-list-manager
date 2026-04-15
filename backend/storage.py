import json

TODO_FILE = 'data/todos.json'


def load_todos():
    with open(TODO_FILE, 'r') as f:
        return json.load(f)['todos']


def save_todos(todos):
    with open(TODO_FILE, 'w') as f:
        json.dump({'todos': todos}, f, indent=4)

