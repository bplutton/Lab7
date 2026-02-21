"""Analytics and reporting functionality."""
from utils import format_timestamp

class Analytics:
    def __init__(self):
        self.results = []
    
    def process(self, data):
        """Process data for analytics."""
        print("Processing analytics...")
        total = sum(item["score"] for item in data)
        average = total / len(data) if data else 0
        
        return {
            "total_records": len(data),
            "average_score": round(average, 2),
            "max_score": max(item["score"] for item in data) if data else 0,
            "min_score": min(item["score"] for item in data) if data else 0,
            "timestamp": format_timestamp(),
        }
    
    def report(self, results):
        """Generate report from results."""
        print("\n=== Analytics Report ===")
        print(f"Total Records: {results['total_records']}")
        print(f"Average Score: {results['average_score']}")
        print(f"Max Score: {results['max_score']}")
        print(f"Min Score: {results['min_score']}")
        print(f"Generated: {results['timestamp']}")
        print("========================\n")
