import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd

from backend.database.session import Base, SessionLocal, engine
from backend.models.position_model import Position

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DEFAULT_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def build_jobs_dataframe(raw_dir=DEFAULT_RAW_DIR):
    raw_path = Path(raw_dir)
    rows = []
    source_files = []

    for file_path in sorted(raw_path.glob("*.json")):
        jobs = json.loads(file_path.read_text(encoding="utf-8"))

        for job in jobs:
            processed = job.get("v5_processed_job_data") or {}
            row = {
                "job_title": processed.get("core_job_title"),
                "job_category": processed.get("job_category"),
                "seniority_level": processed.get("seniority_level"),
                "requirements_summary": processed.get("requirements_summary"),
                "technical_tools": processed.get("technical_tools"),
                "formatted_workplace_location": processed.get("formatted_workplace_location"),
                "province": processed.get("workplace_states"),
                "commitment": processed.get("commitment"),
                "workplace_type": processed.get("workplace_type"),
                "yearly_min_compensation": processed.get("yearly_min_compensation"),
                "yearly_max_compensation": processed.get("yearly_max_compensation"),
                "company_name": processed.get("company_name"),
                "apply_url": job.get("apply_url"),
                "source_file": file_path,
                "hash": job.get("id")
            }
            rows.append(row)

        source_files.append(file_path)

    df = pd.DataFrame(rows)
    return df, source_files


def ingest_dataframe_to_supabase(df, batch_size=200):
    db = SessionLocal()

    if df.empty:
        db.close()
        return {"total": 0, "inserted": 0, "updated": 0}

    ids = df["hash"].astype(str).drop_duplicates().tolist()
    existing_rows = db.query(Position.hash).filter(Position.hash.in_(ids)).all()
    existing_ids = {row[0] for row in existing_rows}

    inserted = 0
    updated = 0

    for idx, row in df.iterrows():
        payload = row.to_dict()

        if payload["hash"] in existing_ids:
            updated += 1
        else:
            inserted += 1
            existing_ids.add(payload["hash"])

        payload.pop("source_file", None)
        db.merge(Position(**payload))

        if (idx + 1) % batch_size == 0:
            db.commit()

    db.commit()
    db.close()

    return {
        "total": len(df),
        "inserted": inserted,
        "updated": updated,
    }


def move_raw_files_to_processed(file_paths, processed_dir=DEFAULT_PROCESSED_DIR):
    processed_path = Path(processed_dir)

    moved_files = []
    for src in file_paths:
        src_path = Path(src)
        dst_path = processed_path / src_path.name

        if dst_path.exists():
            suffix = datetime.now().strftime("%Y%m%d%H%M%S")
            dst_path = processed_path / f"{src_path.stem}_{suffix}{src_path.suffix}"

        shutil.move(str(src_path), str(dst_path))
        moved_files.append(dst_path)

    return moved_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_dir", default=str(DEFAULT_RAW_DIR))
    parser.add_argument("--processed_dir", default=str(DEFAULT_PROCESSED_DIR))
    parser.add_argument("--batch_size", type=int, default=200)
    args = parser.parse_args()

    df, source_files = build_jobs_dataframe(raw_dir=args.raw_dir)
    summary = ingest_dataframe_to_supabase(df=df, batch_size=args.batch_size)
    moved_files = move_raw_files_to_processed(
        source_files, processed_dir=args.processed_dir
    )

    result = {
        "dataframe_rows": len(df),
        "ingestion": summary,
        "moved_files": [str(p) for p in moved_files],
    }
    print(result)


if __name__ == "__main__":
    main()
