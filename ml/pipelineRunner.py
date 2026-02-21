import json
import sys
import uuid
from pathlib import Path
from backend.config import DATABASE_URL
from .pipelines.pipeline import listingPipe, matchingPipe, resumePipe

from sqlalchemy import create_engine, text

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
PIPELINES_DIR = CURRENT_DIR / "pipelines"
MATCH_OUTPUT_DIR = PROJECT_ROOT / "data" / "match_data"
MATCH_OUTPUT_FILE = MATCH_OUTPUT_DIR / "resume_job_matches.json"

project_root_str = str(PROJECT_ROOT)
pipelines_dir_str = str(PIPELINES_DIR)

if project_root_str not in sys.path:
    sys.path.insert(0, project_root_str)
if pipelines_dir_str not in sys.path:
    sys.path.insert(0, pipelines_dir_str)



engine = create_engine(DATABASE_URL)


def to_serializable(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_serializable(v) for v in obj]
    return obj


def normalize_skills(value):
    if isinstance(value, list):
        return value
    return []


def extract_matching_rate(match_result):
    if isinstance(match_result, dict):
        raw_score = match_result.get("matching_score")
    else:
        raw_score = match_result

    try:
        return float(raw_score)
    except (TypeError, ValueError):
        return 0.0


def save_match_dataset(match_payloads):
    MATCH_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dataset = {
        "saved_matches": len(match_payloads),
        "matches": to_serializable(match_payloads),
    }
    MATCH_OUTPUT_FILE.write_text(
        json.dumps(dataset, indent=2),
        encoding="utf-8",
    )
    return MATCH_OUTPUT_FILE


if __name__ == "__main__":
    with engine.connect() as conn:
        resumes = conn.execute(
            text("SELECT * FROM candidate_resumes LIMIT 1")
        ).fetchall()

        jobs = conn.execute(
            text("SELECT * FROM market_jobs LIMIT 50")
        ).fetchall()

        match_payloads = []
        for resume_row in resumes:
            resume_data = resumePipe(
                {"skills": normalize_skills(resume_row[10])}
            )

            for job_row in jobs:
                job_data = listingPipe(
                    {
                        "title": job_row[1],
                        "skills": normalize_skills(job_row[5]),
                    }
                )
                match_result = matchingPipe(resume_data, job_data)

                payload = {
                    "job_id": job_row[0],
                    "user_gmail": str(resume_row[5] or "").strip(),
                    "matching_rate": extract_matching_rate(match_result),
                }
                match_payloads.append(payload)

    output_file = save_match_dataset(match_payloads)

    print(
        json.dumps(
            {
                "saved_matches": len(match_payloads),
                "output_file": str(output_file),
            },
            indent=2,
        )
    )
