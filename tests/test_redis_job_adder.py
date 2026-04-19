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
from src.app.config import JOB_ID_COUNTER_NAME, JOBS_LIST_QUEUE_NAME

class TestRedisJobService(TestCase):
    # def test_redis_job_add(self):
    #     job_id = 1234
    #     jd = JobDetails(
    #         job_id=job_id,
    #         job_name='TEST_JOB',
    #         created_date=datetime.strptime('2026-04-14 00:00:00', '%Y-%m-%d %H:%M:%S'),
    #         input_data={
    #             'domain_name': 'ajaydevarakonda.dev',
    #         },
    #     )
    #     red = redis.Redis(
    #         host=os.getenv('REDIS_HOST'),
    #         port=os.getenv('REDIS_PORT'),
    #         decode_responses=True,
    #         db=os.getenv('REDIS_DB_NUMBER'),
    #     )
    #     rjs = RedisJobService(red)
    #     # If job already exists, remove that job first.
    #     rjs.remove_job(job_id)
    #     rjs.add_job(jd)
    #     self.assertTrue(red.hgetall(f'job_orchestrator_service::jobs_list::{job_id}'))
    #     self.assertTrue(
    #         red.zscore(
    #             'job_orchestrator_service::job_queue::un_inited',
    #             job_id
    #         )
    #     )
    #     rjs.remove_job(job_id)

    # def test_redis_job_get(self):
    #     job_id = 1234
    #     jd = JobDetails(
    #         job_id=job_id,
    #         job_name='TEST_JOB',
    #         created_date=datetime.strptime('2026-04-14 00:00:00', '%Y-%m-%d %H:%M:%S'),
    #         input_data={
    #             'domain_name': 'ajaydevarakonda.dev',
    #         },
    #     )
    #     red = redis.Redis(
    #         host=os.getenv('REDIS_HOST'),
    #         port=os.getenv('REDIS_PORT'),
    #         decode_responses=True,
    #         db=os.getenv('REDIS_DB_NUMBER'),
    #     )
    #     rjs = RedisJobService(red)
    #     rjs.add_job(jd)
    #     rjs.get_a_new_job()
    #     self.assertTrue(red.hgetall(f'job_orchestrator_service::jobs_list::{job_id}'))
    #     self.assertTrue(
    #         red.zscore(
    #             'job_orchestrator_service::job_queue::un_inited',
    #             job_id
    #         )
    #     )
    #     rjs.remove_job(job_id)

    # def test_redis_job_id_increment_counter_value_present(self):
    #     red = redis.Redis(
    #         host=os.getenv('REDIS_HOST'),
    #         port=os.getenv('REDIS_PORT'),
    #         decode_responses=True,
    #         db=os.getenv('REDIS_DB_NUMBER'),
    #     )
    #     rjs = RedisJobService(red)
    #     # Making sure counter value exists.
    #     red.set(JOB_ID_COUNTER_NAME, 23)
    #     rjs.increment_job_id_counter()
    #     self.assertEqual(red.get(JOB_ID_COUNTER_NAME), '24')

    # def test_redis_job_id_increment_counter_value_not_present(self):
    #     red = redis.Redis(
    #         host=os.getenv('REDIS_HOST'),
    #         port=os.getenv('REDIS_PORT'),
    #         decode_responses=True,
    #         db=os.getenv('REDIS_DB_NUMBER'),
    #     )
    #     rjs = RedisJobService(red)
    #     # Making sure counter value does not exist.
    #     red.delete(JOB_ID_COUNTER_NAME)
    #     red.hset(JOBS_LIST_QUEUE_NAME + '23', mapping={
    #         'a': 'b'
    #     })
    #     rjs.increment_job_id_counter()
    #     self.assertEqual(red.get(JOB_ID_COUNTER_NAME), '24')
    #     red.delete(JOBS_LIST_QUEUE_NAME + '23')
    #     red.delete(JOB_ID_COUNTER_NAME)

    # def test_redis_job_mark_in_progress(self):
    #     job_id = 1234
    #     jd = JobDetails(
    #         job_id=job_id,
    #         job_name='TEST_JOB',
    #         created_date=datetime.strptime('2026-04-14 00:00:00', '%Y-%m-%d %H:%M:%S'),
    #         input_data={
    #             'domain_name': 'ajaydevarakonda.dev',
    #         },
    #     )
    #     red = redis.Redis(
    #         host=os.getenv('REDIS_HOST'),
    #         port=os.getenv('REDIS_PORT'),
    #         decode_responses=True,
    #         db=os.getenv('REDIS_DB_NUMBER'),
    #     )
    #     rjs = RedisJobService(red)
    #     rjs.remove_job(job_id)
    #     rjs.add_job(jd)
    #     rjs.mark_job_in_progress(job_id)
    #     self.assertEqual(red.hget(f'job_orchestrator_service::jobs_list::{job_id}', 'status'), 'IN_PROGRESS')
    #     rjs.remove_job(job_id)

    # def test_redis_job_mark_done(self):
    #     job_id = 1234
    #     jd = JobDetails(
    #         job_id=job_id,
    #         job_name='TEST_JOB',
    #         created_date=datetime.strptime('2026-04-14 00:00:00', '%Y-%m-%d %H:%M:%S'),
    #         input_data={
    #             'domain_name': 'ajaydevarakonda.dev',
    #         },
    #     )
    #     red = redis.Redis(
    #         host=os.getenv('REDIS_HOST'),
    #         port=os.getenv('REDIS_PORT'),
    #         decode_responses=True,
    #         db=os.getenv('REDIS_DB_NUMBER'),
    #     )
    #     rjs = RedisJobService(red)
    #     rjs.add_job(jd)
    #     rjs.mark_job_done(job_id)
    #     self.assertEqual(red.hget(f'job_orchestrator_service::jobs_list::{job_id}', 'status'), 'DONE')
    #     rjs.remove_job(job_id)

    # def test_redis_job_mark_retrying(self):
    #     job_id = 1234
    #     jd = JobDetails(
    #         job_id=job_id,
    #         job_name='TEST_JOB',
    #         created_date=datetime.strptime('2026-04-14 00:00:00', '%Y-%m-%d %H:%M:%S'),
    #         input_data={
    #             'domain_name': 'ajaydevarakonda.dev',
    #         },
    #     )
    #     red = redis.Redis(
    #         host=os.getenv('REDIS_HOST'),
    #         port=os.getenv('REDIS_PORT'),
    #         decode_responses=True,
    #         db=os.getenv('REDIS_DB_NUMBER'),
    #     )
    #     rjs = RedisJobService(red)
    #     rjs.add_job(jd)
    #     rjs.mark_job_retrying(job_id)
    #     self.assertEqual(red.hget(f'job_orchestrator_service::jobs_list::{job_id}', 'status'), 'UN_INITED')
    #     self.assertEqual(red.hget(f'job_orchestrator_service::jobs_list::{job_id}', 'retries'), '1')
    #     rjs.remove_job(job_id)

    # def test_redis_job_mark_failed(self):
    #     job_id = 1234
    #     jd = JobDetails(
    #         job_id=job_id,
    #         job_name='TEST_JOB',
    #         created_date=datetime.strptime('2026-04-14 00:00:00', '%Y-%m-%d %H:%M:%S'),
    #         input_data={
    #             'domain_name': 'ajaydevarakonda.dev',
    #         },
    #     )
    #     red = redis.Redis(
    #         host=os.getenv('REDIS_HOST'),
    #         port=os.getenv('REDIS_PORT'),
    #         decode_responses=True,
    #         db=os.getenv('REDIS_DB_NUMBER'),
    #     )
    #     rjs = RedisJobService(red)
    #     rjs.add_job(jd)
    #     rjs.mark_job_failed(job_id)
    #     self.assertEqual(red.hget(f'job_orchestrator_service::jobs_list::{job_id}', 'status'), 'FAILED')
    #     rjs.remove_job(job_id)

    def test_redis_get_latest_job_mark_failed(self):
        red = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            decode_responses=True,
            db=os.getenv('REDIS_DB_NUMBER'),
        )

        # Job 1
        jd1 = JobDetails(
            job_id=1000,
            job_name='TEST_JOB',
            created_date=datetime.strptime('2026-04-15 00:23:00', '%Y-%m-%d %H:%M:%S'),
            input_data={
                'domain_name': 'ajaydevarakonda.dev',
            },
        )
        
        jd2 = JobDetails(
            job_id=1001,
            job_name='TEST_JOB_1',
            created_date=datetime.strptime('2026-04-15 00:24:00', '%Y-%m-%d %H:%M:%S'),
            input_data={
                'domain_name': 'google.com',
            },
        )

        jd3 = JobDetails(
            job_id=1002,
            job_name='TEST_JOB_2',
            created_date=datetime.strptime('2026-04-15 00:22:00', '%Y-%m-%d %H:%M:%S'),
            input_data={
                'domain_name': 'gmail.com',
            },
        )

        rjs = RedisJobService(red)

        rjs.remove_job(1000)
        rjs.remove_job(1001)
        rjs.remove_job(1002)

        rjs.add_job(jd1)
        rjs.add_job(jd2)
        rjs.add_job(jd3)
        new_job = rjs.get_a_new_job()
        self.assertEqual(new_job['job_id'], '1002')

        rjs.remove_job(1000)
        rjs.remove_job(1001)
        rjs.remove_job(1002)
