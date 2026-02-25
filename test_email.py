from agents.email_agent import generate_email

candidate = {
    "name": "Priya Das",
    "fit_score": "85%",
    "matched_skills": ["Python", "Machine Learning"],
    "email": "priya@gmail.com"
}

jd = {
    "job_role": "Data Scientist"
}

mail = generate_email(candidate, jd, status="shortlisted")

print(mail)