import sys
import os
import json
from unittest import TestCase
from datetime import datetime

import redis
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.app.models import JobDetails
from src.adapters.RedisJobService import RedisJobService
from src.adapters.RedisJobStore import RedisJobStore
from src.adapters.RedisJobQueue import RedisJobQueue
from src.adapters.RedisJobState import RedisJobState
from src.app.config import JOBS_LIST_QUEUE_NAME,\
    JOBS_UN_INITED_QUEUE_NAME, STATUS_IN_PROGRESS

class TestRedisJobService(TestCase):
    def test_add_job(self):
        jd = JobDetails(
            job_name='TEST_JOB',
            created_date=datetime.strptime('2026-04-14 00:00:00', '%Y-%m-%d %H:%M:%S'),
            input_data={
                'domain_name': 'ajaydevarakonda.dev',
            },
        )
        red = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            decode_responses=True,
            db=os.getenv('REDIS_DB_NUMBER'),
        )
        rj_store = RedisJobStore(red)
        rj_queue = RedisJobQueue(red)
        rj_state = RedisJobState(red)
        rjs = RedisJobService(red, rj_store, rj_queue, rj_state)

        job_id = rjs.add_job(jd)
        self.assertTrue(red.hgetall(JOBS_LIST_QUEUE_NAME + str(job_id)))
        self.assertTrue(
            red.zscore(JOBS_UN_INITED_QUEUE_NAME, job_id)
        )
        rjs._remove_job(job_id)

    def test_process_job(self):
        jd = JobDetails(
            job_name='TEST_JOB',
            created_date=datetime.strptime(
                '2026-04-14 00:00:00', '%Y-%m-%d %H:%M:%S'
            ),
            input_data={
                'domain_name': 'ajaydevarakonda.dev',
            },
        )
        red = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            decode_responses=True,
            db=os.getenv('REDIS_DB_NUMBER'),
        )
        rj_store = RedisJobStore(red)
        rj_queue = RedisJobQueue(red)
        rj_state = RedisJobState(red)
        rjs = RedisJobService(red, rj_store, rj_queue, rj_state)
        job_id = rjs.add_job(jd)
        rjs.process_job(job_id)
        self.assertTrue(
            red.hget(
                JOBS_LIST_QUEUE_NAME + str(job_id),
                'status',
            ),
            STATUS_IN_PROGRESS,
        )
        self.assertTrue(
            red.zscore(JOBS_UN_INITED_QUEUE_NAME, job_id)
        )

        rjs._remove_job(job_id)
