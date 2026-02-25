from agents.ranking_agent import ranking_agent

mock_match_outputs = [
    {"name": "Rahul", "fit_score": "60%"},
    {"name": "Priya", "fit_score": "85%"},
    {"name": "Siddharth", "fit_score": "75%"}
]

results = ranking_agent(mock_match_outputs)

for i, r in enumerate(results, 1):
    print(f"Rank {i}: {r['name']} - {r['fit_score']}")