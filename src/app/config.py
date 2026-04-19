JOB_ID_COUNTER_NAME='job_orchestrator_service::job_id_counter'
JOBS_LIST_QUEUE_NAME='job_orchestrator_service::jobs_list::'
JOBS_UN_INITED_QUEUE_NAME='job_orchestrator_service::job_queue::un_inited'
JOBS_IN_PROGRESS_QUEUE_NAME='job_orchestrator_service::job_queue::in_progress'
JOBS_DONE_QUEUE_NAME='job_orchestrator_service::job_queue::done'
JOBS_FAILED_QUEUE_NAME='job_orchestrator_service::job_queue::failed'

STATUS_UN_INITED='UN_INITED'
STATUS_IN_PROGRESS='IN_PROGRESS'
STATUS_DONE='DONE'
STATUS_FAILED='FAILED'

LARGE_FOR_LOOP_TOP_END_LIMIT=10000

JOB_TYPES = {
    'SAMPLE_JOB': {
        'WORKER_PATH': '/home/rj/Desktop/programming/job-orchestrator-service/src/app/workers/sample-worker-1.py'
    }
}
JOB_NAMES = list(JOB_TYPES.keys())
JOB_MAX_RETRIES = 4
JOB_FETCHER_SLEEP_TIME_SECS = 5