import unittest
from app import app

class TodoTagsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_tags(self):
        response = self.app.post('/todos/64afd7a1-ef1e-4758-b892-9d6feb2990c3/tags', json={'tags': ['urgent', 'meeting']})
        self.assertEqual(response.status_code, 200)

    def test_get_tags(self):
        response = self.app.get('/todos/tags')
        self.assertEqual(response.status_code, 200)

    def test_filter_todos_by_tag(self):
        response = self.app.get('/todos?tag=urgent')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()