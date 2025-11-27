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
You are a senior HR recruiter.

Your task is to evaluate how relevant this CV is for the following job description.

### JOB DESCRIPTION
{job_description}

### CANDIDATE CV
{cv_text}

### SCORING GRID (0 to 100)
- 0–30: Very weak match (profile is off-topic or has almost no required skills)
- 31–50: Weak match (some relevant elements but largely insufficient)
- 51–70: Average match (junior or incomplete profile, could fit with training)
- 71–85: Good match (most key requirements are present)
- 86–100: Excellent match (profile is highly aligned with the job)

Give ONLY a single number between 0 and 100 with no extra text.
For example: 42 or 67.5 or 90
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1  # more deterministic, less random
            },
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
