# ================================
# Intelligent Talent Acquisition Assistant
# Resume Parsing Engine
# ================================

import os
import json
from groq import Groq
from pdfminer.high_level import extract_text
from dotenv import load_dotenv
load_dotenv()

# ================================
# GROQ CLIENT INITIALIZATION
# ================================

groq_api_key = os.getenv("GROQ_API_KEY")

if groq_api_key is None:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=groq_api_key)


# ================================
# PDF TEXT EXTRACTION
# ================================

def extract_resume_text(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"PDF Read Error: {e}")
        return ""


# ================================
# LLM STRUCTURED PARSING
# ================================

# def parse_resume_with_llm(resume_text):

#     prompt = f"""
# Extract the following details from this resume and return ONLY valid JSON:

# {{
# "name": "",
# "email": "",
# "phone": "",
# "skills": [],
# "experience": "",
# "education": ""
# }}

# Resume Text:
# {resume_text}
# """

#     response = client.chat.completions.create(
#         model="llama-3.1-8b-instant",
#         messages=[
#             {"role": "system", "content": "You are an AI Resume Parser."},
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0
#     )

#     content = response.choices[0].message.content.strip()

#     # Remove markdown if present
#     content = content.replace("```json", "").replace("```", "").strip()

#     return json.loads(content)

def parse_resume_with_llm(resume_text):

    if len(resume_text.strip()) < 50:
        print("Resume text too small. Skipping...")
        return None

    prompt = f"""
Extract the following details from this resume.

Return STRICTLY valid JSON only.
Do NOT include explanation.
Do NOT include markdown.
Do NOT include ```json

Format:
{{
"name": "",
"email": "",
"phone": "",
"skills": [],
"experience": "",
"education": ""
}}

Resume Text:
{resume_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a Resume Parser. Return ONLY JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown junk
    content = content.replace("```json", "").replace("```", "").strip()

    # 🚨 SAFE JSON PARSING
    try:
        return json.loads(content)

    except json.JSONDecodeError:

        print("❌ JSON Parsing Failed. Raw LLM Output:")
        print(content)

        # Try extracting JSON block manually
        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            json_block = content[start:end]
            return json.loads(json_block)

        except:
            print("⚠️ Resume skipped due to invalid JSON")
            return None


# ================================
# SINGLE RESUME PROCESSOR
# ================================

# def process_resume(pdf_path):

#     text = extract_resume_text(pdf_path)

#     if text.strip() == "":
#         return None

#     parsed_data = parse_resume_with_llm(text)

#     return parsed_data

def process_resume(pdf_path):

    text = extract_resume_text(pdf_path)

    if text.strip() == "":
        print("Empty resume detected. Skipping...")
        return None

    parsed_data = parse_resume_with_llm(text)

    if parsed_data is None:
        print(f"Skipping resume due to parsing error: {pdf_path}")
        return None

    return parsed_data


# ================================
# BATCH PROCESSOR
# ================================

def parse_all_resumes(folder_path):

    results = {}

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(folder_path, file)

            print(f"Processing: {file}")

            try:
                parsed = process_resume(pdf_path)

                if parsed:
                    results[file] = parsed

            except Exception as e:
                print(f"Error in: {file}")
                print(e)

    return results


# ================================
# SAVE TO JSON
# ================================

# def save_to_json(data, output_path):

#     with open(output_path, "w") as f:
#         json.dump(data, f, indent=4)

def save_to_json(new_resume_data, file_name="parsed_resumes.json"):

    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    if os.path.exists(file_name):

        with open(file_name, "r") as f:
            try:
                existing_data = json.load(f)

                # 🔴 If old dict format found → convert to list
                if isinstance(existing_data, dict):
                    existing_data = list(existing_data.values())

            except:
                existing_data = []

    else:
        existing_data = []

    existing_data.append(new_resume_data)

    with open(file_name, "w") as f:
        json.dump(existing_data, f, indent=4)

    print("Resume added successfully ✅")


# ================================
# MAIN RUNNER (CLI USAGE)
# ================================

if __name__ == "__main__":

    folder_path = "resume"
    output_file = "dataset/parsed_resumes.json"

    for file in os.listdir(folder_path):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(folder_path, file)

            print(f"Processing: {file}")

            try:
                parsed = process_resume(pdf_path)

                if parsed:
                    
                    # Add filename reference
                    parsed["source_file"] = file

                    save_to_json(parsed, output_file)

            except Exception as e:
                print(f"Error in: {file}")
                print(e)

    print("\nAll resumes processed successfully!")