import subprocess
import threading

class SubProcessJobExecutor:
    def __init__(self):
        pass

    def _execute_job(
            self,
            on_process_created_handler_function,
            on_process_done_handler_function,
            cmd,
        ):
        job = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        on_process_created_handler_function(job.pid)
        stdout, stderr = job.communicate()
        ret_code = job.returncode
        on_process_done_handler_function(ret_code, stdout, stderr)

    def execute_job(
            self,
            on_process_created_handler_function,
            on_process_done_handler_function,
            cmd,
        ):
        threading.Thread(
            target=self._execute_job,
            args=(
                on_process_created_handler_function,
                on_process_done_handler_function,
                cmd,
            ),
        ).start()
