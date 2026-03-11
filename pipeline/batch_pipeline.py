



from agents.candidate_scoring_agent import score_and_rank_candidates
from agents.email_agent import generate_email
from agents.scheduler_agent import schedule_interview


def run_batch_pipeline(parsed_resumes, jd_data, context):

    # STEP 1: SCORE + RANK ALL CANDIDATES
    ranked = score_and_rank_candidates(parsed_resumes, jd_data, context)

    # STEP 2: SHORTLIST BASED ON SCORE
    threshold = 50

    eligible = [
        c for c in ranked
        if int(c["fit_score"][:-1]) >= threshold
    ]

    shortlisted = eligible[:]

    # STEP 3: EMAIL + SCHEDULING
    final_results = []

    for candidate in shortlisted:

        score = int(candidate["fit_score"][:-1])

        if score >= threshold:
            email = generate_email(candidate, jd_data, context, status="shortlisted")
            schedule = schedule_interview(candidate, jd_data, context)
        else:
            email = generate_email(candidate, jd_data, context, status="rejected")
            schedule = None

        final_results.append({
            "candidate": candidate,
            "email": email,
            "interview_schedule": schedule
        })

    return final_results