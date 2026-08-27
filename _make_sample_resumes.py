"""Temporary helper: generate a few sample DOCX resumes for testing the match API."""
import os
from pathlib import Path

from docx import Document

OUT = Path(__file__).parent / "resumes"
OUT.mkdir(exist_ok=True)

SAMPLES = [
    {
        "name": "Priya Sharma Resume.docx",
        "body": [
            "Priya Sharma",
            "Email: priya@example.com",
            "Python Developer with 4 years of experience",
            "Bachelor of Technology in Computer Science",
            "Skills: Python, Machine Learning, SQL, AWS, Docker, Flask, Pandas, Numpy",
            "Experience: Worked on ML pipelines at a fintech company for 4 years.",
        ],
    },
    {
        "name": "Rahul Verma Resume.docx",
        "body": [
            "Rahul Verma",
            "Email: rahul@example.com",
            "Full Stack Engineer, 2 years experience",
            "Master of Science in Information Systems",
            "Skills: JavaScript, React, Node.js, Django, SQL, MongoDB, Git",
            "Experience: Built web applications at a startup for 2 years.",
        ],
    },
    {
        "name": "Sneha Patel Resume.docx",
        "body": [
            "Sneha Patel",
            "Email: sneha@example.com",
            "Fresher, Data Science graduate",
            "Master of Science in Data Science",
            "Skills: Python, Numpy, Pandas, Matplotlib, SQL, Machine Learning, TensorFlow",
            "Experience: University projects and internship in data analysis.",
        ],
    },
]

for item in SAMPLES:
    fname = item["name"]
    lines = item["body"]
    doc = Document()
    for line in lines:
        doc.add_paragraph(line)
    doc.save(OUT / fname)
    print("wrote", OUT / fname)

print("done")
