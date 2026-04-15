import json

class TodoStorage:
    def __init__(self, filename='data/todos.json'):
        self.filename = filename
        self.load_todos()

    def load_todos(self):
        try:
            with open(self.filename, 'r') as file:
                self.todos = json.load(file)
        except FileNotFoundError:
            self.todos = []

    def save_todos(self):
        with open(self.filename, 'w') as file:
            json.dump(self.todos, file, indent=4)

    def add_todo(self, todo):
        self.todos.append(todo.to_dict())
        self.save_todos()

    def get_todos(self):
        return self.todos

    def filter_todos_by_tag(self, tag):
        return [todo for todo in self.todos if tag in todo.get('tags', [])]