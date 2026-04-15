import json
import os
import tempfile
import threading


DEFAULT_DATA = {
    "todos": [],
    "categories": ["Work", "Personal", "Shopping", "Health"],
}


class StorageManager:
    def __init__(self, filepath="data/todos.json"):
        self.filepath = filepath
        self._lock = threading.Lock()
        self._data = None
        self._load()

    def _normalize_todo(self, todo: dict) -> dict:
        normalized = dict(todo)
        normalized.setdefault("tags", [])
        if not isinstance(normalized["tags"], list):
            normalized["tags"] = []
        normalized["tags"] = [str(tag).strip() for tag in normalized["tags"] if str(tag).strip()]
        return normalized

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                self._data.setdefault("todos", [])
                self._data.setdefault("categories", list(DEFAULT_DATA["categories"]))
                self._data["todos"] = [self._normalize_todo(todo) for todo in self._data.get("todos", [])]
            except (json.JSONDecodeError, IOError):
                self._data = {**DEFAULT_DATA}
                self._save()
        else:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            self._data = {**DEFAULT_DATA, "todos": [], "categories": list(DEFAULT_DATA["categories"])}
            self._save()

    def _save(self):
        dir_name = os.path.dirname(self.filepath)
        fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, self.filepath)
        except Exception:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

    def get_all_todos(self) -> list:
        with self._lock:
            return [dict(t) for t in self._data.get("todos", [])]

    def get_todo(self, todo_id: str) -> dict | None:
        with self._lock:
            for t in self._data.get("todos", []):
                if t["id"] == todo_id:
                    return dict(t)
        return None

    def add_todo(self, todo: dict) -> dict:
        with self._lock:
            todo = self._normalize_todo(todo)
            self._data["todos"].append(todo)
            if todo.get("category"):
                self._ensure_category(todo["category"])
            self._save()
            return dict(todo)

    def update_todo(self, todo_id: str, updates: dict) -> dict | None:
        with self._lock:
            for t in self._data["todos"]:
                if t["id"] == todo_id:
                    if "tags" in updates:
                        updates = dict(updates)
                        updates["tags"] = [str(tag).strip() for tag in updates.get("tags", []) if str(tag).strip()]
                    t.update(updates)
                    if "category" in updates and updates["category"]:
                        self._ensure_category(updates["category"])
                    self._save()
                    return dict(t)
        return None

    def delete_todo(self, todo_id: str) -> bool:
        with self._lock:
            before = len(self._data["todos"])
            self._data["todos"] = [t for t in self._data["todos"] if t["id"] != todo_id]
            if len(self._data["todos"]) < before:
                self._save()
                return True
            return False

    def delete_completed(self) -> int:
        with self._lock:
            before = len(self._data["todos"])
            self._data["todos"] = [t for t in self._data["todos"] if t.get("status") != "completed"]
            count = before - len(self._data["todos"])
            if count > 0:
                self._save()
            return count

    def get_categories(self) -> list:
        with self._lock:
            return list(self._data.get("categories", []))

    def _ensure_category(self, category: str):
        cats = self._data.get("categories", [])
        if category and category not in cats:
            cats.append(category)
            self._data["categories"] = cats
