import unittest
from app import create_app, db

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def test_get_messages_unauthorized(self):
        rv = self.client.get('/msg')
        self.assertEqual(rv.status_code, 401)

if __name__ == '__main__':
    unittest.main()
