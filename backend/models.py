class Todo:
    def __init__(self, id, title, description, status, priority, category, due_date, created_at, updated_at, completed_at, tags=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.category = category
        self.due_date = due_date
        self.created_at = created_at
        self.updated_at = updated_at
        self.completed_at = completed_at
        self.tags = tags if tags is not None else []  # Initialize tags as an empty list

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'category': self.category,
            'due_date': self.due_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'completed_at': self.completed_at,
            'tags': self.tags
        }