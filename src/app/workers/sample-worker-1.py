import os
import sys
import json
import time
import logging

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from src.adapters.ResultFileStore import ResultFileStore

def main(job_id, input_data):
    time.sleep(10)
    raise ValueError('Throwing our own exception for testing!!!')
    # rfs = ResultFileStore('temp/job_runs')
    # rfs.write_json_result(job_id, input_data)

if __name__ == '__main__':
    cmd_args = sys.argv

    if len(cmd_args) < 3:
        logging.error('[ - ] sample-worker-1: Did not recieve any input data! Expected stringified json input as command line argument!')
        sys.exit(1)

    job_id = json.loads(cmd_args[1])
    input_data = json.loads(cmd_args[2])
    main(job_id, input_data)
