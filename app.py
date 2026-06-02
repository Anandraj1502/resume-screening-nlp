import re
from pathlib import Path
from typing import List, Dict

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    import docx2txt
except Exception:
    docx2txt = None


SKILLS = [
    "python", "sql", "excel", "power bi", "tableau", "machine learning", "deep learning",
    "nlp", "pandas", "numpy", "scikit-learn", "statistics", "data visualization",
    "streamlit", "matplotlib", "seaborn", "tensorflow", "pytorch", "flask", "fastapi",
    "aws", "azure", "git", "github", "mysql", "postgresql", "mongodb", "etl",
    "data cleaning", "eda", "dashboard", "business analysis", "a/b testing", "regression",
    "classification", "xgboost", "communication", "problem solving"
]


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_text_from_pdf(file) -> str:
    if pdfplumber is None:
        return "PDF support is not available. Please install pdfplumber or upload TXT/DOCX."
    text_parts = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def extract_text(uploaded_file) -> str:
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix == ".pdf":
        return extract_text_from_pdf(uploaded_file)
    if suffix == ".docx":
        if docx2txt is None:
            return "DOCX support is not available. Please install docx2txt or upload TXT/PDF."
        temp_path = Path("temp_resume.docx")
        temp_path.write_bytes(uploaded_file.getbuffer())
        text = docx2txt.process(str(temp_path))
        temp_path.unlink(missing_ok=True)
        return text
    if suffix == ".txt":
        return uploaded_file.read().decode("utf-8", errors="ignore")
    return "Unsupported file type. Upload PDF, DOCX, or TXT."


def find_skills(text: str) -> List[str]:
    cleaned = clean_text(text)
    found = []
    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, cleaned):
            found.append(skill.title())
    return sorted(set(found))


def calculate_match_score(job_description: str, resume_text: str) -> float:
    documents = [clean_text(job_description), clean_text(resume_text)]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(documents)
    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(score * 100, 2)


def screen_resume(filename: str, resume_text: str, job_description: str) -> Dict:
    jd_skills = set(find_skills(job_description))
    resume_skills = set(find_skills(resume_text))
    matched = sorted(jd_skills.intersection(resume_skills))
    missing = sorted(jd_skills.difference(resume_skills))
    score = calculate_match_score(job_description, resume_text)

    if score >= 75:
        recommendation = "Strong Match"
    elif score >= 50:
        recommendation = "Moderate Match"
    else:
        recommendation = "Needs Improvement"

    return {
        "Resume": filename,
        "Match Score (%)": score,
        "Recommendation": recommendation,
        "Matched Skills": ", ".join(matched) if matched else "None",
        "Missing Skills": ", ".join(missing) if missing else "None",
        "Total Resume Skills Found": len(resume_skills),
    }


st.set_page_config(page_title="AI Resume Screening System", page_icon="📄", layout="wide")

st.title("📄 AI-Based Resume Screening System using NLP")
st.write("Upload resumes, paste a job description, and rank candidates using TF-IDF, cosine similarity, and skill matching.")

with st.sidebar:
    st.header("Project Info")
    st.write("Built with Python, Streamlit, scikit-learn, and NLP text processing.")
    st.write("Best for Data Science / Data Analyst resume portfolio.")

job_description = st.text_area(
    "Paste Job Description",
    height=220,
    placeholder="Paste the job description here... Example: Python, SQL, Power BI, Machine Learning, NLP...",
)

uploaded_files = st.file_uploader(
    "Upload Resume Files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

if st.button("Screen Resumes"):
    if not job_description.strip():
        st.error("Please paste a job description first.")
    elif not uploaded_files:
        st.error("Please upload at least one resume file.")
    else:
        results = []
        extracted_texts = {}
        for file in uploaded_files:
            text = extract_text(file)
            extracted_texts[file.name] = text
            results.append(screen_resume(file.name, text, job_description))

        df = pd.DataFrame(results).sort_values(by="Match Score (%)", ascending=False)

        st.subheader("Candidate Ranking")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Screening Results CSV",
            data=csv,
            file_name="resume_screening_results.csv",
            mime="text/csv",
        )

        st.subheader("Top Candidate Summary")
        top = df.iloc[0]
        col1, col2, col3 = st.columns(3)
        col1.metric("Top Resume", top["Resume"])
        col2.metric("Match Score", f"{top['Match Score (%)']}%")
        col3.metric("Recommendation", top["Recommendation"])

        with st.expander("View Extracted Resume Text"):
            for name, text in extracted_texts.items():
                st.markdown(f"### {name}")
                st.text(text[:3000])
