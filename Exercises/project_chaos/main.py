"""Main application entry point."""
from database import Database
from analytics import Analytics
from utils import format_timestamp

def main():
    db = Database("production")
    analytics = Analytics()
    
    print("Application Starting...")
    print(f"Started at: {format_timestamp()}")
    
    # Load data
    data = db.query("SELECT * FROM users")
    print(f"Loaded {len(data)} records")
    
    # Process analytics
    results = analytics.process(data)
    analytics.report(results)
    
    print("Application Complete")

if __name__ == "__main__":
    main()
