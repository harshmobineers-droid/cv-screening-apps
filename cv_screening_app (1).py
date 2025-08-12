
import streamlit as st
import fitz  # PyMuPDF
import docx
from collections import Counter

# PDF text extraction
def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# DOCX text extraction
def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

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
        job_text = extract_text_from_pdf(job_description_file)
    else:
        job_text = extract_text_from_docx(job_description_file)

    # Extract keywords from job description
    job_keywords = job_text.lower().split()
    job_keywords = [word for word in job_keywords if len(word) > 3]  # Filter short words

    # Score resumes
    resume_scores = []
    for resume_file in resume_files:
        if resume_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_file)
        else:
            resume_text = extract_text_from_docx(resume_file)

        score = score_resume(resume_text, job_keywords)
        resume_scores.append((resume_file.name, score))

    # Sort and display results
    resume_scores.sort(key=lambda x: x[1], reverse=True)
    st.subheader("📊 Resume Rankings")
    for name, score in resume_scores:
        st.write(f"{name}: {score}")
else:
    st.info("Please upload both job description and resumes to begin screening.")
