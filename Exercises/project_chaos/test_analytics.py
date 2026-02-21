"""Tests for analytics module."""
import unittest
from analytics import Analytics
from utils import calculate_grade

class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.analytics = Analytics()
        self.sample_data = [
            {"id": 1, "name": "Alice", "score": 95},
            {"id": 2, "name": "Bob", "score": 85},
            {"id": 3, "name": "Charlie", "score": 92},
        ]
    
    def test_process(self):
        """Test analytics processing."""
        result = self.analytics.process(self.sample_data)
        self.assertEqual(result["total_records"], 3)
        self.assertEqual(result["average_score"], 90.67)
        self.assertEqual(result["max_score"], 95)
    
    def test_empty_data(self):
        """Test with empty data."""
        result = self.analytics.process([])
        self.assertEqual(result["total_records"], 0)
        self.assertEqual(result["average_score"], 0)

class TestGradeCalculation(unittest.TestCase):
    def test_calculate_grade(self):
        """Test grade calculation."""
        self.assertEqual(calculate_grade(95), "A")
        self.assertEqual(calculate_grade(85), "B")
        self.assertEqual(calculate_grade(75), "C")
        self.assertEqual(calculate_grade(65), "D")
        self.assertEqual(calculate_grade(55), "F")

if __name__ == "__main__":
    unittest.main()
