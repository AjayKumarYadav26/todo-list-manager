from flask import Flask, jsonify, request
from models import Todo
from storage import load_todos, save_todos
from services import normalize_tags, get_popular_tags

app = Flask(__name__)


def _find_todo(todos, todo_id):
    return next((todo for todo in todos if todo.get('id') == todo_id), None)


@app.get('/todos')
def list_todos():
    todos = load_todos()
    return jsonify(todos), 200


@app.post('/todos')
def create_todo():
    payload = request.get_json(silent=True) or {}
    title = (payload.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    todos = load_todos()
    todo = Todo.from_payload(payload, next_id=todos)
    todos.append(todo)
    save_todos(todos)
    return jsonify(todo), 201


@app.put('/todos/<todo_id>')
def update_todo(todo_id):
    payload = request.get_json(silent=True) or {}
    todos = load_todos()
    todo = _find_todo(todos, todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    if 'title' in payload:
        title = (payload.get('title') or '').strip()
        if not title:
            return jsonify({'error': 'Title is required'}), 400
        todo['title'] = title

    for field in ['description', 'priority', 'category', 'due_date', 'completed']:
        if field in payload:
            todo[field] = payload[field]

    if 'tags' in payload:
        todo['tags'] = normalize_tags(payload.get('tags'))

    save_todos(todos)
    return jsonify(todo), 200


@app.get('/tags')
def popular_tags():
    todos = load_todos()
    return jsonify(get_popular_tags(todos)), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
