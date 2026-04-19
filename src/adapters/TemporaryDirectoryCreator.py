import os

class TemporaryDirectoryCreator:
    def __init__(self, parent_directory_full_path):
        self.parent_dir_path = parent_directory_full_path

    def create_temp_directory(self, job_id):
        os.path.join(self.parent_dir_path, str(job_id))
