# 🚀 HireReady – AI-Powered ATS Resume Architect & Interview Coach

HireReady is an AI-powered career assistant that helps job seekers optimize their resumes, analyze ATS compatibility, prepare for interviews, and generate professional resumes—all from a single platform.

The application combines Large Language Models (LLMs), Natural Language Processing (NLP), ATS simulation, and PDF generation to provide an end-to-end job application experience.

---

# ✨ Features

## 📊 AI ATS Resume Analysis
- Upload Resume (PDF/TXT)
- Paste Job Description
- AI-powered ATS Simulation
- Weighted ATS Score
- Semantic Similarity Score
- Readability Analysis
- Skills Matching
- Experience Evaluation
- Education Evaluation
- Keyword Analysis

---

## 🎯 Skill Gap Analysis

Automatically detects:

- Missing Technical Skills
- Missing Soft Skills
- Missing Tools & Technologies
- Extra Skills in Resume
- Matched Skills

---

## 📈 Precision • Recall • F1 Score

Calculates resume quality using Information Retrieval metrics.

- Precision
- Recall
- F1 Score
- True Positives (Matched Skills)
- False Positives (Extra Skills)
- False Negatives (Missing Skills)

---

## 🧠 Semantic Resume Matching

Uses spaCy NLP embeddings to compare the semantic meaning of:

- Resume
- Job Description

instead of relying only on keyword matching.

---

## 📖 Resume Readability Analysis

Calculates readability using the Flesch Reading Ease Score to determine how ATS-friendly and recruiter-friendly the resume is.

---

## 🤖 AI Resume Tailoring

Uses Groq Llama models to:

- Rewrite Resume
- Improve Bullet Points
- Apply STAR Method
- Match Resume to Job Description
- Optimize ATS Keywords

---

## 💬 AI Interview Coach

Interactive interview preparation chatbot.

Supports:

- Technical Interview Questions
- HR Interview Questions
- Behavioral Questions
- Resume-based Questions
- JD-based Questions
- Follow-up Conversations
- Context-aware Memory

---

## 💾 Chat History

- Save conversations
- Load previous chats
- Delete chats
- Multiple chat sessions

---

## 📝 Resume Builder

Professional Resume Generator with multiple templates.

Supports:

### Template 1
- Engineering Resume
- Academic Resume
- ATS Friendly

### Template 2
- Modern Resume
- Executive Style
- Creative Design

---

## 📄 PDF Resume Generator

Generate downloadable professional PDF resumes with:

- Personal Information
- Education
- Skills
- Experience
- Projects
- Coursework
- Contact Details

---

## 📚 Resume Database

Automatically stores generated reports.

Supports:

- ATS Reports
- Tailored Resumes
- Generated PDFs
- Report History
- Delete Reports

---

## 🎨 Modern UI

Built using Streamlit with:

- Responsive Layout
- Sidebar Navigation
- Tabs
- Chat Interface
- Custom CSS
- Interactive Metrics
- Download Buttons

---

# 🛠️ Tech Stack

## Programming Language

- Python 3.11+

---

## Frontend

- Streamlit

---

## AI & LLM

- Groq API
- Llama 3.1 8B Instant
- Llama 3.3 70B Versatile

---

## NLP

- spaCy
- NLTK
- textstat

---

## PDF Processing

- PyPDF

---

## Database

- SQLite
- SQLAlchemy ORM

---

## PDF Generation

- ReportLab

---

## Other Libraries

- JSON
- io
- datetime
- Regular Expressions (re)

---

# 📂 Project Structure

```
HireReady/
│
├── main.py
│
├── db/
│   ├── connection.py
│   └── queries.py
│
├── utils/
│   ├── agents.py
│   ├── chatbot.py
│   ├── generator.py
│   └── constants.py
│
├── .streamlit/
│   ├── config.toml
│   └── style.css
│
├── requirements.txt
├── README.md
└── .env
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Ananya9870/HireReady.git
```

```bash
cd HireReady
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Download spaCy Model

```bash
python -m spacy download en_core_web_md
```

---

## Configure Environment

Create a `.streamlit/secrets.toml` file:

```toml
GROQ_API_KEY="your_groq_api_key"
```

---

# ▶️ Run Project

```bash
streamlit run main.py
```

---

# 📌 Workflow

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
Skill Gap Detection
        │
        ▼
Precision / Recall / F1
        │
        ▼
Tailored Resume
        │
        ▼
Interview Coach
        │
        ▼
Resume Builder
        │
        ▼
Generate Professional PDF
```

---

# 📊 ATS Scoring Parameters

The ATS engine evaluates resumes using weighted scoring:

| Category | Weight |
|----------|--------|
| Skills | 40% |
| Experience | 30% |
| Keywords | 15% |
| Education | 10% |
| Readability | 5% |

---

# 📈 Skill Matching Metrics

The project computes:

- Precision
- Recall
- F1 Score
- Matched Skills
- Missing Skills
- Extra Skills

---

# 💡 Key Highlights

- AI-Powered ATS Simulation
- Resume Tailoring using LLMs
- Semantic Resume Matching
- Skill Gap Analysis
- Precision / Recall / F1 Metrics
- Context-Aware Interview Coach
- Professional Resume Generator
- PDF Export
- Chat History
- SQLite Database Integration
- Responsive Streamlit UI

---

# 🔮 Future Improvements

- Multi-language Resume Support
- OCR for Scanned PDFs
- Cover Letter Generator
- LinkedIn Profile Analyzer
- Resume Version Management
- Interview Voice Mode
- AI Mock Interview Evaluation
- Resume Ranking Against Multiple JDs
- Recruiter Dashboard
- Cloud Deployment

---

# 👩‍💻 Author

**Ananya Kriti**
- AI/ML Developer

---

# ⭐ If you found this project useful, don't forget to star the repository!
