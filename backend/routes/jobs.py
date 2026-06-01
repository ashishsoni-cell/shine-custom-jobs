
import json
import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models import Job
from backend.schemas import JobResponse, JobListResponse

router = APIRouter(prefix="/api", tags=["jobs"])
COHORTS_PATH = os.path.join(os.path.dirname(__file__), "../../data/cohorts.json")

def _load_cohorts():
    with open(COHORTS_PATH) as f:
        return json.load(f)

@router.get("/jobs", response_model=JobListResponse)
def list_jobs(
    cohort: str = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    location: Optional[str] = None,
    employment_type: Optional[str] = None,
    work_mode: Optional[str] = None,
    company: Optional[str] = None,
    sort: str = "recent",
    db: Session = Depends(get_db),
):
    cohorts = _load_cohorts()
    cohort_info = next((c for c in cohorts if c["name"] == cohort), None)
    cohort_label = cohort_info["label"] if cohort_info else cohort.replace("-", " ").title()
    q = db.query(Job).filter(Job.cohort_tag == cohort, Job.is_active == True)
    if location:
        q = q.filter(Job.location.ilike(f"%{location}%"))
    if employment_type:
        q = q.filter(Job.employment_type == employment_type)
    if work_mode:
        q = q.filter(Job.work_mode == work_mode)
    if company:
        q = q.filter(Job.company.ilike(f"%{company}%"))
    total = q.count()
    if sort == "company":
        q = q.order_by(Job.company.asc())
    else:
        q = q.order_by(Job.job_pull_date.desc())
    offset = (page - 1) * limit
    jobs = q.offset(offset).limit(limit).all()
    pages = max(1, (total + limit - 1) // limit)
    return JobListResponse(
        jobs=[JobResponse.model_validate(j) for j in jobs],
        total=total, page=page, pages=pages, cohort_label=cohort_label,
    )

@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobResponse.model_validate(job)

@router.get("/cohorts")
def list_cohorts(db: Session = Depends(get_db)):
    cohorts = _load_cohorts()
    counts = dict(db.query(Job.cohort_tag, func.count(Job.id)).group_by(Job.cohort_tag).all())
    return [{"name": c["name"], "label": c["label"], "count": counts.get(c["name"], 0)} for c in cohorts]

@router.get("/filters/{cohort}")
def get_filters(cohort: str, db: Session = Depends(get_db)):
    base = db.query(Job).filter(Job.cohort_tag == cohort, Job.is_active == True)
    def unique_vals(col):
        rows = base.with_entities(col).filter(col != None).distinct().all()
        return sorted(set(r[0] for r in rows if r[0]))
    locations_raw = unique_vals(Job.location)
    cities = sorted(set(loc.split(",")[0].strip() for loc in locations_raw if loc))
    return {
        "locations": cities[:30],
        "companies": unique_vals(Job.company)[:50],
        "employment_types": unique_vals(Job.employment_type),
        "work_modes": unique_vals(Job.work_mode),
    }
