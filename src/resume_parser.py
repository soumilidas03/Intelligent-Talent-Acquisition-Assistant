import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

    return text


def parse_all_resumes(folder_path):
    resumes = {}

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            full_path = os.path.join(folder_path, file)
            resumes[file] = extract_text_from_pdf(full_path)

    return resumes