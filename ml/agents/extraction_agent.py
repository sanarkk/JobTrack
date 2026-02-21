import json
from typing import Any, Dict
from .base_agent import BaseAgent


class ExtractionAgent(BaseAgent):
    def extract_entities(self, text) :
        """
        Extracts structured entities (Name, Email, Skills, etc.) from the text.
        """
        system_prompt = (
            "You are an expert Data Extractor. "
            "Your job is to extract factual details from resumes into strict JSON format. "
            "Do not invent information. If a field is missing, leave it as null or empty string."
        )
        
        # Balanced truncation for 4k context (4000 chars covers most resumes)
        truncated_text = text[:4000]

        user_prompt = (
            "Analyze the resume text and extract structured information into JSON.\n\n"
            "Fields:\n"
            "- name, email, mobile_number: strings\n"
            "- skills, company_names: comma-separated strings\n"
            "- education, designation, total_experience: strings\n"
            "- ai_summary: 3 sentence professional summary\n"
            "- ai_strengths: list of 3-5 strings\n"
            "- experiences (list of objects):\n"
            "  - designation, company, start_date, end_date: strings\n"
            "  - job_description: bullet points of achievements\n\n"
            "RULES for 'experiences':\n"
            "1. Only include professional roles (Jobs, Internships).\n"
            "2. DO NOT include standalone Projects, Skill headers, or Certifications as a 'job'.\n"
            "3. If a section looks like a Project section, ignore it for the 'experiences' list.\n"
            "4. Capture the full Job Description. Do not summarize it into a single line; include key achievements.\n"
            "5. Sort by date, most recent first.\n\n"
            "Output valid JSON only.\n\n"
            f"Resume Text:\n{truncated_text}"
        )

        response_content = self.inference(
            system_prompt,
            user_prompt,
            max_tokens=5000,
            response_format={"type": "json_object"},
            temperature=0.0,
        )

        if response_content is not None:
            try:
                return json.loads(response_content)
            except json.JSONDecodeError as e:
                print(f"ExtractionAgent: Failed to decode JSON. Error: {e}")
                print(f"RAW CONTENT: {repr(response_content)}")
                return {}
        return {}
