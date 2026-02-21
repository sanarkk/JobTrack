from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util
import numpy as np

vectorizer_a = TfidfVectorizer(lowercase=True, ngram_range=(1, 2))
model_b = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cuda")

def match_skills_train(resume_skills, job_skills):
    corpus = [" ".join(resume_skills), " ".join(job_skills)]
    vectorizer_a.fit(corpus)

# def match_skills_processing(resume_skills, job_skills):
#     resume_text = " ".join(resume_skills)
#     job_text = " ".join(job_skills)

#     X = vectorizer_a.transform([resume_text, job_text]).toarray()
#     cos = float(np.dot(X[0], X[1]) / (np.linalg.norm(X[0]) * np.linalg.norm(X[1]) + 1e-9))

#     resume_set = set(s.lower() for s in resume_skills)
#     job_set = set(s.lower() for s in job_skills)
#     overlap = len(resume_set & job_set) / max(len(job_set), 1)

#     final = 0.6 * overlap + 0.4 * cos
#     return final * 100

def match_skills_contextual(resume_skills, job_skills):
    resume_emb = model_b.encode(resume_skills, convert_to_tensor=True)
    job_emb = model_b.encode(job_skills, convert_to_tensor=True)

    sim_matrix = util.cos_sim(job_emb, resume_emb)
    best_per_job_skill = sim_matrix.max(dim=1).values

    return float(best_per_job_skill.mean().item() * 100)

#testing
# resume_skills = [
#     "Python",
#     "Machine Learning",
#     "Data Analysis",
#     "SQL",
#     "TensorFlow",
#     "Deep Learning",
#     "Pandas",
#     "Neural Networks"
# ]

# job_skills = [
#     "Python",
#     "SQL",
#     "Data Engineering",
#     "Deep Learning",
#     "Machine Learning",
#     "Model Deployment"
# ]

# match_skills_train(resume_skills, job_skills)

# print(match_skills_processing(resume_skills, job_skills))
# print(match_skills_contextual(resume_skills, job_skills))