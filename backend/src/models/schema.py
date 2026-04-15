from typing import List

class Todo:
    def __init__(self, id: int, title: str, description: str, tags: List[str] = None):
        self.id = id
        self.title = title
        self.description = description
        self.tags = tags if tags is not None else []

    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        if tag in self.tags:
            self.tags.remove(tag)

    def __repr__(self):
        return f"<Todo {self.id}: {self.title}, Tags: {self.tags}>"