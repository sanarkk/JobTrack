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
    try:
        return json.loads(raw)
    except:
        return [s.strip() for s in raw.split(",")]

def load_resume_path():
    samples_dir = os.path.join(CURRENT_DIR, "samples")
    files = [f for f in os.listdir(samples_dir) if f.startswith("resume")]
    return os.path.join(samples_dir, files[0])

if __name__ == "__main__":
    resume_path = load_resume_path()
    resume_processed = resumePipe(resume_path)

    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM market_jobs LIMIT 10")).fetchall()

        for posting in rows:
            title = posting[1]
            skills = parse_skills(posting[11])

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