from src.shared.utils import redis_zmove
from src.app.config import JOBS_LIST_QUEUE_NAME, JOBS_UN_INITED_QUEUE_NAME, JOBS_IN_PROGRESS_QUEUE_NAME,\
    JOBS_DONE_QUEUE_NAME, JOBS_FAILED_QUEUE_NAME, STATUS_UN_INITED, STATUS_IN_PROGRESS, STATUS_DONE,\
    STATUS_FAILED

class RedisJobState:
    def __init__(self, redis_instance):
        self.redis_instance = redis_instance

    def _update_job_status(self, src_queue, dest_queue, new_status, job_id):
        if not self.redis_instance.exists(JOBS_LIST_QUEUE_NAME + str(job_id)):
            raise ValueError(f'[ - ] RedisJobService::_update_job_status: job {job_id} is not present in jobs list!')

        if self.redis_instance.zrank(src_queue, job_id):
            raise ValueError(f'[ - ] RedisJobService::_update_job_status: job {job_id} is not present in the `{src_queue}` job queue!')

        self.redis_instance.hset(JOBS_LIST_QUEUE_NAME + str(job_id), 'status', new_status)
        redis_zmove(self.redis_instance, src_queue, dest_queue, job_id)

    def mark_job_un_inited(self, job_id):
        if not self.redis_instance.exists(JOBS_LIST_QUEUE_NAME + str(job_id)):
            raise ValueError(f'[ - ] RedisJobService::_update_job_status: job {job_id} is not present in jobs list!')

        self.redis_instance.hset(JOBS_LIST_QUEUE_NAME + str(job_id), 'status', STATUS_UN_INITED)

    def mark_job_in_progress(self, job_id):
        self._update_job_status(
            JOBS_UN_INITED_QUEUE_NAME, JOBS_IN_PROGRESS_QUEUE_NAME,\
            STATUS_IN_PROGRESS, job_id,
        )

    def mark_job_done(self, job_id):
        self._update_job_status(
            JOBS_IN_PROGRESS_QUEUE_NAME, JOBS_DONE_QUEUE_NAME, STATUS_DONE,
            job_id,
        )

    def mark_job_retrying(self, job_id):
        self.redis_instance.hset(JOBS_LIST_QUEUE_NAME + str(job_id), 'status', STATUS_UN_INITED)
        redis_zmove(self.redis_instance, JOBS_IN_PROGRESS_QUEUE_NAME, JOBS_UN_INITED_QUEUE_NAME, job_id)

    def mark_job_failed(self, job_id):
        self._update_job_status(
            JOBS_IN_PROGRESS_QUEUE_NAME, JOBS_FAILED_QUEUE_NAME, STATUS_FAILED,
            job_id,
        )
