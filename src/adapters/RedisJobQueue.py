from datetime import datetime

from src.app.config import JOBS_UN_INITED_QUEUE_NAME,\
    JOBS_IN_PROGRESS_QUEUE_NAME, JOBS_DONE_QUEUE_NAME,\
    JOBS_FAILED_QUEUE_NAME
from src.shared.utils import redis_zmove

class RedisJobQueue:
    def __init__(self, redis_instance):
        self.redis_instance = redis_instance

    def dequeue(self):
        job_id = self.redis_instance.zrange(JOBS_UN_INITED_QUEUE_NAME, 0, 0)

        if len(job_id):
            return job_id[0]

        return None

    def enqueue(self, job_id):
        return self.redis_instance.zadd(
            JOBS_UN_INITED_QUEUE_NAME,
            {
                str(job_id): int(datetime.now().timestamp()),
            },
        )

    def move_job_to_un_inited_queue(self, job_id):
        '''We are doing this when retrying a job, so moving from un-inited->in progress.'''
        redis_zmove(
            self.redis_instance,
            JOBS_IN_PROGRESS_QUEUE_NAME,
            JOBS_UN_INITED_QUEUE_NAME,
            job_id
        )

    def move_job_to_in_progress_queue(self, job_id):
        redis_zmove(
            self.redis_instance,
            JOBS_UN_INITED_QUEUE_NAME,
            JOBS_IN_PROGRESS_QUEUE_NAME,
            job_id
        )

    def move_job_to_done_queue(self, job_id):
        redis_zmove(
            self.redis_instance,
            JOBS_IN_PROGRESS_QUEUE_NAME,
            JOBS_DONE_QUEUE_NAME,
            job_id
        )

    def move_job_to_failed_queue(self, job_id):
        redis_zmove(
            self.redis_instance,
            JOBS_IN_PROGRESS_QUEUE_NAME,
            JOBS_FAILED_QUEUE_NAME,
            job_id
        )

    def remove_job_from_all_queues(self, job_id):
        self.redis_instance.zrem(JOBS_IN_PROGRESS_QUEUE_NAME, job_id)
        self.redis_instance.zrem(JOBS_DONE_QUEUE_NAME, job_id)
        self.redis_instance.zrem(JOBS_FAILED_QUEUE_NAME, job_id)
