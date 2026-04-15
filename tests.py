import os
import tempfile
import unittest
from unittest.mock import patch

from app import app
from storage import StorageManager


class TodoTimestampTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.data_file = os.path.join(self.tmpdir.name, "todos.json")
        self.store = StorageManager(filepath=self.data_file)
        self.client = app.test_client()
        app.config["TESTING"] = True

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_create_todo_sets_created_at_automatically(self):
        with patch("app.store", self.store):
            response = self.client.post(
                "/api/todos",
                json={"title": "Write tests", "description": "Check timestamp"},
            )

        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertIn("created_at", payload)
        self.assertIsInstance(payload["created_at"], str)
        self.assertEqual(payload["status"], "pending")

    def test_created_at_is_returned_in_todo_detail(self):
        with patch("app.store", self.store):
            create_response = self.client.post("/api/todos", json={"title": "Read detail"})
            todo_id = create_response.get_json()["id"]
            detail_response = self.client.get(f"/api/todos/{todo_id}")

        self.assertEqual(detail_response.status_code, 200)
        payload = detail_response.get_json()
        self.assertIn("created_at", payload)
        self.assertEqual(payload["id"], todo_id)

    def test_created_at_is_present_in_list_response(self):
        with patch("app.store", self.store):
            self.client.post("/api/todos", json={"title": "List item"})
            response = self.client.get("/api/todos")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(len(payload), 1)
        self.assertIn("created_at", payload[0])


if __name__ == "__main__":
    unittest.main()
