import json
import os
from datetime import datetime
import uuid

class SimpleStorage:
    def __init__(self):
        self.data_file = 'analyses.json'
        self.data = self._load_data()
    
    def _load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, default=str, indent=2)
    
    def save_analysis(self, data):
        data['_id'] = str(uuid.uuid4())
        data['created_at'] = datetime.utcnow().isoformat()
        self.data.append(data)
        self._save_data()
        return type('Result', (), {'inserted_id': data['_id']})()
    
    def get_analysis(self, analysis_id):
        for item in self.data:
            if item['_id'] == analysis_id:
                return item
        return None
    
    def get_all_analyses(self):
        return sorted(self.data, key=lambda x: x['created_at'], reverse=True)