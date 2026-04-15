import unittest
from unittest.mock import patch

from app import app
from models import create_todo, validate_update


class TodoTimestampTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("models.datetime")
    def test_create_todo_sets_created_at(self, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = "2026-04-15T10:00:00"
        todo = create_todo({"title": "Write tests"})
        self.assertEqual(todo["created_at"], "2026-04-15T10:00:00")
        self.assertEqual(todo["updated_at"], "2026-04-15T10:00:00")

    @patch("app.create_todo")
    @patch("app.store")
    def test_post_todo_returns_created_at(self, mock_store, mock_create_todo):
        mock_create_todo.return_value = {
            "id": "1",
            "title": "New todo",
            "description": "",
            "status": "pending",
            "priority": "medium",
            "category": "",
            "due_date": None,
            "created_at": "2026-04-15T10:00:00",
            "updated_at": "2026-04-15T10:00:00",
            "completed_at": None,
        }
        mock_store.add_todo.return_value = mock_create_todo.return_value

        response = self.client.post("/api/todos", json={"title": "New todo"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["created_at"], "2026-04-15T10:00:00")

    @patch("models.datetime")
    def test_validate_update_sets_updated_at(self, mock_datetime):
        mock_datetime.utcnow.return_value.isoformat.return_value = "2026-04-15T11:00:00"
        updates = validate_update({"title": "Updated title"})
        self.assertEqual(updates["updated_at"], "2026-04-15T11:00:00")


if __name__ == "__main__":
    unittest.main()
