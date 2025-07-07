from pdfminer.high_level import extract_text
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_pdf_text(path):
    try:
        return extract_text(path)
    except Exception as e:
        print(f"❌ Failed to extract from {path}: {e}")
        return ""

def match_score(jd_text, resume_text):
    try:
        tfidf = TfidfVectorizer()
        vectors = tfidf.fit_transform([jd_text, resume_text])
        return cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    except:
        return 0.0

# Load JD
with open("jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

results = []
resumes_path = "resumes"

for filename in os.listdir(resumes_path):
    if filename.endswith(".pdf"):
        file_path = os.path.join(resumes_path, filename)
        print(f"📄 Processing: {filename}")
        resume_text = extract_pdf_text(file_path)
        score = match_score(jd_text, resume_text)
        results.append({"filename": filename, "score": round(score, 2)})

df = pd.DataFrame(results)
df = df.sort_values(by='score', ascending=False)
df.to_csv("result.csv", index=False)
print("\n✅ All resumes scored! Check 'result.csv'")
