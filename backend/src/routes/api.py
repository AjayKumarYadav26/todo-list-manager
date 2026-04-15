from flask import Flask, request, jsonify
from models.schema import Todo

app = Flask(__name__)

todos = []

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    todo = Todo(id=len(todos)+1, title=data['title'], description=data['description'], tags=data.get('tags', []))
    todos.append(todo)
    return jsonify({'id': todo.id}), 201

@app.route('/todos/<int:todo_id>', methods=['PATCH'])
def update_todo_tags(todo_id):
    data = request.json
    todo = next((t for t in todos if t.id == todo_id), None)
    if todo:
        if 'tags' in data:
            todo.tags = data['tags']
        return jsonify({'tags': todo.tags}), 200
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify([{'id': t.id, 'title': t.title, 'tags': t.tags} for t in todos]), 200

if __name__ == '__main__':
    app.run(port=5050)