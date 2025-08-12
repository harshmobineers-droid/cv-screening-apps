import streamlit as st
import fitz  # PyMuPDF
import docx
from collections import Counter

# PDF text extraction
def extract_text_from_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# DOCX text extraction
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "
".join([para.text for para in doc.paragraphs])

# Resume scoring
def score_resume(text, keywords):
    words = text.lower().split()
    word_counts = Counter(words)
    score = sum(word_counts.get(keyword.lower(), 0) for keyword in keywords)
    return score

# Streamlit UI
st.title("📄 CV Screening App")
st.write("Upload resumes and a job description to rank candidates based on keyword matches.")

job_description_file = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"])
resume_files = st.file_uploader("Upload Resumes (PDF or DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

if job_description_file and resume_files:
    # Extract job description text
    if job_description_file.name.endswith(".pdf"):
        jd_text = extract_text_from_pdf(job_description_file)
    else:
        jd_text = extract_text_from_docx(job_description_file)

    # Extract keywords from job description
    jd_keywords = list(set(jd_text.lower().split()))
    st.write(f"🔍 Extracted {len(jd_keywords)} keywords from job description.")

    # Score resumes
    results = []
    for resume in resume_files:
        if resume.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume)
        else:
            resume_text = extract_text_from_docx(resume)
        score = score_resume(resume_text, jd_keywords)
        results.append((resume.name, score))

    # Sort and display results
    results.sort(key=lambda x: x[1], reverse=True)
    st.subheader("📊 Resume Rankings")
    for name, score in results:
        st.write(f"{name}: {score} keyword matches")
else:
    st.info("Please upload both job description and resumes to begin screening.")
