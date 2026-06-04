from fastapi import FastAPI
from pydantic import BaseModel
from src.skill_counter import detect_skills

app = FastAPI()


class JobDescriptionRequest(BaseModel):
    description: str

class JobPost(BaseModel):
    job_title: str
    description: str

class AnalyzeJobsRequest(BaseModel):
    jobs: list[JobPost]

@app.get("/")
def home():
    return {"message": "CS Career Skill Analyzer API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/detect-skills")
def detect_skills_from_description(request: JobDescriptionRequest):
    skills_detected = detect_skills(request.description)

    return {
        "description": request.description,
        "skills_detected": skills_detected,
        "total_skills_detected": len(skills_detected)
    }

@app.post("/analyze-jobs")
def analyze_jobs(request: AnalyzeJobsRequest):
    skill_count = {}

    for job in request.jobs:
        skills_detected = detect_skills(job.description)

        for skill in skills_detected:
            skill_count[skill] = skill_count.get(skill, 0) + 1
    
    return {
        "total_jobs": len(request.jobs),
        "skill_count": skill_count
    }