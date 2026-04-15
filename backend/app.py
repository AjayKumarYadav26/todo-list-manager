from flask import Flask, request, jsonify
from models import Todo
from storage import TodoStorage

app = Flask(__name__)
storage = TodoStorage()

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    todo = Todo(
        id=len(storage.get_todos()) + 1,
        title=data['title'],
        description=data['description'],
        priority=data['priority'],
        category=data['category'],
        due_date=data['due_date'],
        tags=data.get('tags', [])  # Get tags from request
    )
    storage.add_todo(todo)
    return jsonify(todo.to_dict()), 201

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(storage.get_todos()), 200

@app.route('/todos/filter', methods=['GET'])
def filter_todos_by_tag():
    tag = request.args.get('tag')
    filtered_todos = storage.filter_todos_by_tag(tag)
    return jsonify(filtered_todos), 200

if __name__ == '__main__':
    app.run(port=5050)