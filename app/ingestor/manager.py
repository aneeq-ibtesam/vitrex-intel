import threading
import time
from app.extensions import mongo
from .limo import LimoIngestor
from .abusech import AbuseCHIngestor
from .tor import TorIngestor

class IngestionManager:
    def __init__(self):
        self.ingestors = [
            LimoIngestor(), # Simulated
            AbuseCHIngestor(),
            TorIngestor()
        ]
        self.running = False

    def start_background_ingestion(self):
        if not self.running:
            self.running = True
            t = threading.Thread(target=self._run_loop)
            t.daemon = True
            t.start()
            print("Background ingestion started.")

    def _run_loop(self):
        # Run once immediately, then every hour (or manual trigger)
        # For this demo, just run once when called
        self.run_ingestion()
        self.running = False # Reset for demo purposes so it can be triggered again

    def run_sync_ingestion(self):
        """Run ingestion synchronously and return stats."""
        return self.run_ingestion()

    def run_ingestion(self):
        print("Starting ingestion cycle...")
        all_objects = []
        for ingestor in self.ingestors:
            try:
                objects = ingestor.ingest()
                all_objects.extend(objects)
            except Exception as e:
                print(f"Ingestor failed: {e}")
        
        stats = self._save_to_db(all_objects)
        print("Ingestion cycle complete.")
        return stats

    def _save_to_db(self, objects):
        stats = {'new': 0, 'updated': 0}
        
        if not objects:
            return stats
            
        db = mongo.db
        if db is not None:
            col = db.iocs
            for obj in objects:
                # Upsert based on the Indicator Pattern (the actual IOC value)
                res = col.update_one(
                    {'id': obj['id']},
                    {'$set': obj},
                    upsert=True
                )
                
                if res.upserted_id:
                    stats['new'] += 1
                elif res.modified_count > 0:
                    stats['updated'] += 1
                    
            print(f"Saved {len(objects)} objects. New: {stats['new']}, Updated: {stats['updated']}")
        else:
            print("Database not initialized, skipping save.")
            
        return stats

