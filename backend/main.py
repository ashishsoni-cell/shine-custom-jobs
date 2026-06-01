
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from backend.database import create_tables
from backend.routes.jobs import router as jobs_router
from backend.routes.ingest import router as ingest_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(title="Shine Custom Jobs API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../frontend")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(jobs_router)
app.include_router(ingest_router)

@app.get("/health")
def health():
    from backend.database import SessionLocal
    from backend.models import Job
    db = SessionLocal()
    try:
        count = db.query(Job).count()
        return {"status": "ok", "db_job_count": count}
    finally:
        db.close()

@app.get("/job/{job_id}")
def serve_job_page(job_id: int):
    path = os.path.join(FRONTEND_DIR, "job.html")
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse({"error": "job.html not found"}, status_code=404)

@app.get("/")
def serve_index():
    path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse({"message": "Shine Custom Jobs API running!"})
