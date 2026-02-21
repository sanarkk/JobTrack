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

engine = create_engine(DATABASE_URL)

def parse_skills(raw):
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(skill).strip() for skill in raw if str(skill).strip()]
    if isinstance(raw, tuple):
        return [str(skill).strip() for skill in raw if str(skill).strip()]

    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return [str(skill).strip() for skill in parsed if str(skill).strip()]
        except Exception:
            pass
        return [s.strip() for s in raw.split(",") if s.strip()]

    return []

def load_resume_path():
    samples_dir = os.path.join(CURRENT_DIR, "samples")
    files = [f for f in os.listdir(samples_dir) if f.startswith("resume")]
    return os.path.join(samples_dir, files[0])

if __name__ == "__main__":
    resume_path = load_resume_path()
    resume_processed = resumePipe(resume_path)

    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT job_title, technical_tools FROM market_jobs LIMIT 10")
        ).mappings().all()

        for posting in rows:
            title = posting.get("job_title") or ""
            skills = parse_skills(posting.get("technical_tools"))

            listing_processed = listingPipe({
                "title": title,
                "skills": skills
            })

            match_processed = matchingPipe(resume_processed, listing_processed)

            print(json.dumps({
                "resume": resume_processed,
                "listing": listing_processed,
                "match": match_processed
            }, 
            indent=2))
