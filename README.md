# 🤖 Intelligent Talent Acquisition Assistant

An AI-powered multi-agent hiring automation system that analyzes Job Descriptions, parses resumes, ranks candidates, generates HR emails, and schedules interviews automatically.

Built using Groq LLM (Llama 3.1), Streamlit, and a modular multi-agent architecture.

---

## 🚀 Project Overview

The Intelligent Talent Acquisition Assistant automates the complete hiring pipeline:

1. 📄 Job Description Analysis
2. 📑 Resume Parsing (Batch Processing)
3. 🎯 Skill Matching & Fit Scoring
4. 🏆 Candidate Ranking
5. 📧 Automated Email Generation
6. 📅 AI-based Interview Scheduling

This project simulates a real-world Applicant Tracking System (ATS) powered by Generative AI.

---

## 🧠 System Architecture

<p align="center">
  <img src="./assets/architecture.png" width="500"/>
</p>

---

Each component is designed as an independent agent for modularity and scalability.

---

flowchart TD

A[HR Recruiter] --> B[Streamlit Web Interface]

B --> C[Upload Job Description]
C --> D[JD Text Extraction]

D --> E[RAG Retrieval - ChromaDB Vector Search]
E --> F[Retrieve Hiring Knowledge Base]

F --> G[JD Analyzer Agent - Groq LLM]
G --> H[Structured Job Requirements]

B --> I[Upload Candidate Resumes]

I --> J[Read Resume Bytes]
J --> K[AWS S3 Resume Storage]
K --> L[Resume URL Stored]

J --> M[Resume Parser Agent]
M --> N[Structured Resume Data]

H --> O[Candidate Scoring Agent]
N --> O
F --> O

O --> P[Candidate Ranking]

P --> Q[Shortlisting Logic]
Q --> R[Top Candidates Selected]

R --> S[Email Generation Agent]
R --> T[Interview Scheduler Agent]

S --> U[Generated HR Emails]
T --> V[Interview Schedule JSON]

U --> W[Streamlit Hiring Dashboard]
V --> W
P --> W

W --> X[Analytics + Visualizations]
W --> Y[Excel Report Download]
W --> Z[JSON Results Export]

---

## 🛠️ Tech Stack

- **LLM**: Groq API (Llama-3.1-8b-instant)
- **Frontend**: Streamlit
- **Backend**: Python
- **PDF Parsing**: pdfminer
- **Environment Management**: dotenv
- **JSON Processing**: Native Python JSON
- **Architecture Style**: Multi-Agent Modular Design

---

## Streamlit UI Interface

<p align="center">
  <img src="./assets/ui2.png" width="500"/>
</p>

<p align="center">
  <img src="./assets/ui3.png" width="900"/>
</p><p align="center">
  <img src="./assets/ui4.png" width="900"/>
</p><p align="center">
  <img src="./assets/ui5.png" width="900"/>
</p>

<p align="center">
  <img src="./assets/ui6.png" width="500"/>
</p><p align="center">
  <img src="./assets/ui7.png" width="500"/>
</p><p align="center">
  <img src="./assets/ui8.png" width="500"/>
</p><p align="center">
  <img src="./assets/ui9.png" width="500"/>
</p>
---

👩‍💻 Author

Soumili Das
B.Tech CSE (3rd Year)
AI | MERN | Generative AI

---

📄 License

This project is for educational and demonstration purposes.
