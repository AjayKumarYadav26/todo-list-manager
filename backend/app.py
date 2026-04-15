from flask import Flask, jsonify, request
from models import Todo
import json

app = Flask(__name__)

# Load existing todos from JSON file

def load_todos():
    with open('data/todos.json', 'r') as f:
        return json.load(f)

# Save todos to JSON file

def save_todos(todos):
    with open('data/todos.json', 'w') as f:
        json.dump(todos, f)

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = Todo(
        id=data['id'],
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        category=data['category'],
        due_date=data['due_date'],
        tags=data.get('tags', [])  # Get tags from request, default to empty list
    )
    todos = load_todos()
    todos.append(new_todo.to_dict())
    save_todos(todos)
    return jsonify(new_todo.to_dict()), 201

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = load_todos()
    return jsonify(todos)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['title'] = data.get('title', todo['title'])
            todo['description'] = data.get('description', todo['description'])
            todo['priority'] = data.get('priority', todo['priority'])
            todo['category'] = data.get('category', todo['category'])
            todo['due_date'] = data.get('due_date', todo['due_date'])
            todo['tags'] = data.get('tags', todo['tags'])  # Update tags
            save_todos(todos)
            return jsonify(todo)
    return jsonify({'error': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(port=5050)