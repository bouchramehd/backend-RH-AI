import requests
from pypdf import PdfReader
import re


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def score_cv_with_ollama(cv_text, job_description):
    prompt = f"""
    You are an HR expert.

    Evaluate how relevant this CV is for the job description.

    Job Description:
    {job_description}

    CV:
    {cv_text}

    Answer with ONLY a number between 0 and 100.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    data = response.json()
    raw = data.get("response", "").strip()

    # Try to find the first number in the response
    match = re.search(r"(\d+(\.\d+)?)", raw)
    if match:
        score = float(match.group(1))
        # clamp between 0 and 100
        score = max(0.0, min(score, 100.0))
    else:
        score = 0.0

    return score
