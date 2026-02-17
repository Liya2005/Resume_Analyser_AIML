from pymongo import MongoClient
from datetime import datetime
import os

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
        self.db = self.client.resume_analyzer
        
    def save_analysis(self, data):
        data['created_at'] = datetime.utcnow()
        return self.db.analyses.insert_one(data)
    
    def get_analysis(self, analysis_id):
        return self.db.analyses.find_one({'_id': analysis_id})
    
    def get_all_analyses(self):
        return list(self.db.analyses.find().sort('created_at', -1))