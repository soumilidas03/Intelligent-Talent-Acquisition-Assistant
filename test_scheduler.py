from agents.scheduler_agent import schedule_interview

candidate = {
    "name": "Priya Das"
}

jd = {
    "job_role": "Data Scientist"
}

schedule = schedule_interview(candidate, jd)

print(schedule)