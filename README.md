# AI-Based Resume Screening System using NLP

This project screens resumes against a job description using NLP. It extracts resume text, calculates job-resume match score, identifies matched/missing skills, and ranks candidates.

## Features

- Upload PDF, DOCX, or TXT resumes
- Paste any job description
- Calculate match score using TF-IDF + cosine similarity
- Extract matched and missing skills
- Rank multiple resumes
- Download results as CSV
- Streamlit web app interface

## Tech Stack

- Python
- Streamlit
- pandas
- scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity
- pdfplumber
- docx2txt

## Folder Structure

```text
resume-screening-nlp/
├── app.py
├── requirements.txt
├── README.md
├── sample_resumes/
│   ├── data_analyst_resume.txt
│   ├── ml_engineer_resume.txt
│   └── business_analyst_resume.txt
├── data/
│   └── sample_job_description.txt
└── outputs/
```

## How to Run

### 1. Open terminal inside the project folder

```bash
cd resume-screening-nlp
```

### 2. Create virtual environment

For Windows PowerShell:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

For Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in your terminal.

## Sample Job Description

A sample job description is available in:

```text
data/sample_job_description.txt
```

## Sample Resumes

Sample TXT resumes are available in:

```text
sample_resumes/
```

Upload these sample resumes in the app to test the system.

## Resume Bullet Points

You can add this project to your resume:

- Built an AI-based resume screening system using NLP to match resumes with job descriptions.
- Extracted resume text from PDF, DOCX, and TXT files and cleaned unstructured text data using Python.
- Applied TF-IDF vectorization and cosine similarity to calculate candidate-job match scores.
- Developed a Streamlit dashboard to rank candidates, identify matched skills, missing skills, and download screening results.

## Future Improvements

- Add BERT/Sentence Transformers for semantic matching
- Add login system for HR users
- Store results in SQLite or PostgreSQL
- Deploy on Streamlit Cloud
- Add resume parser for name, email, phone, and education extraction
