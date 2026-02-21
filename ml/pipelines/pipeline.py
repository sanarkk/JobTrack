# import os
# import sys
# import re
# import json

# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
# sys.path.insert(0, PROJECT_ROOT)

# from utils.titleCanonicalConversion import predict_canonical_title
# from utils.matchSkillRate import match_skills_contextual

# def clean_text(x):
#     return re.sub(r"[^a-zA-Z0-9 +]", "", x).strip().lower()

# def resumePipe(resume_dict):
#     title = clean_text(resume_dict.get("designation", "") or "")
#     skills = [clean_text(s) for s in resume_dict.get("skills", [])]
#     canonical_title = predict_canonical_title(title)
#     return {
#         "title": canonical_title,
#         "skills": skills
#     }


# def listingPipe(data):
#     title = clean_text(data["title"])
#     skills = [clean_text(s) for s in data["skills"]]
#     canonical_title = predict_canonical_title(title)
#     return {
#         "title": canonical_title,
#         "skills": skills
#     }

# def matchingPipe(resume_dict, listing_dict):
#     resume_title = clean_text(resume_dict["title"])
#     listing_title = clean_text(listing_dict["title"])

#     resume_skills = [clean_text(s) for s in resume_dict["skills"]]
#     listing_skills = [clean_text(s) for s in listing_dict["skills"]]

#     canonical_resume_title = predict_canonical_title(resume_title)
#     canonical_listing_title = predict_canonical_title(listing_title)

#     match_score = match_skills_contextual(resume_skills, listing_skills)

#     return {
#         "resume_title": canonical_resume_title,
#         "listing_title": canonical_listing_title,
#         "matching_score": match_score
#     }

import re
from utils.matchSkillRate import match_skills_contextual

def clean_text(x):
    return re.sub(r"[^a-zA-Z0-9 +]", "", x).strip().lower()

def resumePipe(resume_dict):
    skills = [clean_text(s) for s in resume_dict.get("skills", [])]
    return {
        "skills": skills
    }

def listingPipe(data):
    skills = [clean_text(s) for s in data["skills"]]
    return {
        "skills": skills
    }

def matchingPipe(resume_dict, listing_dict):
    resume_skills = resume_dict["skills"]
    listing_skills = listing_dict["skills"]
    score = match_skills_contextual(resume_skills, listing_skills)
    return {
        "matching_score": score
    }