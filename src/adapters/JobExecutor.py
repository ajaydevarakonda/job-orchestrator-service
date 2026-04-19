class JobExecutor:
    def __init__(self, process_executor, command_builder):
        self.process_executor = process_executor
        self.command_builder = command_builder

    def run(
            self,
            on_process_created_handler_function,
            on_process_done_handler_function,
            worker_full_path,
            job_id,
            input_data,
        ):
        cmd = self.command_builder.build_command(
            worker_full_path, job_id, input_data,
        )
        self.process_executor.execute_job(
            on_process_created_handler_function,
            on_process_done_handler_function,
            cmd,
        )
