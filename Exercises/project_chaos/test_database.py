"""Tests for database module."""
import unittest
from database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database("test")
    
    def test_connection(self):
        """Test database connection."""
        self.assertIsNotNone(self.db.connection)
        self.assertIn("test", self.db.connection.lower())
    
    def test_query(self):
        """Test query execution."""
        result = self.db.query("SELECT * FROM users")
        self.assertEqual(len(result), 3)
        self.assertIn("name", result[0])
    
    def tearDown(self):
        self.db.close()

if __name__ == "__main__":
    unittest.main()
