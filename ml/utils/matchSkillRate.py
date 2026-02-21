from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

vectorizer_a = TfidfVectorizer(lowercase=True, ngram_range=(1,2))
model_b = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def match_skills_train(resume_skills, job_skills):
    resume_text = " ".join(resume_skills)
    job_text = " ".join(job_skills)
    vectorizer_a.fit([resume_text, job_text])

# def match_skills_processing(resume_skills, job_skills):
#     resume_text = " ".join(resume_skills)
#     job_text = " ".join(job_skills)

#     X = vectorizer_a.transform([resume_text, job_text])
#     cos = cosine_similarity(X[0], X[1])[0][0]

#     resume_set = set([s.lower() for s in resume_skills])
#     job_set = set([s.lower() for s in job_skills])

#     overlap = len(resume_set.intersection(job_set)) / max(len(job_set), 1)
#     final = 0.6 * overlap + 0.4 * cos
#     return final * 100

def match_skills_contextual(resume_skills, job_skills):
    scores = []
    for js in job_skills:
        js_emb = model_b.encode(js, convert_to_tensor=True)
        best = 0
        for rs in resume_skills:
            rs_emb = model_b.encode(rs, convert_to_tensor=True)
            sim = float(util.cos_sim(js_emb, rs_emb)[0][0])
            best = max(best, sim)
        scores.append(best)
    return (sum(scores) / len(scores)) * 100

#testing
resume_skills = [
    "Python",
    "Machine Learning",
    "Data Analysis",
    "SQL",
    "TensorFlow",
    "Deep Learning",
    "Pandas",
    "Neural Networks"
]

job_skills = [
    "Python",
    "SQL",
    "Data Engineering",
    "Deep Learning",
    "Machine Learning",
    "Model Deployment"
]

match_skills_train(resume_skills, job_skills)

# print(match_skills_processing(resume_skills, job_skills))
# print(match_skills_contextual(resume_skills, job_skills))