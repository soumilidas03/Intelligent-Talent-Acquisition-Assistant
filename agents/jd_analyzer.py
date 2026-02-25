import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_jd(jd_text):

    prompt = f"""
Extract the following details from this Job Description.
Return ONLY valid JSON.

{{
"required_skills": [],
"experience_required": "",
"education_required": "",
"job_role": ""
}}

Job Description:
{jd_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an AI Job Description Analyzer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    content = content.replace("```json","").replace("```","").strip()

    try:
        return json.loads(content)
    except:
        print("Invalid JSON from LLM:")
        print(content)
        return None