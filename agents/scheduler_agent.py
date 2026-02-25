from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def schedule_interview(candidate_data, jd_data):

    prompt = f"""
Schedule an interview for the following shortlisted candidate.

Candidate Name: {candidate_data['name']}
Job Role: {jd_data.get('job_role','the applied role')}

Generate:
- Interview Date (within next 5 days)
- Time Slot
- Mode (Online/Offline)
- Meeting Link (if online)
- HR Contact Person

Return ONLY valid JSON:

{{
 "candidate_name":"",
 "interview_date":"",
 "time_slot":"",
 "mode":"",
 "meeting_link":"",
 "hr_contact":""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an HR Interview Scheduler."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()

    content = content.replace("```json","").replace("```","").strip()

    return json.loads(content)