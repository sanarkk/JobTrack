import argparse
import json
from pathlib import Path

from backend.database.session import SessionLocal
from backend.models.candidate_model import CandidateResume


def load_json(json_path):
    return json.loads(Path(json_path).read_text(encoding="utf-8"))


def ingest_json_file(json_path):
    path = Path(str(json_path) + ".json")
    payload = load_json(path)

    source = payload.get("source", {})
    profile = payload.get("profile", {})
    summary = payload.get("summary", {})
    user_email_ad = payload.get("user_email", {})

    resume = CandidateResume(
        user_email=user_email_ad,
        file_name=source.get("file_name") or path.name,
        file_path=source.get("file_path") or str(path),
        extension=source.get("extension") or path.suffix,

        profile_name=profile.get("name"),
        mobile_number=profile.get("mobile_number"),
        designation=profile.get("designation"),
        total_experience=profile.get("total_experience"),
        education=profile.get("education"),

        skills=payload.get("skills") or [],
        company_names=payload.get("company_names") or [],

        ai_summary=summary.get("ai_summary"),
        ai_strengths=summary.get("ai_strengths") or [],

        experiences=payload.get("experiences") or [],

        resume_json=payload,
    )

    db = SessionLocal()
    db.add(resume)
    db.commit()
    db.close()

    return {"inserted": 1, "file": str(path)}


def main():
    parser = argparse.ArgumentParser(description="Ingest one resume JSON into candidate_resumes")
    parser.add_argument("json_file")
    args = parser.parse_args()

    result = ingest_json_file(args.json_file)
    print(result)


if __name__ == "__main__":
    main()