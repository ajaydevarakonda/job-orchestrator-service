class PythonCommandBuilder:
    def __init__(self):
        pass

    def build_command(
        self,
        python_file_full_path,
        job_id,
        input_data,
    ):
        job_cmd = ['python', python_file_full_path, job_id, input_data]
        return job_cmd
