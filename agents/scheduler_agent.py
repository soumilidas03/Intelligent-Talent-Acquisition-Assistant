from groq import Groq
from datetime import datetime
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def schedule_interview(candidate_data, jd_data):

    today = datetime.today().strftime("%Y-%m-%d")

    prompt = f"""
Schedule an interview for the following shortlisted candidate.

Today's date: {today}
The interview must be within 5 days from this date.

Candidate Name: {candidate_data['name']}
Job Role: {jd_data.get('job_role','the applied role')}

Generate:
- Interview Date (YYYY-MM-DD format)
- Time Slot
- Mode (Online/Offline)
- Meeting Link (if online)
- HR Contact Person

Return ONLY valid JSON in this format:

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
            {"role": "system", "content": "You are an HR Interview Scheduler. Always return clean JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()
    content = content.replace("```json","").replace("```","").strip()

    try:
        return json.loads(content)
    except:
        print("Invalid JSON from Scheduler:")
        print(content)
        return None