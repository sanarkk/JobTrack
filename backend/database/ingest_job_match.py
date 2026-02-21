import argparse
import json
from pathlib import Path

from sqlalchemy import text as sql_text

from backend.database.session import SessionLocal
from backend.models.resume_job_match_model import ResumeJobMatch


def load_json(json_path):
    return json.loads(Path(json_path).read_text(encoding="utf-8"))


def extract_match_objects(payload):
    if isinstance(payload, dict):
        matches = payload.get("matches")
        if isinstance(matches, list):
            return matches
        return [payload]

    if isinstance(payload, list):
        return payload

    raise ValueError("Unsupported JSON structure: expected dict or list.")


def has_matching_rate_column(db):
    query = sql_text(
        """
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name = 'resume_job_match'
          AND column_name = 'matching_rate'
        LIMIT 1
        """
    )
    return db.execute(query).scalar() is not None


def ingest_json_file(json_path):
    path = Path(json_path)
    if path.suffix.lower() != ".json":
        path = Path(f"{path}.json")

    payload = load_json(path)
    match_objects = extract_match_objects(payload)

    db = SessionLocal()
    inserted = 0
    skipped = 0
    try:
        include_matching_rate = has_matching_rate_column(db)

        for match_obj in match_objects:
            row = match_obj or {}
            job_id = str(row.get("job_id") or "").strip()
            user_gmail = str(row.get("user_gmail") or "").strip()

            if not job_id or not user_gmail:
                skipped += 1
                continue

            if include_matching_rate:
                raw_matching_rate = row.get("matching_rate")
                try:
                    matching_rate = float(raw_matching_rate)
                except (TypeError, ValueError):
                    matching_rate = 0.0

                db.execute(
                    sql_text(
                        """
                        INSERT INTO resume_job_match (job_id, user_gmail, matching_rate)
                        VALUES (:job_id, :user_gmail, :matching_rate)
                        """
                    ),
                    {
                        "job_id": job_id,
                        "user_gmail": user_gmail,
                        "matching_rate": matching_rate,
                    },
                )
            else:
                db.add(
                    ResumeJobMatch(
                        job_id=job_id,
                        user_gmail=user_gmail,
                    )
                )
            inserted += 1

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    return {
        "file": str(path),
        "total": len(match_objects),
        "inserted": inserted,
        "skipped": skipped,
        "include_matching_rate": include_matching_rate,
    }


def main():
    parser = argparse.ArgumentParser(description="Ingest resume-job match JSON file into resume_job_match")
    parser.add_argument("json_file")
    args = parser.parse_args()

    result = ingest_json_file(args.json_file)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
