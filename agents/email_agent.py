from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_email(candidate_data, jd_data, status="shortlisted"):

    if status == "shortlisted":

        prompt = f"""
Write a professional HR email informing the candidate that they have been shortlisted.

Candidate Name: {candidate_data['name']}
Fit Score: {candidate_data['fit_score']}
Matched Skills: {candidate_data['matched_skills']}
Job Role: {jd_data.get('job_role','the applied position')}

Keep it concise and formal.
"""

    else:

        prompt = f"""
Write a professional rejection email.

Candidate Name: {candidate_data['name']}
Job Role: {jd_data.get('job_role','the applied position')}

Keep tone polite and encouraging.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an HR assistant generating recruitment emails."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content