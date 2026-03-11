import streamlit as st
import tempfile
import json
import pandas as pd

from agents.jd_analyzer import analyze_jd
from agents.resume_parser import process_resume
from pipeline.batch_pipeline import run_batch_pipeline
from pdfminer.high_level import extract_text

from rag.rag_retriever import retrieve_context

st.set_page_config(page_title="AI Talent Acquisition Assistant")

st.title("🤖 Intelligent Talent Acquisition Assistant")

# =========================
# JD INPUT
# =========================


jd_file = st.file_uploader(
    "Upload Job Description (PDF or TXT)",
    type=["pdf","txt"]
)

# =========================
# RESUME UPLOAD
# =========================
uploaded_files = st.file_uploader(
    "Upload Candidate Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)



def extract_jd_text(uploaded_file):

    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/pdf":

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        text = extract_text(tmp_path)
        return text

    return ""

# =========================
# PROCESS BUTTON
# =========================
if st.button("Run AI Hiring Pipeline"):

    if jd_file is None or not uploaded_files:
        st.warning("Please provide JD and upload resumes")
        st.stop()

    # -------------------------
    # 1. JD ANALYSIS
    # -------------------------
    st.subheader("Analyzing Job Description...")
    jd_text = extract_jd_text(jd_file)

    if jd_text.strip() == "":
        st.error("Could not extract text from the uploaded JD file.")
        st.stop()

    st.subheader("📄 Extracted Job Description Preview")
    st.text_area("Extracted JD Preview", jd_text[:800], height=200)

    # jd_data = analyze_jd(jd_text)

    # -------------------------
    # RAG RETRIEVAL
    # -------------------------

    context = ""

    try:
        context = retrieve_context(jd_text)

        if context:
            st.subheader("📚 Retrieved Hiring Knowledge (RAG)")
            st.text_area("Retrieved Context", context, height=200)

    except Exception:
        st.warning("RAG retrieval failed. Proceeding without external knowledge.")

    # -------------------------
    # ENHANCED JD PROMPT
    # -------------------------

    enhanced_jd = f"""
    Use the following hiring knowledge as context to improve job description analysis.

    Context:
    {context}

    Job Description:
    {jd_text}
    """

    # -------------------------
    # JD ANALYSIS
    # -------------------------

    jd_data = analyze_jd(enhanced_jd)

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

    final_output = run_batch_pipeline(parsed_resumes, jd_data,context)

    st.success("Pipeline Completed!")

    # =========================
    # DASHBOARD METRICS
    # =========================
    st.subheader("📊 Hiring Dashboard")

    total_resumes = len(parsed_resumes)
    shortlisted = len(final_output)

    fit_scores = [
        int(c["candidate"]["fit_score"].replace("%", ""))
        for c in final_output
    ]

    avg_score = sum(fit_scores) / len(fit_scores) if fit_scores else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Resumes parsed", total_resumes)
    col2.metric("Shortlisted Candidates", shortlisted)
    col3.metric("Average Fit Score", f"{avg_score:.1f}%")

    # =========================
    # CANDIDATE TABLE
    # =========================
    st.subheader("🏆 Shortlisted Candidates")

    table_data = []

    for result in final_output:

        candidate = result["candidate"]

        table_data.append({
            "Candidate Name": candidate["name"],
            "Fit Score": candidate["fit_score"],
            "Matched Skills": ", ".join(candidate["matched_skills"]),
            "Missing Skills": ", ".join(candidate["missing_skills"])
        })

    df = pd.DataFrame(table_data)

    st.dataframe(df)

    #CANDIDATE FIT SCORE VISUALISATION

    st.subheader("📈 Candidate Fit Score Visualization")

    chart_df = pd.DataFrame({
        "Candidate": [c["candidate"]["name"] for c in final_output],
        "Fit Score": [int(c["candidate"]["fit_score"].replace("%","")) for c in final_output]
    })

    st.bar_chart(chart_df.set_index("Candidate"))

    # =========================
    # EXCEL DOWNLOAD
    # =========================
    excel_file = "shortlisted_candidates.xlsx"

    df.to_excel(excel_file, index=False)

    with open(excel_file, "rb") as f:
        st.download_button(
            label="📥 Download Excel Report",
            data=f,
            file_name="shortlisted_candidates.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    #Email Preview Section
    st.subheader("📧 Generated Candidate Emails")

    for result in final_output:

        with st.expander(f"Email for {result['candidate']['name']}"):
            st.write(result["email"])


    #Show Interview Schedule Table
    schedule_data = []

    for result in final_output:
        if result["interview_schedule"]:
            schedule = result["interview_schedule"]

            schedule_data.append({
                "Candidate": schedule["candidate_name"],
                "Interview Date": schedule["interview_date"],
                "Time Slot": schedule["time_slot"],
                "Mode": schedule["mode"]
            })

    if schedule_data:
        st.subheader("📅 Interview Schedule")
        st.dataframe(pd.DataFrame(schedule_data))

    

    # =========================
    # RAW JSON OUTPUT
    # =========================
    st.subheader("🔎 Full Pipeline Output (JSON)")

    st.json(final_output)

    with open("final_results.json", "w") as f:
        json.dump(final_output, f, indent=4)

    st.download_button(
        label="Download JSON Results",
        data=json.dumps(final_output, indent=4),
        file_name="final_results.json",
        mime="application/json"
    )