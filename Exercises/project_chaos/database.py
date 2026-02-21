"""Database connection and query handling."""

class Database:
    def __init__(self, environment):
        self.environment = environment
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish database connection."""
        print(f"Connecting to {self.environment} database...")
        self.connection = f"DB_{self.environment.upper()}"
    
    def query(self, sql):
        """Execute a database query."""
        print(f"Executing query: {sql[:50]}...")
        # Mock data for exercise
        return [
            {"id": 1, "name": "Alice", "score": 95},
            {"id": 2, "name": "Bob", "score": 87},
            {"id": 3, "name": "Charlie", "score": 92},
        ]
    
    def close(self):
        """Close database connection."""
        print("Database connection closed")
