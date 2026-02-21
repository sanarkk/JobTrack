import argparse
import json
import uuid
from fastapi import APIRouter, UploadFile, File, Form
import shutil
from pathlib import Path
from pathlib import Path
from backend.database.ingest_resumes import ingest_json_file
from ml.agents.extraction_agent import ExtractionAgent
from .text_from_file import extract_text_by_file_type

parser_router = APIRouter()


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(value).strip()] if str(value).strip() else []


def _as_string(value):
    if value is None:
        return ""
    return str(value).strip()


def normalize_resume_schema(raw, source_file):
    source_path = Path(source_file).resolve()
    experiences = raw.get("experiences") if isinstance(raw.get("experiences"), list) else []

    normalized_experiences = []
    for exp in experiences:
        if not isinstance(exp, dict):
            continue
        normalized_experiences.append(
            {
                "designation": _as_string(exp.get("designation")),
                "company": _as_string(exp.get("company")),
                "start_date": _as_string(exp.get("start_date")),
                "end_date": _as_string(exp.get("end_date")),
                "job_description": _as_string(exp.get("job_description")),
            }
        )

    return {
        "source": {
            "file_name": source_path.name,
            "file_path": str(source_path),
            "extension": source_path.suffix.lower(),
        },
        "profile": {
            "name": _as_string(raw.get("name")),
            "email": _as_string(raw.get("email")),
            "mobile_number": _as_string(raw.get("mobile_number")),
            "designation": _as_string(raw.get("designation")),
            "total_experience": _as_string(raw.get("total_experience")),
            "education": _as_string(raw.get("education")),
        },
        "skills": _as_list(raw.get("skills")),
        "company_names": _as_list(raw.get("company_names")),
        "summary": {
            "ai_summary": _as_string(raw.get("ai_summary")),
            "ai_strengths": _as_list(raw.get("ai_strengths")),
        },
        "experiences": normalized_experiences,
    }


def process_cv(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Resume file not found: {path}")

    extracted_text = extract_text_by_file_type(path)
    if not extracted_text.strip():
        raise ValueError(f"No text extracted from file: {path}")

    agent = ExtractionAgent()
    raw_output = agent.extract_entities(extracted_text)
    return normalize_resume_schema(raw_output, path)

@parser_router.post("/resume/")
async def main(user_email: str = Form(...), file: UploadFile = File(...)):
    # parser = argparse.ArgumentParser(description="Process CV into a stable JSON schema.")
    # parser.add_argument("resume_file", help="Path to resume file (.pdf or .docx)")
    # args = parser.parse_args()
    # resume_name = args.resume_file
    extension = Path(file.filename).suffix.lower()

    BASE_DIR = Path(__file__).resolve().parents[2]
    UPLOAD_DIR = BASE_DIR / "data" / "resume_in"
    ALLOWED_EXTENSIONS = {".pdf", ".docx"}

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    unique_name = f"{uuid.uuid4()}{extension}"
    file_path = UPLOAD_DIR / unique_name


    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    in_dir = Path(__file__).resolve().parents[2] / "data" / "resume_in"
    out_dir = Path(__file__).resolve().parents[2] / "data" / "resume_out"
    
    result = process_cv(in_dir / unique_name)
    result["user_email"] = user_email
    
    output_json = json.dumps(result, indent=2, ensure_ascii=False)

    out_path = out_dir / f"{unique_name}.json"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output_json)

    print(f"Saved normalized CV JSON to {(out_dir / unique_name).resolve()}")
    ingest_result = ingest_json_file(out_dir / unique_name)

    print(f"Ingested resume JSON to Supabase: {ingest_result}")

    return result




if __name__ == "__main__":
    main()
