import unittest

from app import app


class TagsApiTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_create_todo_accepts_tags(self):
        response = self.client.post('/todos', json={'title': 'Fix bug', 'tags': ['Bug', 'urgent', 'bug']})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['tags'], ['bug', 'urgent'])

    def test_get_todos_returns_tags(self):
        response = self.client.get('/todos')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_tags_returns_counts(self):
        self.client.post('/todos', json={'title': 'Meet team', 'tags': ['meeting', 'urgent']})
        self.client.post('/todos', json={'title': 'Fix prod bug', 'tags': ['urgent', 'bug']})
        response = self.client.get('/tags')
        self.assertEqual(response.status_code, 200)
        tags = response.get_json()
        self.assertTrue(any(item['tag'] == 'urgent' for item in tags))
