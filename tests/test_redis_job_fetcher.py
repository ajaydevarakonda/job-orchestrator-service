import sys
import os
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.adapters.RedisJobFetcher import RedisJobFetcher
from src.adapters.Redis import Redis

class TestRedisJobFetcher(TestCase):
    def test_redis_job_fetcher(self):
        jc = RedisJobFetcher()
        red = Redis(host='localhost', port=6379, db=0)
        red._redis.hset('job_orchestrator_service::job_queue')
        jc.fetch_new_jobs()
