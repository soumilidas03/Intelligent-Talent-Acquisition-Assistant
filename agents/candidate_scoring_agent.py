def score_and_rank_candidates(parsed_resumes, jd_data, context=None):

    # -------------------------
    # PREPARE JD SKILLS
    # -------------------------

    jd_skills_raw = jd_data.get("required_skills", [])

    if isinstance(jd_skills_raw, str):
        jd_skills = set([jd_skills_raw.lower()])
    else:
        jd_skills = set([skill.lower() for skill in jd_skills_raw])

    scored_candidates = []

    # -------------------------
    # PROCESS EACH RESUME
    # -------------------------

    for resume in parsed_resumes:

        # -------------------------
        # SKILLS NORMALIZATION
        # -------------------------

        resume_skills_raw = resume.get("skills", [])

        if isinstance(resume_skills_raw, str):
            resume_skills = set([resume_skills_raw.lower()])
        else:
            resume_skills = set([skill.lower() for skill in resume_skills_raw])

        # -------------------------
        # EXPERIENCE NORMALIZATION
        # -------------------------

        experience_data = resume.get("experience", "")

        # Normalize experience safely
        if isinstance(experience_data, list):

            cleaned_experience = []

            for item in experience_data:

                if isinstance(item, dict):
                    cleaned_experience.append(" ".join(str(v) for v in item.values()))
                else:
                    cleaned_experience.append(str(item))

            experience_text = " ".join(cleaned_experience).lower()

        else:
            experience_text = str(experience_data).lower()

        # -------------------------
        # SKILL MATCHING
        # -------------------------

        matched = resume_skills.intersection(jd_skills)
        missing = jd_skills - resume_skills

        # -------------------------
        # SKILL MATCH SCORE
        # -------------------------

        if len(jd_skills) == 0:
            skill_score = 0
        else:
            skill_score = int((len(matched) / len(jd_skills)) * 100)

        # -------------------------
        # EXPERIENCE BONUS
        # -------------------------

        experience_bonus = 0

        if context and "experience" in context.lower() and experience_text:
            experience_bonus = 5

        # -------------------------
        # FINAL SCORE
        # -------------------------

        final_score = min(skill_score + experience_bonus, 100)

        # -------------------------
        # BUILD CANDIDATE OBJECT
        # -------------------------

        candidate_data = {
            "name": resume.get("name", "Unknown"),
            "email": resume.get("email", "Not Provided"),
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "fit_score": f"{final_score}%"
        }

        scored_candidates.append(candidate_data)

    # -------------------------
    # RANK CANDIDATES
    # -------------------------

    ranked_candidates = sorted(
        scored_candidates,
        key=lambda x: int(x["fit_score"].replace("%", "")),
        reverse=True
    )

    return ranked_candidates