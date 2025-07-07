import streamlit as st
import os
import io
import tempfile
import pandas as pd
import re
import fitz  # PyMuPDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------- Streamlit Page Setup --------------------
st.set_page_config(page_title="Resume Sorter", layout="wide")
st.title("📄 Resume Sorter + JD Matcher")
st.markdown("Upload resumes and a job description. We'll rank candidates based on JD match.")

# -------------------- Upload Section --------------------
jd_file = st.file_uploader("📌 Upload Job Description (Text File)", type=["txt"])
resume_files = st.file_uploader("📁 Upload Resumes (PDF Only)", type=["pdf"], accept_multiple_files=True)

# -------------------- Resume Text Extractor --------------------
def extract_text_from_pdf(file):
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        return ""

# -------------------- Matcher --------------------
def rank_resumes(jd_text, resumes_dict):
    scores = []
    for name, resume_text in resumes_dict.items():
        documents = [jd_text, resume_text]
        tfidf = TfidfVectorizer().fit_transform(documents)
        score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        scores.append((name, round(score * 100, 2)))
    return sorted(scores, key=lambda x: x[1], reverse=True)

# -------------------- Process Button --------------------
if st.button("⚙️ Match Resumes"):
    if not jd_file or not resume_files:
        st.warning("Please upload both Job Description and at least one Resume.")
    else:
        jd_text = jd_file.read().decode("utf-8")
        resumes_dict = {}

        with st.spinner("Processing resumes..."):
            for uploaded_file in resume_files:
                text = extract_text_from_pdf(uploaded_file)
                resumes_dict[uploaded_file.name] = text

        ranked = rank_resumes(jd_text, resumes_dict)
        df = pd.DataFrame(ranked, columns=["Candidate", "Match %"])
        st.success("✅ Matching Complete!")
        st.dataframe(df, use_container_width=True)

        # Optional: Download CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Results as CSV", data=csv, file_name="resume_ranking.csv", mime="text/csv")
