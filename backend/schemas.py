from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class JobResponse(BaseModel):
    id: int
    google_job_id: Optional[str] = None
    job_pull_date: Optional[datetime] = None
    posted_date_parsed: Optional[str] = None
    employment_type: Optional[str] = None
    job_title: str
    company: str
    source: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    best_apply_link: Optional[str] = None
    apply_link_type: Optional[str] = None
    thumbnail: Optional[str] = None
    cohort_tag: str
    salary_display: Optional[str] = None
    work_mode: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    pages: int
    cohort_label: str


class IngestRequest(BaseModel):
    cohort_name: Optional[str] = None


class IngestResponse(BaseModel):
    inserted: int
    skipped: int
    cohort: str
