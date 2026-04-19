import json
from datetime import datetime

from src.app.models import JobDetails
from src.app.config import\
    JOBS_LIST_QUEUE_NAME, JOBS_UN_INITED_QUEUE_NAME, JOBS_IN_PROGRESS_QUEUE_NAME,\
    JOBS_DONE_QUEUE_NAME, JOBS_FAILED_QUEUE_NAME, STATUS_UN_INITED, JOB_ID_COUNTER_NAME,\
    LARGE_FOR_LOOP_TOP_END_LIMIT

class RedisJobStore:
    def __init__(self, redis_instance):
        self.redis_instance = redis_instance

    def extract_job_ids_list_from_redis_keys(self, redis_keys):
        job_ids = []

        for key in redis_keys:
            job_id = key.split('::')[-1]

            if not job_id.isdigit():
                continue

            job_id = int(job_id)
            job_ids.append(job_id)

        return job_ids

    def recover_job_id_from_existing_data(self):
        cursor = 0

        for i in range(LARGE_FOR_LOOP_TOP_END_LIMIT):
            cursor, keys = self.redis_instance.scan(cursor=cursor, match=JOBS_LIST_QUEUE_NAME+'*')

            if keys:
                job_ids = self.extract_job_ids_list_from_redis_keys(keys)
                return max(job_ids)

            if cursor == 0:
                return 0

        return 0

    def increment_job_id_counter(self):
        if self.redis_instance.exists(JOB_ID_COUNTER_NAME):
            new_job_id_value = self.redis_instance.incr(JOB_ID_COUNTER_NAME)
            return int(new_job_id_value)

        new_job_id_value = self.recover_job_id_from_existing_data() + 1
        self.redis_instance.set(JOB_ID_COUNTER_NAME, new_job_id_value)
        return int(new_job_id_value)

    def raise_if_job_already_exists(self, job_id):
        if self.redis_instance.exists(JOBS_LIST_QUEUE_NAME + str(job_id)):
            raise ValueError(f'[ - ] RedisJobService::check_if_job_already_exists: A job with job_id {job_id} is already present in the jobs list!')

        if self.redis_instance.zrank(JOBS_UN_INITED_QUEUE_NAME, job_id):
            raise ValueError(f'[ - ] RedisJobService::check_if_job_already_exists: A job with job_id {job_id} is already present in the `un-inited` job queue!')

        if self.redis_instance.zrank(JOBS_IN_PROGRESS_QUEUE_NAME, job_id):
            raise ValueError(f'[ - ] RedisJobService::check_if_job_already_exists: A job with job_id {job_id} is already present in the `in-progress` job queue!')

        if self.redis_instance.zrank(JOBS_DONE_QUEUE_NAME, job_id):
            raise ValueError(f'[ - ] RedisJobService::check_if_job_already_exists: A job with job_id {job_id} is already present in the `done` job queue!')

        return False

    def add_job(self, job_details):
        self.redis_instance.hset(
            JOBS_LIST_QUEUE_NAME + str(job_details.job_id),
            mapping={
                'job_name': job_details.job_name,
                'created_date': datetime.strftime(job_details.created_date, '%Y-%m-%d %H:%M:%S'),
                'input_data': json.dumps(job_details.input_data),
                'output_data': '',
                'retries': 0,
                'status': STATUS_UN_INITED,
                'stderr': '',
            }
        )

    def get_job(self, job_id):
        job = self.redis_instance.hgetall(
            JOBS_LIST_QUEUE_NAME + str(job_id),
        )

        if not job:
            raise ValueError(f'[ - ] RedisJobStore::get_job: A job with job_id {job_id} doesn\'t exist in the jobs list!')

        new_job = JobDetails(
            job_id=job_id,
            job_name=job['job_name'],
            input_data=job['input_data'],
            created_date=job['created_date'],
        )
        return new_job

    def remove_job(self, job_id):
        self.redis_instance.delete(JOBS_LIST_QUEUE_NAME + str(job_id))

    def set_job_output_data(self, job_id, data):
        self.redis_instance.hset(
            JOBS_LIST_QUEUE_NAME + str(job_id),
            'output_data',
            json.dumps(data),
        )

    def set_job_stderr(self, job_id, stderr):
        self.redis_instance.hset(
            JOBS_LIST_QUEUE_NAME + str(job_id),
            'stderr',
            stderr,
        )

    def get_job_retries(self, job_id):
        return int(
            self.redis_instance.hget(
                JOBS_LIST_QUEUE_NAME + str(job_id),
                'retries',
            )
        )

    def set_job_retries(self, retries_count, job_id):
        self.redis_instance.hset(
            JOBS_LIST_QUEUE_NAME + str(job_id),
            'retries',
            retries_count,
        )
