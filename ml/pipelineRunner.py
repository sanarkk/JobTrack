# import os
# import sys
# import json

# from sqlalchemy import create_engine, text

# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
# sys.path.insert(0, PROJECT_ROOT)
# sys.path.insert(0, os.path.join(CURRENT_DIR, "pipelines"))

# from backend.config import DATABASE_URL
# from pipelines.pipeline import listingPipe, resumePipe, matchingPipe

# engine = create_engine(DATABASE_URL)

# def parse_skills(skills):
#     try:
#         return json.loads(skills)
#     except:
#         return [s.strip() for s in skills.split(",")]

# if __name__ == "__main__":
#     with engine.connect() as conn:

#         resumes = conn.execute(
#             text("SELECT * FROM candidate_resumes LIMIT 2")
#         ).fetchall()
        
#         print(resumes)

#         jobs = conn.execute(
#             text("SELECT * FROM market_jobs LIMIT 2")
#         ).fetchall()

#         processed_resumes = []
#         for r in resumes:
#             resume_path = r[4]
#             processed_resumes.append({
#                 "resume_id": r[0],
#                 "data": resumePipe(resume_path)
#             })

#         processed_jobs = []
#         for j in jobs:
#             title = j[1]
#             skills = parse_skills(j[11])
#             processed_jobs.append({
#                 "job_id": j[0],
#                 "data": listingPipe({
#                     "title": title,
#                     "skills": skills
#                 })
#             })

#         for resume in processed_resumes:
#             for job in processed_jobs:
#                 match = matchingPipe(resume["data"], job["data"])
#                 print(json.dumps({
#                     "resume_id": resume["resume_id"],
#                     "job_id": job["job_id"],
#                     "resume": resume["data"],
#                     "job": job["data"],
#                     "match": match
#                 }, indent=2))


import os
import sys
import json
from sqlalchemy import create_engine, text

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(CURRENT_DIR, "pipelines"))

from backend.config import DATABASE_URL
from pipelines.pipeline import listingPipe, resumePipe, matchingPipe

import uuid

def to_serializable(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_serializable(v) for v in obj]
    return obj

engine = create_engine(DATABASE_URL)

def normalize_skills(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return []

if __name__ == "__main__":
    with engine.connect() as conn:
        resumes = conn.execute(
            text("SELECT * FROM candidate_resumes LIMIT 1")
        ).fetchall()

        jobs = conn.execute(
            text("SELECT * FROM market_jobs LIMIT 50")
        ).fetchall()

        processed_resumes = []
        for r in resumes:
            resume_dict = {
                "skills": normalize_skills(r[10])
            }
            processed_resumes.append({
                "resume_id": str(r[0]),
                "data": resumePipe(resume_dict)
            })

        processed_jobs = []
        for j in jobs:
            title = j[1]
            skills = normalize_skills(j[5])
            processed_jobs.append({
                "job_id": j[0],
                "data": listingPipe({
                    "title": title,
                    "skills": skills
                })
            })

        for resume in processed_resumes:
            for job in processed_jobs:
                match = matchingPipe(resume["data"], job["data"])
                print(json.dumps(
                to_serializable({
                    "resume_id": resume["resume_id"],
                    "job_id": job["job_id"],
                    "match": match
                }),
                indent=2
            ))