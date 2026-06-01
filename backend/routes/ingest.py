import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models import Job

router = APIRouter(prefix="/ingest", tags=["ingest"])

@router.get("/mock")
def insert_mock_jobs(db: Session = Depends(get_db)):
    mock_jobs = [{'hash_key': 'mock_google_swe_001', 'job_title': 'Software Engineer III', 'company': 'Google', 'source': 'via LinkedIn', 'location': 'Bangalore, Karnataka, India', 'description': 'Design and implement scalable backend services.\n**Key Responsibilities:**\n- Build high-performance APIs using Python and Java\n- Work with distributed systems\n- Code reviews and mentoring\n**Qualifications:**\n- 3-7 years experience\n- Strong Python or Java skills', 'best_apply_link': 'https://careers.google.com', 'apply_link_type': 'career_page', 'cohort_tag': 'tech-jobs', 'posted_date_parsed': '2 days ago', 'employment_type': 'Full-time', 'work_mode': 'Hybrid', 'experience': '3-7 years', 'salary_display': 'Not Disclosed', 'skills': 'Python, Java, SQL, Docker, Kubernetes', 'is_active': True}, {'hash_key': 'mock_microsoft_pm_002', 'job_title': 'Senior Product Manager - Remote', 'company': 'Microsoft', 'source': 'via Naukri', 'location': 'Remote, India', 'description': 'Lead Azure product strategy.\n**Key Responsibilities:**\n- Define product roadmap\n- Partner with engineering teams\n- Analyze customer data\n**Qualifications:**\n- 5+ years PM experience\n- Technical background preferred', 'best_apply_link': 'https://careers.microsoft.com', 'apply_link_type': 'career_page', 'cohort_tag': 'work-from-home-jobs', 'posted_date_parsed': '1 day ago', 'employment_type': 'Full-time', 'work_mode': 'Remote', 'experience': '5+ years', 'salary_display': '35-55 LPA', 'skills': 'Product Management, Agile, Azure, Data Analysis', 'is_active': True}, {'hash_key': 'mock_flipkart_ml_003', 'job_title': 'Machine Learning Engineer', 'company': 'Flipkart', 'source': 'via LinkedIn', 'location': 'Hyderabad, Telangana, India', 'description': 'Build ML models for recommendations.\n**Key Responsibilities:**\n- Build recommendation systems\n- Work with large datasets using Spark\n- MLOps pipelines\n**Qualifications:**\n- 2-5 years ML experience\n- Python and TensorFlow skills', 'best_apply_link': 'https://careers.flipkart.com', 'apply_link_type': 'career_page', 'cohort_tag': 'ai-ml-jobs', 'posted_date_parsed': '3 days ago', 'employment_type': 'Full-time', 'work_mode': 'Onsite', 'experience': '2-5 years', 'salary_display': '20-35 LPA', 'skills': 'Python, Machine Learning, TensorFlow, Spark, SQL', 'is_active': True}, {'hash_key': 'mock_razorpay_devops_004', 'job_title': 'DevOps Engineer - Work From Home', 'company': 'Razorpay', 'source': 'via Glassdoor', 'location': 'Work From Home, India', 'description': 'Manage infrastructure at Razorpay.\n**Key Responsibilities:**\n- Manage Kubernetes clusters on AWS\n- Build CI/CD pipelines\n- Monitoring with Prometheus\n**Qualifications:**\n- 3-6 years DevOps experience\n- AWS and Kubernetes expertise', 'best_apply_link': 'https://razorpay.com/jobs', 'apply_link_type': 'career_page', 'cohort_tag': 'work-from-home-jobs', 'posted_date_parsed': '5 hours ago', 'employment_type': 'Full-time', 'work_mode': 'Remote', 'experience': '3-6 years', 'salary_display': '18-30 LPA', 'skills': 'AWS, Kubernetes, Docker, Linux, Python, Terraform', 'is_active': True}, {'hash_key': 'mock_swiggy_ds_005', 'job_title': 'Data Scientist - Demand Forecasting', 'company': 'Swiggy', 'source': 'via LinkedIn', 'location': 'Bangalore, Karnataka, India', 'description': 'Solve forecasting problems at scale.\n**Key Responsibilities:**\n- Build demand forecasting models\n- Analyze large datasets\n- Present findings to stakeholders\n**Qualifications:**\n- 2-4 years data science experience\n- Strong Python and SQL', 'best_apply_link': 'https://careers.swiggy.com', 'apply_link_type': 'career_page', 'cohort_tag': 'ai-ml-jobs', 'posted_date_parsed': '1 week ago', 'employment_type': 'Full-time', 'work_mode': 'Hybrid', 'experience': '2-4 years', 'salary_display': '15-25 LPA', 'skills': 'Python, SQL, Machine Learning, TensorFlow, Spark', 'is_active': True}]
    inserted = skipped = 0
    for job_data in mock_jobs:
        exists = db.query(Job).filter(Job.hash_key == job_data["hash_key"]).first()
        if exists:
            skipped += 1
            continue
        db.add(Job(**job_data))
        inserted += 1
    db.commit()
    return {"message": "Mock jobs ready", "inserted": inserted, "skipped": skipped}

@router.get("/status")
def ingest_status(db: Session = Depends(get_db)):
    total = db.query(func.count(Job.id)).scalar()
    by_cohort = dict(db.query(Job.cohort_tag, func.count(Job.id)).group_by(Job.cohort_tag).all())
    return {"total_jobs": total, "by_cohort": by_cohort}
