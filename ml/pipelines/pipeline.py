import os
import sys
import re
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_ROOT)

from utils.titleCanonicalConversion import predict_canonical_title
# from utils.matchSkillRate import match_skills_processing
from utils.matchSkillRate import match_skills_contextual

def clean_text(x):
    return re.sub(r"[^a-zA-Z0-9 +]", "", x).strip().lower()

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def resumePipe(path):
    resume = load_json(path)
    title = clean_text(resume["title"])
    skills = [clean_text(s) for s in resume["skills"]]
    canonical_title = predict_canonical_title(title)
    return json.dumps({
        "title": canonical_title,
        "skills": skills
    })

def listingPipe(path):
    listing = load_json(path)
    title = clean_text(listing["title"])
    skills = [clean_text(s) for s in listing["skills"]]

    canonical_title = predict_canonical_title(title)
    return json.dumps({
        "title": canonical_title,
        "skills": skills
    })

def matchingPipe(resume_path, listing_path):
    resume = load_json(resume_path)
    listing = load_json(listing_path)

    resume_title = clean_text(resume["title"])
    listing_title = clean_text(listing["title"])

    resume_skills = [clean_text(s) for s in resume["skills"]]
    listing_skills = [clean_text(s) for s in listing["skills"]]

    canonical_resume_title = predict_canonical_title(resume_title)
    canonical_listing_title = predict_canonical_title(listing_title)

    # match_tfidf = match_skills_processing(resume_skills, listing_skills)
    match_transformers = match_skills_contextual(resume_skills, listing_skills)

    return json.dumps({
        "resume_title": canonical_resume_title,
        "listing_title": canonical_listing_title,
        # "tfidf_score": match_tfidf,
        "transformer_score": match_transformers
    })

# TESTING

if __name__ == "__main__":
    samples_dir = os.path.join(PROJECT_ROOT, "samples")

    files = os.listdir(samples_dir)
    resumes = [f for f in files if f.startswith("resume")]
    postings = [f for f in files if f.startswith("posting")]

    print("resume pipeline testing")
    for r in resumes:
        path = os.path.join(samples_dir, r)
        print(f"\nResume: {r}")
        print(resumePipe(path))

    print("job listring pipeline testing")
    for p in postings:
        path = os.path.join(samples_dir, p)
        print(f"\nPosting: {p}")
        print(listingPipe(path))

    print("skills matching pipeline testing")
    for resume in resumes:
        for posting in postings:
            r_path = os.path.join(samples_dir, resume)
            p_path = os.path.join(samples_dir, posting)
            print(f"\nMatching: {resume}  <->  {posting}")
            print(matchingPipe(r_path, p_path))