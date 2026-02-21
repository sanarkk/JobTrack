import argparse
import json
from pathlib import Path

from sqlalchemy import text

from backend.database.session import SessionLocal

INSERT_SQL = text(
    """
    insert into candidate_resumes (file_name, resume_json)
    values (:file_name, cast(:resume_json as jsonb))
    """
)


def load_json(json_path):
    return json.loads(Path(json_path).read_text(encoding="utf-8"))


def ingest_json_file(json_path):
    path = Path(json_path)
    payload = load_json(path)

    file_name = path.name
    if isinstance(payload, dict):
        source = payload.get("source") or {}
        file_name = source.get("file_name") or file_name

    db = SessionLocal()
    db.execute(
        INSERT_SQL,
        {
            "file_name": file_name,
            "resume_json": json.dumps(payload, ensure_ascii=False),
        },
    )
    db.commit()
    db.close()

    return {"inserted": 1, "file": str(path)}

def main():
    parser = argparse.ArgumentParser(
        description="Ingest one resume JSON into candidate_resumes"
    )
    parser.add_argument("json_file")
    args = parser.parse_args()
    result = ingest_json_file(args.json_file)
    print(result)


if __name__ == "__main__":
    main()
