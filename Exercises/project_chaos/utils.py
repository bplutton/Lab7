"""Utility functions used across the application."""
from datetime import datetime

def format_timestamp():
    """Return current timestamp as formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validate_input(data):
    """Validate input data structure."""
    required_fields = ["id", "name", "score"]
    return all(field in data for field in required_fields)

def calculate_grade(score):
    """Convert numeric score to letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
