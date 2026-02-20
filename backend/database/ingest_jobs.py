import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
import pandas as pd

from backend.database.session import Base, SessionLocal, engine
from backend.models.position_model import Position


def build_jobs_dataframe(raw_dir="data/raw"):
    raw_path = Path(raw_dir)
    rows = []
    source_files = []

    for file_path in sorted(raw_path.glob("*.json")):
        jobs = json.loads(file_path.read_text(encoding="utf-8"))
        search_term = file_path.stem.replace("_jobs", "").replace("_", " ").strip().lower()

        for job in jobs:
            processed = job.get("v5_processed_job_data") or {}
            job_info = job.get("job_information") or {}
            company = job.get("enriched_company_data") or {}

            salary_min = processed.get("yearly_min_compensation")
            salary_max = processed.get("yearly_max_compensation")
            salary_mid = None
            if isinstance(salary_min, (int, float)) and isinstance(salary_max, (int, float)):
                salary_mid = (salary_min + salary_max) / 2

            row = {
                "id": str(job.get("id") or job.get("objectID") or ""),
                "search_term": search_term,
                "salary_min": str(salary_min if salary_min is not None else "0"),
                "salary_max": str(salary_max if salary_max is not None else "0"),
                "salary_mid": str(salary_mid if salary_mid is not None else "0"),
                "core_job_title": str(
                    processed.get("core_job_title")
                    or job_info.get("title")
                    or job_info.get("job_title_raw")
                    or "unknown"
                ),
                "location": str(processed.get("workplace_states") or "unknown"),
                "date_posted": processed.get("estimated_publish_date"),
                "description": str(job_info.get("description") or ""),
                "job_category": str(processed.get("job_category") or "unknown"),
                "seniority_level": str(processed.get("seniority_level") or "unknown"),
                "technical_tools": processed.get("technical_tools") or [],
                "workplace_type": str(processed.get("workplace_type") or "unknown"),
                "company_industry": company.get("industries") or [],
                "company_size": str(company.get("nb_employees") or "unknown"),
                "company_sector_and_industry": str(
                    processed.get("company_sector_and_industry") or "unknown"
                ),
                "min_industry_and_role_yoe": (
                    None
                    if processed.get("min_industry_and_role_yoe") is None
                    else str(processed.get("min_industry_and_role_yoe"))
                ),
                "listed_compensation_currency": str(
                    processed.get("listed_compensation_currency") or "unknown"
                ),
                "source_file": str(file_path),
            }
            rows.append(row)

        source_files.append(file_path)

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df[df["id"].str.len() > 0].copy()
        df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
        df["date_posted"] = df["date_posted"].fillna(pd.Timestamp.utcnow())

    return df, source_files


def ingest_dataframe_to_supabase(df, batch_size=200):
    db = SessionLocal()

    if df.empty:
        db.close()
        return {"total": 0, "inserted": 0, "updated": 0}

    ids = df["id"].astype(str).drop_duplicates().tolist()
    existing_rows = db.query(Position.id).filter(Position.id.in_(ids)).all()
    existing_ids = {row[0] for row in existing_rows}

    inserted = 0
    updated = 0

    for idx, row in df.iterrows():
        payload = row.to_dict()

        if hasattr(payload["date_posted"], "to_pydatetime"):
            payload["date_posted"] = payload["date_posted"].to_pydatetime()

        if payload["id"] in existing_ids:
            updated += 1
        else:
            inserted += 1
            existing_ids.add(payload["id"])

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


def move_raw_files_to_processed(file_paths, processed_dir="data/processed"):
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
    parser.add_argument("--raw_dir", default="data/raw")
    parser.add_argument("--processed_dir", default="data/processed")
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
