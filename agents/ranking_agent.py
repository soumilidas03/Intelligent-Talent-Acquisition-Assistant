# agents/ranking_agent.py

def ranking_agent(matched_candidates):

    # Convert % to int for sorting
    for candidate in matched_candidates:
        candidate['fit_score_int'] = int(candidate['fit_score'].replace('%',''))

    # Sort based on fit_score
    ranked_list = sorted(
        matched_candidates,
        key=lambda x: x['fit_score_int'],
        reverse=True
    )

    # Remove helper field
    for candidate in ranked_list:
        del candidate['fit_score_int']

    return ranked_list