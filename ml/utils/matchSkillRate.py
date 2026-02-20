from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1,2))

def match_skills_train(resume_skills, job_skills):
    resume_text = " ".join(resume_skills)
    job_text = " ".join(job_skills)
    vectorizer.fit([resume_text, job_text])

def match_skills(resume_skills, job_skills):
    resume_text = " ".join(resume_skills)
    job_text = " ".join(job_skills)

    X = vectorizer.transform([resume_text, job_text])
    cos = cosine_similarity(X[0], X[1])[0][0]

    resume_set = set([s.lower() for s in resume_skills])
    job_set = set([s.lower() for s in job_skills])
    overlap = len(resume_set.intersection(job_set)) / max(len(job_set), 1)
    
    final = 0.6 * overlap + 0.4 * cos
    return final * 100

resume_skills = [
    "Python",
    "Machine Learning",
    "Data Analysis",
    "SQL",
    "TensorFlow"
]

job_skills = [
    "Python",
    "SQL",
    "Deep Learning",
    "Machine Learning",
    "Data Engineering"
]

match_skills_train(resume_skills, job_skills)
print(match_skills(resume_skills, job_skills))
