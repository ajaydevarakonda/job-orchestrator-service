import os
import json
import tempfile


class ResultFileStore:
    def __init__(self, base_dir='tmp/job_runs'):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _get_job_dir(self, job_id):
        path = os.path.join(self.base_dir, str(job_id))
        os.makedirs(path, exist_ok=True)
        return path

    def _get_file_path(self, job_id, filename='result.json'):
        return os.path.join(self._get_job_dir(job_id), filename)

    def write_json_result(self, job_id, data):
        '''
            We are first going to write to a temp file and then just\
            rename that file to result.json, to prevent any moment\
            where the file is half written, to prevent data corruption\
            issues on the reader's end, due to half reads while the\
            writer is writing.
        '''
        final_path = self._get_file_path(job_id)
        fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(final_path))

        try:
            with os.fdopen(fd, 'w') as temp_file:
                json.dump(data, temp_file)
                temp_file.flush()
                # Ensure it's written to disk.
                os.fsync(temp_file.fileno())

            os.replace(temp_path, final_path)
        except:
            print('[ - ] ResultFileStore::write_json_result: Couldn\'t write data to result file!')
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def read_json_result(self, job_id):
        path = self._get_file_path(job_id)

        if not os.path.exists(path):
            raise FileNotFoundError(f'{path} does not exist')

        with open(path, 'r') as f:
            return json.load(f)
