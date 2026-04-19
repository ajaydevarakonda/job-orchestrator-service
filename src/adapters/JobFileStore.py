import os
import json

class JobFileStore:
    def __init__(self, base_dir):
        self.base_dir = base_dir

    def write_to_file(self, job_id, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        
        file_path = os.path.join(self.base_dir, f'job_{job_id}', 'result.json')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(data)

    def read_from_file(self, job_id):
        file_path = os.path.join(self.base_dir, f'job_{job_id}', 'result.json')
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        return data