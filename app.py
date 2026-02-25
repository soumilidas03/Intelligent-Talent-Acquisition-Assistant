import streamlit as st
import tempfile
import json

from agents.jd_analyzer import analyze_jd
from agents.resume_parser import process_resume
from pipeline.batch_pipeline import run_batch_pipeline


st.set_page_config(page_title="AI Talent Acquisition Assistant")

st.title("🤖 Intelligent Talent Acquisition Assistant")

# =========================
# JD INPUT
# =========================
jd_text = st.text_area("Paste Job Description Here")

# =========================
# RESUME UPLOAD
# =========================
uploaded_files = st.file_uploader(
    "Upload Candidate Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

# =========================
# PROCESS BUTTON
# =========================
if st.button("Run AI Hiring Pipeline"):

    if jd_text == "" or uploaded_files is None:
        st.warning("Please provide JD and upload resumes")
        st.stop()

    # -------------------------
    # 1. JD ANALYSIS
    # -------------------------
    st.subheader("Analyzing Job Description...")
    jd_data = analyze_jd(jd_text)

    if jd_data is None:
        st.error("JD Analysis Failed")
        st.stop()

    st.success("JD Analysis Done")
    st.json(jd_data)

    # -------------------------
    # 2. RESUME PARSING
    # -------------------------
    st.subheader("Parsing Resumes...")

    parsed_resumes = []

    for file in uploaded_files:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        parsed = process_resume(tmp_path)

        if parsed:
            parsed_resumes.append(parsed)

    if len(parsed_resumes) == 0:
        st.error("Resume Parsing Failed")
        st.stop()

    st.success("Resume Parsing Completed")

    # -------------------------
    # 3. BATCH PIPELINE
    # -------------------------
    st.subheader("Running Batch Hiring Pipeline...")

    final_output = run_batch_pipeline(parsed_resumes, jd_data)

    st.success("Pipeline Completed!")

    # -------------------------
    # 4. DISPLAY OUTPUT
    # -------------------------
    st.subheader("Final Shortlisted Candidates")

    st.json(final_output)

    with open("final_results.json","w") as f:
        json.dump(final_output,f,indent=4)

    st.download_button(
        label="Download Results",
        data=json.dumps(final_output,indent=4),
        file_name="final_results.json",
        mime="application/json"
    )