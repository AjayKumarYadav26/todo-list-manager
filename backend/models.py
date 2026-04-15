from services import normalize_tags


class Todo:
    @staticmethod
    def from_payload(payload, next_id):
        todos = next_id if isinstance(next_id, list) else []
        max_id = 0
        for todo in todos:
            try:
                max_id = max(max_id, int(todo.get('id', 0)))
            except (TypeError, ValueError):
                continue

        return {
            'id': str(max_id + 1),
            'title': (payload.get('title') or '').strip(),
            'description': payload.get('description', ''),
            'priority': payload.get('priority', 'medium'),
            'category': payload.get('category', ''),
            'due_date': payload.get('due_date', ''),
            'completed': bool(payload.get('completed', False)),
            'tags': normalize_tags(payload.get('tags')),
        }
