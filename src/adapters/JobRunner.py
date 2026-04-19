import time
import traceback
from datetime import datetime

from src.app.config import JOB_NAMES, JOB_TYPES, JOB_FETCHER_SLEEP_TIME_SECS

class JobRunner:
    def __init__(self, job_service, job_executor, file_store):
        self.job_service = job_service
        self.job_executor = job_executor
        self.file_store = file_store

    def get_job_done_handler(self, rjs, job_id):
        def job_done_handler(ret_code, std_out, std_err):
            if ret_code == 0:
                json_result = self.file_store.read_json_result(job_id)
                rjs.complete_job(std_err, json_result, job_id)
            else:
                rjs.retry_job(std_err, job_id)

        return job_done_handler

    def run_job(self):
        while True:
            try:
                time.sleep(JOB_FETCHER_SLEEP_TIME_SECS)
                job_details = self.job_service.process_job()

                if job_details == None:
                    print(f'[ + ] {datetime.now()}: No jobs in the queue, continuing to poll...')
                    continue

                if job_details.job_name not in JOB_NAMES:
                    continue

                job_id = job_details.job_id
                print(f'[ + ] JobRunner::run_job: Found job {job_id}! Running job!')
                job_done_handler = self.get_job_done_handler(self.job_service, job_id)
                self.job_executor.run(
                    lambda pid: print('Worker started with process id:', pid),
                    job_done_handler,
                    JOB_TYPES[job_details.job_name]['WORKER_PATH'],
                    job_id,
                    job_details.input_data,
                )
            except KeyboardInterrupt:
                break
            except:
                print('[ - ] JobRunner::run_job: Something went wrong!' + traceback.format_exc())
