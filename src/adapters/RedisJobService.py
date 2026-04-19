import asyncio
from src.app.config import JOB_MAX_RETRIES

class RedisJobService:
    def __init__(
        self, redis_instance, redis_job_store, redis_job_queue,
        redis_job_state,
    ):
        self.redis = redis_instance
        self.redis_job_store = redis_job_store
        self.redis_job_queue = redis_job_queue
        self.redis_job_state = redis_job_state

    def add_job(self, job_details):
        job_id = self.redis_job_store.increment_job_id_counter()
        self.redis_job_store.raise_if_job_already_exists(job_id)
        job_details.job_id = job_id
        self.redis_job_store.add_job(job_details)
        self.redis_job_state.mark_job_un_inited(job_id)
        self.redis_job_queue.enqueue(job_id)
        return job_id

    async def add_job_async(self, job_details):
        return await asyncio.to_thread(self.add_job, job_details)

    def process_job(self):
        job_id = self.redis_job_queue.dequeue()

        if job_id == None:
            return None

        self.redis_job_state.mark_job_in_progress(job_id)
        self.redis_job_queue.move_job_to_in_progress_queue(job_id)
        job_details = self.redis_job_store.get_job(job_id)
        return job_details

    def complete_job(self, std_err, output_data, job_id):
        self.redis_job_store.set_job_stderr(job_id, std_err)
        self.redis_job_store.set_job_output_data(job_id, output_data)
        self.redis_job_state.mark_job_done(job_id)
        self.redis_job_queue.move_job_to_done_queue(job_id)

    def retry_job(self, std_err, job_id):
        retries = self.redis_job_store.get_job_retries(job_id)

        if retries >= JOB_MAX_RETRIES:
            self.fail_job(std_err, job_id)
            return None

        self.redis_job_store.set_job_retries(int(retries) + 1, job_id)
        self.redis_job_store.set_job_stderr(job_id, std_err)
        self.redis_job_state.mark_job_retrying(job_id)
        self.redis_job_queue.move_job_to_un_inited_queue(job_id)

    def fail_job(self, std_err, job_id):
        self.redis_job_store.set_job_stderr(job_id, std_err)
        self.redis_job_state.mark_job_failed(job_id)
        self.redis_job_queue.move_job_to_failed_queue(job_id)

    def _remove_job(self, job_id):
        self.redis_job_store.remove_job(job_id)
        self.redis_job_queue.remove_job_from_all_queues(job_id)
