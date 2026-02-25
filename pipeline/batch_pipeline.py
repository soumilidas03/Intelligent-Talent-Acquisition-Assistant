import json
# from agents.matching_agent import match_resume_to_jd
from agents.matching_agent import matching_agent
from agents.email_agent import generate_email
from agents.scheduler_agent import schedule_interview


def run_batch_pipeline(parsed_resumes, jd_data):

    matched_candidates = []

    # STEP 1: MATCH ALL RESUMES
    for resume in parsed_resumes:

        match_result = matching_agent(resume, jd_data)

        candidate_data = {
            "name": resume.get("name"),
            "fit_score": match_result.get("fit_score"),
            "matched_skills": match_result.get("matched_skills"),
            "missing_skills": match_result.get("missing_skills")
        }

        matched_candidates.append(candidate_data)

    # STEP 2: RANK ALL
    ranked = sorted(
        matched_candidates,
        key=lambda x: int(str(x['fit_score']).replace('%','')),
        reverse=True
    )

    # STEP 3: TAKE TOP 3
    # shortlisted = ranked[:3]

    # Filter candidates above threshold (e.g., 50%)
    threshold = 50

    eligible = [
        c for c in ranked
        if int(c['fit_score'].replace('%','')) >= threshold
    ]

    shortlisted = eligible[:3]

    # STEP 4: EMAIL + SCHEDULE
    final_results = []

    for candidate in shortlisted:

        # email = generate_email(candidate, jd_data)
        score = int(candidate['fit_score'].replace('%',''))

        if score >= threshold:
            email = generate_email(candidate, jd_data, status="shortlisted")
        else:
            email = generate_email(candidate, jd_data, status="rejected")
    

        # schedule = schedule_interview(candidate, jd_data)

        if score >= threshold:
            schedule = schedule_interview(candidate, jd_data)
        else:
            schedule = None

        final_results.append({
            "candidate": candidate,
            "email": email,
            "interview_schedule": schedule
        })

    return final_results