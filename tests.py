import unittest
from unittest.mock import patch

from app import app
from models import create_todo


class TodoCreatedAtTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_create_todo_sets_created_at(self):
        with patch("models.datetime") as mock_datetime:
            mock_datetime.utcnow.return_value.isoformat.return_value = "2026-04-15T10:00:00"
            todo = create_todo({"title": "Write tests"})

        self.assertIn("created_at", todo)
        self.assertEqual(todo["created_at"], "2026-04-15T10:00:00")
        self.assertEqual(todo["updated_at"], "2026-04-15T10:00:00")

    def test_create_todo_api_returns_created_at(self):
        with patch("app.create_todo") as mock_create_todo, patch("app.store") as mock_store:
            mock_create_todo.return_value = {
                "id": "1",
                "title": "Sample",
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

            response = self.client.post("/api/todos", json={"title": "Sample"})

        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload["created_at"], "2026-04-15T10:00:00")


if __name__ == "__main__":
    unittest.main()
