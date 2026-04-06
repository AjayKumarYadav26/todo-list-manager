from flask import Flask, request, jsonify, render_template
from storage import StorageManager
from models import create_todo, validate_update, compute_stats, matches_filters, sort_todos

app = Flask(__name__)
store = StorageManager()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/todos", methods=["GET"])
def list_todos():
    todos = store.get_all_todos()

    filters = {
        "status": request.args.get("status"),
        "priority": request.args.get("priority"),
        "category": request.args.get("category"),
        "search": request.args.get("search"),
    }
    filters = {k: v for k, v in filters.items() if v}

    if filters:
        todos = [t for t in todos if matches_filters(t, filters)]

    sort_by = request.args.get("sort_by", "created_at")
    sort_order = request.args.get("sort_order", "desc")
    todos = sort_todos(todos, sort_by, sort_order)

    return jsonify(todos)


@app.route("/api/todos/<todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = store.get_todo(todo_id)
    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo)


@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400
    try:
        todo = create_todo(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    saved = store.add_todo(todo)
    return jsonify(saved), 201


@app.route("/api/todos/<todo_id>", methods=["PUT"])
def update_todo(todo_id):
    existing = store.get_todo(todo_id)
    if not existing:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        updates = validate_update(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    updated = store.update_todo(todo_id, updates)
    return jsonify(updated)


@app.route("/api/todos/<todo_id>", methods=["PATCH"])
def patch_todo(todo_id):
    existing = store.get_todo(todo_id)
    if not existing:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    try:
        updates = validate_update(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    updated = store.update_todo(todo_id, updates)
    return jsonify(updated)


@app.route("/api/todos/<todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    if store.delete_todo(todo_id):
        return jsonify({"message": "Todo deleted"})
    return jsonify({"error": "Todo not found"}), 404


@app.route("/api/todos", methods=["DELETE"])
def bulk_delete():
    if request.args.get("completed") == "true":
        count = store.delete_completed()
        return jsonify({"message": f"Deleted {count} completed todo(s)", "count": count})
    return jsonify({"error": "Use ?completed=true to bulk delete"}), 400


@app.route("/api/categories", methods=["GET"])
def list_categories():
    return jsonify(store.get_categories())


@app.route("/api/stats", methods=["GET"])
def get_stats():
    todos = store.get_all_todos()
    stats = compute_stats(todos)
    return jsonify(stats)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
