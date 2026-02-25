from agents.matching_agent import matching_agent

resume_sample = {
    "name": "Priya Das",
    "skills": ["Python", "Machine Learning", "SQL"],
    "experience": "2 years"
}

jd_sample = {
    "required_skills": ["Python", "Machine Learning", "React"]
}

result = matching_agent(resume_sample, jd_sample)

print(result)