import sys
import os
from unittest import TestCase

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from adapters.PythonCommandBuilder import PythonJobCreator

def my_handler(ret_code, stdout, stderr):
    print(ret_code, stdout, stderr)
    print('This is the on complete handler!')

class TestPythonJobCreator(TestCase):
    def test_job_creation(self):
        jc = PythonJobCreator()
        job = jc.run_job(
            my_handler,
            '/home/rj/Desktop/programming/job-orchestrator-service/src/app/workers/sample-worker-1.py',
            '{\"hello\": \"world!\"}'
        )
        print('Job already instantiated, moving on to do other stuff!')
