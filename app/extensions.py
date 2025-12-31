from pymongo import MongoClient

class MongoExtension:
    def __init__(self):
        self.db = None
        self.client = None

    def init_app(self, app):
        self.client = MongoClient(app.config['MONGO_URI'])
        self.db = self.client.get_default_database()

mongo = MongoExtension()
