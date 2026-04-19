from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

@dataclass
class NewJobDetails:
    job_name: str
    created_date: datetime
    input_data: dict
    job_id: int=None

@dataclass
class JobDetails:
    job_id: int
    job_name: str
    created_date: datetime
    input_data: str

class JobDetailsBaseModel(BaseModel):
    job_name: str
    input_data: dict
