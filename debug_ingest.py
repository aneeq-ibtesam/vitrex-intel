import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from app import create_app
from app.ingestor.manager import IngestionManager

app = create_app('default')

# We need to run this within app context so mongo extension works
with app.app_context():
    print("Initializing Ingestion Manager...")
    manager = IngestionManager()
    
    print("Starting manual ingestion run...")
    try:
        manager.run_ingestion()
        print("Ingestion run finished.")
        
        # Check DB count
        from app.extensions import mongo
        count = mongo.db.iocs.count_documents({})
        print(f"Total IOCs in DB: {count}")
        
    except Exception as e:
        print(f"Ingestion failed with error: {e}")
        import traceback
        traceback.print_exc()
