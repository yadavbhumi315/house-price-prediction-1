import pdfplumber

def extract_text_from_pdf(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()

            if content:
                text += content

    return text


def extract_skills(text):
    skills = [
        "python",
        "java",
        "c++",
        "html",
        "css",
        "javascript",
        "sql",
        "react",
        "node",
        "machine learning",
        "data science"
    ]

    text = text.lower()

    found = []

    for skill in skills:
        if skill in text:
            found.append(skill)

    return found