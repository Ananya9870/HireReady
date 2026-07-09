# HireReady

An AI-powered resume optimization and interview preparation platform that combines Large Language Models (LLMs), Natural Language Processing (NLP), semantic similarity analysis, and ATS simulation to help candidates improve their resumes, identify skill gaps, prepare for interviews, and generate professional resume templates.

---

## Overview

HireReady automates multiple stages of the recruitment preparation process through an integrated AI workflow:

- Resume Parsing
- ATS Compatibility Analysis
- Semantic Resume–Job Description Matching
- Skill Gap Detection
- Resume Tailoring using LLMs
- AI Interview Coach
- Professional Resume PDF Generation
- Resume & Report Management

The application is built using **Python**, **Streamlit**, **Groq LLMs**, **spaCy**, **SQLAlchemy**, and **ReportLab**.

---

# System Architecture

```
                         User
                           │
            Upload Resume + Job Description
                           │
                           ▼
                     Streamlit UI
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
      ▼                    ▼                    ▼
 ATS Analysis         Interview Coach     Resume Builder
      │                    │                    │
      ▼                    ▼                    ▼
  Groq LLM API       Groq LLM API         ReportLab PDF
      │
      ▼
 SQLite Database (SQLAlchemy ORM)
```

---

# Core Features

## 1. AI-Based ATS Simulation

Evaluates uploaded resumes against a target Job Description using a weighted ATS scoring mechanism.

Evaluation Categories

| Category | Weight |
|----------|--------|
| Skills | 40% |
| Experience | 30% |
| Keywords | 15% |
| Education | 10% |
| Readability | 5% |

Outputs include:

- Overall ATS Score
- Category-wise Breakdown
- Semantic Match Score
- Missing Keywords
- Improvement Suggestions

---

## 2. Semantic Resume Matching

Instead of relying solely on keyword matching, HireReady computes semantic similarity between the resume and Job Description using spaCy word embeddings.

Benefits include:

- Better contextual understanding
- Reduced dependency on exact keywords
- Improved ATS approximation

---

## 3. Skill Gap Analysis

Automatically extracts skills from both:

- Resume
- Job Description

and identifies

- Matched Skills
- Missing Skills
- Additional Skills
- Technical Skill Gaps
- Soft Skill Gaps

---

## 4. Resume Evaluation Metrics

The platform computes Information Retrieval metrics to quantify resume relevance.

### Precision

Percentage of resume skills relevant to the Job Description.

### Recall

Percentage of required Job Description skills covered by the resume.

### F1 Score

Harmonic mean of Precision and Recall.

Additional statistics include:

- True Positives
- False Positives
- False Negatives

---

## 5. AI Resume Tailoring

Generates an optimized resume using Groq-hosted Llama models.

Capabilities include

- STAR-based bullet rewriting
- ATS keyword optimization
- Experience enhancement
- Professional formatting
- Job-specific customization

---

## 6. AI Interview Coach

A context-aware conversational assistant that uses:

- Resume
- Job Description
- Previous Conversation History

to generate personalized interview guidance.

Supports

- Technical Interviews
- Behavioral Interviews
- HR Interviews
- Resume-based Questions
- Follow-up Conversations

---

## 7. Resume Builder

Generate professionally formatted PDF resumes using two templates.

### Engineering Template

- ATS Friendly
- Academic Layout
- One-page Format

### Modern Template

- Executive Design
- Professional Styling
- Recruiter Friendly

---

## 8. Persistent Resume Management

Generated resumes and ATS reports are automatically stored using SQLite.

Supports

- Resume History
- ATS Report History
- Download
- Delete

---

# Technology Stack

## Frontend

- Streamlit

## Backend

- Python 3.11+

## Large Language Models

- Groq API
- Llama-3.1-8B-Instant
- Llama-3.3-70B-Versatile

## Natural Language Processing

- spaCy
- NLTK
- textstat

## Resume Processing

- PyPDF

## Database

- SQLite
- SQLAlchemy ORM

## PDF Generation

- ReportLab

---

# Project Structure

```
HireReady
│
├── db
│   ├── connection.py
│   └── queries.py
│
├── utils
│   ├── agents.py
│   ├── chatbot.py
│   ├── generator.py
│   └── constants.py
│
├── .streamlit
│   ├── style.css
│   └── secrets.toml
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/Ananya9870/HireReady.git
cd HireReady
```

Create a virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Download the spaCy model

```bash
python -m spacy download en_core_web_md
```

Configure Groq API

Create

```
.streamlit/secrets.toml
```

```toml
GROQ_API_KEY="YOUR_API_KEY"
```

Run the application

```bash
streamlit run main.py
```

---

# Workflow

```
Upload Resume
        │
        ▼
Extract Resume Text
        │
        ▼
Paste Job Description
        │
        ▼
ATS Analysis
        │
        ▼
Semantic Matching
        │
        ▼
Skill Gap Detection
        │
        ▼
Resume Tailoring
        │
        ▼
Interview Preparation
        │
        ▼
Resume Generation
```

---

# Database

SQLite is used for persistent storage of

- Generated Resume PDFs
- ATS Reports
- Tailored Resume Outputs

Database operations are implemented using SQLAlchemy ORM.

---

# Future Improvements

- OCR Support for Scanned Resumes
- Cover Letter Generation
- LinkedIn Profile Optimization
- Resume Version Control
- Voice-based Mock Interviews
- Recruiter Dashboard
- Multi-language Resume Analysis
- Cloud Deployment

---

# Author

**Ananya Kriti**

---

## License

This project is intended for educational and research purposes.
