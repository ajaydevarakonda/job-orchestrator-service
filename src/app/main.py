import os
import traceback
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import redis
from dotenv import load_dotenv
load_dotenv()

from src.app.models import NewJobDetails, JobDetailsBaseModel
from src.adapters.RedisJobStore import RedisJobStore
from src.adapters.RedisJobQueue import RedisJobQueue
from src.adapters.RedisJobState import RedisJobState
from src.adapters.RedisJobService import RedisJobService

# ------------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

origins = ['*']
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
red = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    decode_responses=True,
    db=os.getenv('REDIS_DB_NUMBER'),
)
red_job_store = RedisJobStore(red)
red_job_queue = RedisJobQueue(red)
red_job_state = RedisJobState(red)
rjs = RedisJobService(red, red_job_store, red_job_queue, red_job_state)

# ------------------------------------------------------------------------------

@app.get('/')
def root():
    return Response(status_code=204)

@app.post('/add-job')
async def check_token_validity(jd: JobDetailsBaseModel):
    try:
        jd = NewJobDetails(
            job_name=jd.job_name,
            created_date=datetime.now(),
            input_data=jd.input_data
        )
        await rjs.add_job_async(jd)
        return Response(status_code=201)
    except Exception as e:
        print(traceback.format_exc())
        return HTTPException(
            status_code=400,
            message='Could not create a new job!'
        )
