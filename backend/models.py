from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    google_job_id: Mapped[Optional[str]] = mapped_column(String(500), unique=True, nullable=True)
    job_pull_date: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    posted_on_raw: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    posted_date_parsed: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    employment_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    job_title: Mapped[str] = mapped_column(String(300), index=True)
    company: Mapped[str] = mapped_column(String(200), index=True)
    source: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    apply_options: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    best_apply_link: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    apply_link_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    hash_key: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    thumbnail: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cohort_tag: Mapped[str] = mapped_column(String(200), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    salary_display: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    work_mode: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    experience: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    skills: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
