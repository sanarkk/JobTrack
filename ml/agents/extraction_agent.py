import json
import re
from typing import Any, Dict
from .base_agent import BaseAgent


class ExtractionAgent(BaseAgent):
    _MAX_MODEL_OUTPUT_TOKENS = 1200

    @staticmethod
    def _empty_schema() -> Dict[str, Any]:
        return {
            "name": "",
            "email": "",
            "mobile_number": "",
            "skills": [],
            "company_names": [],
            "education": "",
            "designation": "",
            "total_experience": "",
            "ai_summary": "",
            "ai_strengths": [],
            "experiences": [],
        }

    @staticmethod
    def _extract_first_json_object(raw_text: str) -> str:
        start = raw_text.find("{")
        if start == -1:
            return raw_text.strip()

        in_string = False
        escaped = False
        depth = 0
        for idx in range(start, len(raw_text)):
            ch = raw_text[idx]
            if escaped:
                escaped = False
                continue
            if ch == "\\":
                escaped = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == "{":
                depth += 1
                continue
            if ch == "}":
                depth -= 1
                if depth == 0:
                    return raw_text[start : idx + 1].strip()
        return raw_text[start:].strip()

    @staticmethod
    def _repair_truncated_json(raw_json: str) -> str:
        repaired = raw_json.strip()
        if not repaired:
            return repaired

        # Fix malformed adjacent quoted segments seen in corrupt model output,
        # e.g. "React-Rout "Heroicons", -> "React-Rout Heroicons",
        repaired = re.sub(
            r'"([^"\n]*)\s+"([^"\n]*)"',
            lambda m: f'"{m.group(1).rstrip()} {m.group(2).lstrip()}"',
            repaired,
        )

        in_string = False
        escaped = False
        curly_depth = 0
        square_depth = 0
        for ch in repaired:
            if escaped:
                escaped = False
                continue
            if ch == "\\":
                escaped = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == "{":
                curly_depth += 1
            elif ch == "}":
                curly_depth = max(0, curly_depth - 1)
            elif ch == "[":
                square_depth += 1
            elif ch == "]":
                square_depth = max(0, square_depth - 1)

        if in_string:
            if escaped:
                repaired += " "
            repaired += '"'

        repaired = re.sub(r",\s*([}\]])", r"\1", repaired)

        if square_depth > 0:
            repaired += "]" * square_depth
        if curly_depth > 0:
            repaired += "}" * curly_depth
        return repaired

    @staticmethod
    def _extract_string_field(raw_text: str, field: str) -> str:
        match = re.search(
            rf'"{re.escape(field)}"\s*:\s*"((?:\\.|[^"\\])*)"',
            raw_text,
            re.DOTALL,
        )
        if not match:
            return ""
        value = match.group(1).replace('\\"', '"').replace("\\n", " ").strip()
        return value

    @staticmethod
    def _find_matching_bracket(raw_text: str, start_idx: int) -> int:
        in_string = False
        escaped = False
        depth = 0

        for idx in range(start_idx, len(raw_text)):
            ch = raw_text[idx]
            if escaped:
                escaped = False
                continue
            if ch == "\\":
                escaped = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return idx
        return -1

    def _extract_array_field(self, raw_text: str, field: str, limit: int) -> list:
        key_match = re.search(rf'"{re.escape(field)}"\s*:\s*\[', raw_text)
        if not key_match:
            return []

        start_idx = raw_text.find("[", key_match.start())
        if start_idx == -1:
            return []

        end_idx = self._find_matching_bracket(raw_text, start_idx)
        if end_idx == -1:
            chunk = raw_text[start_idx + 1 :]
        else:
            chunk = raw_text[start_idx + 1 : end_idx]

        # Re-run the malformed quote repair on array fragment.
        chunk = re.sub(
            r'"([^"\n]*)\s+"([^"\n]*)"',
            lambda m: f'"{m.group(1).rstrip()} {m.group(2).lstrip()}"',
            chunk,
        )

        values = []
        for match in re.finditer(r'"((?:\\.|[^"\\])*)"', chunk):
            value = match.group(1).replace('\\"', '"').replace("\\n", " ")
            value = re.sub(r"\s+", " ", value).strip(" ,;\t\r\n")
            if not value:
                continue
            if not re.search(r"[A-Za-z0-9]", value):
                continue
            if value:
                values.append(value)
            if len(values) >= limit:
                break
        return values

    def _recover_partial_schema(self, raw_text: str) -> Dict[str, Any]:
        recovered = self._empty_schema()

        recovered["name"] = self._extract_string_field(raw_text, "name")
        recovered["email"] = self._extract_string_field(raw_text, "email")
        recovered["mobile_number"] = self._extract_string_field(raw_text, "mobile_number")
        recovered["education"] = self._extract_string_field(raw_text, "education")
        recovered["designation"] = self._extract_string_field(raw_text, "designation")
        recovered["total_experience"] = self._extract_string_field(raw_text, "total_experience")
        recovered["ai_summary"] = self._extract_string_field(raw_text, "ai_summary")

        recovered["skills"] = self._extract_array_field(raw_text, "skills", limit=25)
        recovered["company_names"] = self._extract_array_field(raw_text, "company_names", limit=10)
        recovered["ai_strengths"] = self._extract_array_field(raw_text, "ai_strengths", limit=5)

        # Experience recovery from malformed blobs is intentionally conservative.
        recovered["experiences"] = []
        return recovered

    @staticmethod
    def _has_meaningful_data(payload: Dict[str, Any]) -> bool:
        for value in payload.values():
            if isinstance(value, str) and value.strip():
                return True
            if isinstance(value, list) and len(value) > 0:
                return True
        return False

    def _decode_response_json(self, response_content: str) -> Dict[str, Any]:
        if not response_content:
            return self._empty_schema()

        parse_error = None
        candidates = []
        raw = response_content.strip()
        if raw:
            candidates.append(raw)

        extracted = self._extract_first_json_object(raw)
        if extracted and extracted not in candidates:
            candidates.append(extracted)

        repaired = self._repair_truncated_json(extracted or raw)
        if repaired and repaired not in candidates:
            candidates.append(repaired)

        for candidate in candidates:
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, dict):
                    merged = self._empty_schema()
                    merged.update(parsed)
                    return merged
            except json.JSONDecodeError as err:
                parse_error = err

        recovered = self._recover_partial_schema(raw)
        if self._has_meaningful_data(recovered):
            print("ExtractionAgent: Recovered partial schema from malformed JSON output.")
            return recovered

        if parse_error is not None:
            print(f"ExtractionAgent: Failed to decode JSON. Error: {parse_error}")
            print(f"RAW CONTENT: {repr(response_content)}")
        return self._empty_schema()

    def extract_entities(self, text):
        """
        Extracts structured entities (Name, Email, Skills, etc.) from the text.
        """
        system_prompt = (
            "You are an expert Data Extractor. "
            "Your job is to extract factual details from resumes into strict JSON format. "
            "Do not invent information. If a field is missing, return empty strings or empty arrays."
        )

        # Keep prompt size bounded for a 4k context model.
        truncated_text = text[:4000]

        user_prompt = (
            "Analyze the resume text and return exactly one JSON object using this schema:\n"
            "{\n"
            '  "name": "",\n'
            '  "email": "",\n'
            '  "mobile_number": "",\n'
            '  "skills": [],\n'
            '  "company_names": [],\n'
            '  "education": "",\n'
            '  "designation": "",\n'
            '  "total_experience": "",\n'
            '  "ai_summary": "",\n'
            '  "ai_strengths": [],\n'
            '  "experiences": [\n'
            "    {\n"
            '      "designation": "",\n'
            '      "company": "",\n'
            '      "start_date": "",\n'
            '      "end_date": "",\n'
            '      "job_description": ""\n'
            "    }\n"
            "  ]\n"
            "}\n\n"
            "Rules:\n"
            "1. Output valid JSON only. No markdown or extra text.\n"
            "2. skills, company_names, ai_strengths must be arrays of short strings.\n"
            "3. Limit skills to 25 items and company_names to 5 items.\n"
            "4. ai_strengths should contain 3 to 5 items.\n"
            "5. experiences must include only jobs/internships, sorted most recent first, max 8 items.\n"
            "6. Keep each job_description concise and relevant.\n"
            "7. Unknown values must be empty strings or empty arrays.\n"
            "8. Never repeat duplicate array values.\n\n"
            f"Resume Text:\n{truncated_text}"
        )

        response_content = self.inference(
            system_prompt,
            user_prompt,
            max_tokens=self._MAX_MODEL_OUTPUT_TOKENS,
            response_format={"type": "json_object"},
            temperature=0.0,
        )

        if response_content is not None:
            return self._decode_response_json(response_content)
        return self._empty_schema()
