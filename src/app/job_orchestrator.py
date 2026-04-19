'''
Job orchestrator will read inputs from redis and run tools based on the tool name.
'''
import os
import sys
import time
import traceback

import redis
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.adapters.RedisJobStore import RedisJobStore
from src.adapters.RedisJobState import RedisJobState
from src.adapters.RedisJobQueue import RedisJobQueue
from src.adapters.RedisJobService import RedisJobService
from src.adapters.PythonCommandBuilder import PythonCommandBuilder
from src.adapters.SubProcessJobExecutor import SubProcessJobExecutor
from src.adapters.JobExecutor import JobExecutor
from src.adapters.JobRunner import JobRunner
from src.adapters.ResultFileStore import ResultFileStore
from config import JOB_NAMES, JOB_TYPES

# ---------------------------------------------------------------------------

red = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    decode_responses=True,
    db=os.getenv('REDIS_DB_NUMBER'),
)
job_store = RedisJobStore(red)
job_state = RedisJobState(red)
job_queue = RedisJobQueue(red)
job_service = RedisJobService(red, job_store, job_queue, job_state)
cmd_builder = PythonCommandBuilder()
sub_job_exec = SubProcessJobExecutor()
job_executor = JobExecutor(sub_job_exec, cmd_builder)
file_store = ResultFileStore('temp/job_runs')
job_runner = JobRunner(job_service, job_executor, file_store)

# ---------------------------------------------------------------------------

job_runner.run_job()
