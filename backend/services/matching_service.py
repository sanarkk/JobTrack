from __future__ import annotations

import re
from typing import Iterable

try:
    import torch
    from sentence_transformers import SentenceTransformer
except Exception as exc:  # pragma: no cover - import/runtime environment specific
    torch = None  # type: ignore[assignment]
    SentenceTransformer = None  # type: ignore[assignment]
    _IMPORT_ERROR: Exception | None = exc
else:
    _IMPORT_ERROR = None


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LEXICAL_WEIGHT = 0.45
SEMANTIC_WEIGHT = 0.45
TITLE_WEIGHT = 0.10

_PUNCT_RE = re.compile(r"[^a-z0-9\s]+")
_SPACE_RE = re.compile(r"\s+")
_TEXT_REPLACEMENTS = {
    "c++": "cpp",
    "c#": "csharp",
    ".net": " dotnet ",
    "node.js": "nodejs",
    "postgresql": "postgres",
}

_MODEL = None
_MODEL_LOAD_ERROR: Exception | None = None


class MatchingModelUnavailableError(RuntimeError):
    """Raised when the sentence embedding model is unavailable."""


def _load_model() -> None:
    global _MODEL, _MODEL_LOAD_ERROR

    if _MODEL is not None or _MODEL_LOAD_ERROR is not None:
        return

    if _IMPORT_ERROR is not None:
        _MODEL_LOAD_ERROR = _IMPORT_ERROR
        return

    try:
        _MODEL = SentenceTransformer(MODEL_NAME)
    except Exception as exc:  # pragma: no cover - environment/model specific
        _MODEL_LOAD_ERROR = exc


_load_model()


def assert_model_ready() -> None:
    _load_model()
    if _MODEL_LOAD_ERROR is not None:
        raise RuntimeError(f"Failed to load matching model '{MODEL_NAME}'.") from _MODEL_LOAD_ERROR
    if _MODEL is None:
        raise RuntimeError(f"Matching model '{MODEL_NAME}' is not initialized.")


def normalize_text(value: str | None) -> str:
    if not value:
        return ""

    text = value.strip().lower()
    for source, target in _TEXT_REPLACEMENTS.items():
        text = text.replace(source, target)
    text = _PUNCT_RE.sub(" ", text)
    text = _SPACE_RE.sub(" ", text).strip()
    return text


def normalize_skills(skills: Iterable[str] | None) -> list[str]:
    if not skills:
        return []

    normalized: list[str] = []
    seen: set[str] = set()
    for skill in skills:
        clean_skill = normalize_text(skill)
        if clean_skill and clean_skill not in seen:
            seen.add(clean_skill)
            normalized.append(clean_skill)
    return normalized


def _require_model() -> SentenceTransformer:
    _load_model()
    if _MODEL_LOAD_ERROR is not None:
        raise MatchingModelUnavailableError(
            f"Unable to initialize matching model '{MODEL_NAME}'."
        ) from _MODEL_LOAD_ERROR
    if _MODEL is None:
        raise MatchingModelUnavailableError(f"Matching model '{MODEL_NAME}' is unavailable.")
    return _MODEL


def _encode_texts(texts: Iterable[str], embedding_cache: dict[str, torch.Tensor]) -> None:
    missing = [text for text in dict.fromkeys(texts) if text and text not in embedding_cache]
    if not missing:
        return

    model = _require_model()
    encoded = model.encode(
        missing,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    if not isinstance(encoded, torch.Tensor):
        encoded = torch.tensor(encoded)
    if encoded.dim() == 1:
        encoded = encoded.unsqueeze(0)

    for idx, text in enumerate(missing):
        embedding_cache[text] = encoded[idx]


def _semantic_skill_score(
    resume_skills: list[str],
    job_skills: list[str],
    embedding_cache: dict[str, torch.Tensor],
) -> float:
    if not resume_skills or not job_skills:
        return 0.0

    _encode_texts([*resume_skills, *job_skills], embedding_cache)

    resume_embeddings = torch.stack([embedding_cache[skill] for skill in resume_skills])
    job_embeddings = torch.stack([embedding_cache[skill] for skill in job_skills])

    similarity_matrix = torch.matmul(job_embeddings, resume_embeddings.T)
    best_match_per_job_skill = torch.max(similarity_matrix, dim=1).values
    clamped_scores = torch.clamp(best_match_per_job_skill, min=0.0, max=1.0)
    return float(clamped_scores.mean().item())


def _title_similarity(
    resume_title: str | None,
    job_title: str | None,
    embedding_cache: dict[str, torch.Tensor],
) -> float:
    normalized_resume_title = normalize_text(resume_title)
    normalized_job_title = normalize_text(job_title)
    if not normalized_resume_title or not normalized_job_title:
        return 0.0

    _encode_texts([normalized_resume_title, normalized_job_title], embedding_cache)
    similarity = torch.dot(
        embedding_cache[normalized_resume_title],
        embedding_cache[normalized_job_title],
    ).item()
    return float(max(0.0, min(1.0, similarity)))


def compute_match_score(
    resume_skills: Iterable[str] | None,
    job_skills: Iterable[str] | None,
    resume_title: str | None,
    job_title: str | None,
) -> float:
    normalized_resume_skills = normalize_skills(resume_skills)
    normalized_job_skills = normalize_skills(job_skills)

    if not normalized_job_skills:
        return 0.0

    resume_set = set(normalized_resume_skills)
    job_set = set(normalized_job_skills)
    lexical_score = len(resume_set.intersection(job_set)) / max(len(job_set), 1)

    embedding_cache: dict[str, torch.Tensor] = {}
    semantic_score = _semantic_skill_score(
        resume_skills=normalized_resume_skills,
        job_skills=normalized_job_skills,
        embedding_cache=embedding_cache,
    )
    title_score = _title_similarity(
        resume_title=resume_title,
        job_title=job_title,
        embedding_cache=embedding_cache,
    )

    final_score = 100 * (
        (LEXICAL_WEIGHT * lexical_score)
        + (SEMANTIC_WEIGHT * semantic_score)
        + (TITLE_WEIGHT * title_score)
    )
    return round(float(max(0.0, min(100.0, final_score))), 4)
