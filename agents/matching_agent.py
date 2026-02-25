def matching_agent(resume_data, jd_data):

    resume_skills = set([skill.lower() for skill in resume_data.get("skills", [])])
    jd_skills = set([skill.lower() for skill in jd_data.get("required_skills", [])])

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills

    if len(jd_skills) == 0:
        fit_score = 0
    else:
        fit_score = int((len(matched) / len(jd_skills)) * 100)

    return {
        "name": resume_data.get("name", "Unknown"),
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "fit_score": f"{fit_score}%"
    }