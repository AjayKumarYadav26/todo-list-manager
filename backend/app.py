from flask import Flask, request, jsonify
from storage import load_todos, save_todos

app = Flask(__name__)

@app.route('/todos/<id>/tags', methods=['POST'])
def add_tags(id):
    todo = load_todos().get(id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    tags = request.json.get('tags', [])
    todo['tags'] = list(set(todo.get('tags', []) + tags))  # Add new tags and avoid duplicates
    save_todos()
    return jsonify(todo), 200

@app.route('/todos/tags', methods=['GET'])
def get_tags():
    todos = load_todos().values()
    tag_counts = {}
    for todo in todos:
        for tag in todo.get('tags', []):
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    return jsonify(tag_counts), 200

@app.route('/todos', methods=['GET'])
def filter_todos_by_tag():
    tag = request.args.get('tag')
    todos = load_todos().values()
    filtered_todos = [todo for todo in todos if tag in todo.get('tags', [])]
    return jsonify(filtered_todos), 200
