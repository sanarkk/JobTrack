CANONICAL_TITLES = [
    # Technology
    "Software Engineer",
    "Data Scientist",
    "AI Engineer",
    "Cybersecurity Specialist",
    "Cloud Architect",

    # Engineering
    "Mechanical Engineer",
    "Electrical Engineer",
    "Civil Engineer",
    "Chemical Engineer",
    "Aerospace Engineer",

    # Business
    "Project Manager",
    "Business Analyst",
    "Operations Manager",
    "Marketing Manager",
    "Sales Manager",

    # Finance and Accounting
    "Financial Analyst",
    "Accountant",
    "Risk Manager",

    # Healthcare
    "Registered Nurse",
    "Physician",
    "Pharmacist",

    # Education
    "Teacher",
    "Instructional Designer",

    # Creative and Media
    "Graphic Designer",
    "Content Strategist"
]

import os
import pandas as pd
import joblib
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODEL_DIR, "svm_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

def train_job_title_model(csv_path):
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = pd.read_csv(csv_path)

    # conversion to vectors
    vectorizer = TfidfVectorizer(lowercase=True, ngram_range=(1,2))
    X = vectorizer.fit_transform(df["job_title"])
    y = df["canonical_title"]

    # supoort vector machine model
    clf = LinearSVC()
    clf.fit(X, y)

    joblib.dump(clf, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print("\n - training complete!")

def predict_canonical_title(to_check_title):
    clf = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    X = vectorizer.transform([to_check_title])
    return clf.predict(X)[0]

# training
csv_path = "../datasets/job_title_canonical_dataset.csv"
# train_job_title_model(csv_path=csv_path)

# testing
TEST_TITLES = [
    "Senior Data Eng.",
    "AI Dev",
    "Mechanical Eng Specialist",
    "RN Nurse",
    "Cloud Solutions Architect",
    "Junior Accountant",
    "Marketing Lead",
    "Software Dev Intern",
    "Electrical Eng Technician",
    "Content Creator Strategist"
]

for title in TEST_TITLES:
    predicted_title = predict_canonical_title(title)
    print("\nActual: ", title)
    print("Predicted: ", predicted_title)