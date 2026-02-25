import json
from pipeline.batch_pipeline import run_batch_pipeline

with open("dataset/parsed_resumes.json") as f:
    resumes = json.load(f)

jd = {
    "required_skills": ["Python", "Machine Learning"],
    "experience_required": "2 years",
    "job_role": "Data Scientist"
}

result = run_batch_pipeline(resumes, jd)

print(json.dumps(result, indent=4))