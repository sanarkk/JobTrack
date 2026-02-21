import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from backend.database.session import SessionLocal
from backend.models.candidate_model import CandidateResume


def load_json(json_path):
    return json.loads(Path(json_path).read_text(encoding="utf-8"))


def ingest_json_file(json_path):
    path = Path(json_path)
    if path.suffix.lower() != ".json":
        path = Path(f"{path}.json")

    payload = load_json(path)

    source = payload.get("source", {})
    profile = payload.get("profile", {})
    summary = payload.get("summary", {})
    user_email = str(payload.get("user_email") or "").strip()

    if not user_email:
        raise ValueError(f"Missing required user_email in payload: {path}")

    resume_payload = {
        "user_email": user_email,
        "file_name": source.get("file_name") or path.name,
        "file_path": source.get("file_path") or str(path),
        "extension": source.get("extension") or path.suffix,
        "profile_name": profile.get("name"),
        "mobile_number": profile.get("mobile_number"),
        "designation": profile.get("designation"),
        "total_experience": profile.get("total_experience"),
        "education": profile.get("education"),
        "skills": payload.get("skills") or [],
        "company_names": payload.get("company_names") or [],
        "ai_summary": summary.get("ai_summary"),
        "ai_strengths": summary.get("ai_strengths") or [],
        "experiences": payload.get("experiences") or [],
        "resume_json": payload,
    }

    db = SessionLocal()
    try:
        existing_rows = (
            db.query(CandidateResume)
            .filter(CandidateResume.user_email == user_email)
            .order_by(CandidateResume.updated_at.desc(), CandidateResume.created_at.desc())
            .all()
        )

        if existing_rows:
            current_row = existing_rows[0]
            for field, value in resume_payload.items():
                setattr(current_row, field, value)
            current_row.updated_at = datetime.now(timezone.utc)

            # Keep one record per user_email in case duplicates already exist.
            for duplicate_row in existing_rows[1:]:
                db.delete(duplicate_row)

            inserted = 0
            updated = 1
        else:
            db.add(CandidateResume(**resume_payload))
            inserted = 1
            updated = 0

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

    return {"inserted": inserted, "updated": updated, "file": str(path), "user_email": user_email}


def main():
    parser = argparse.ArgumentParser(description="Ingest one resume JSON into candidate_resumes")
    parser.add_argument("json_file")
    args = parser.parse_args()

    result = ingest_json_file(args.json_file)
    print(result)


if __name__ == "__main__":
    main()
