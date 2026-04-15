class Todo:
    def __init__(self, id, title, description, priority, category, due_date, tags=None):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.category = category
        self.due_date = due_date
        self.tags = tags if tags is not None else []  # Initialize tags as an empty list if not provided

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'category': self.category,
            'due_date': self.due_date,
            'tags': self.tags  # Include tags in the dictionary representation
        }