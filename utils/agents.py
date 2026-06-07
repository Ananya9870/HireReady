import streamlit as st
import json
import io
import re
import spacy
import nltk
import textstat
from groq import Groq
from pypdf import PdfReader
from nltk.stem import WordNetLemmatizer
from utils.constants import INDUSTRY_KEYWORDS

@st.cache_resource
def load_resources():
    nltk.download('wordnet', quiet=True)
    try: return spacy.load("en_core_web_md")
    except: return None

nlp = load_resources()
lemmatizer = WordNetLemmatizer()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

class ResumeATS:
    @staticmethod
    def get_readability_score(text):
        return max(0, min(100, textstat.flesch_reading_ease(text)))

    @staticmethod
    def get_semantic_similarity(resume_text, jd_text):
        if not nlp: return 50.0
        doc1 = nlp(" ".join([lemmatizer.lemmatize(w) for w in re.sub(r'[^a-zA-Z\s]', '', resume_text.lower()).split()]))
        doc2 = nlp(" ".join([lemmatizer.lemmatize(w) for w in re.sub(r'[^a-zA-Z\s]', '', jd_text.lower()).split()]))
        return round(doc1.similarity(doc2) * 100, 2)

def extract_text_from_pdf(pdf_bytes):
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        return "".join([p.extract_text() for p in reader.pages if p.extract_text()]).strip()
    except: return "Extraction Error"

def get_ats_analysis(resume_text, job_description):
    sem_score = ResumeATS.get_semantic_similarity(resume_text, job_description)
    readability = ResumeATS.get_readability_score(resume_text)

    prompt = f"""
    You are a Weighted ATS. Give JSON scores based on:
    - Skills (40%), Experience (30%), Keywords (15%), Education (10%), Readability (5%).
    Current Readability: {readability}. Semantic Base: {sem_score}%.
    Industry Keywords: {json.dumps(INDUSTRY_KEYWORDS)}
    
    JSON format:
    {{
        "total_score": 0,
        "category_scores": {{"skills":0, "experience":0, "keywords":0, "education":0, "readability":{readability}}},
        "missing_keywords": {{"technical":[], "tools":[], "soft_skills":[]}},
        "suggestions": []
    }}
    RESUME: {resume_text}
    JD: {job_description}
    """
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content), sem_score

def get_tailored_resume(resume_text, job_description):
    prompt = f"Rewrite this resume professionals using STAR method for this JD. Return ONLY text.\nRESUME: {resume_text}\nJD: {job_description}"
    completion = client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content

# ─────────────────────────────────────────────
# NEW: Skill Extraction from text using INDUSTRY_KEYWORDS
# ─────────────────────────────────────────────
def extract_skills_set(text):
    """Extract skills as a cleaned set from any text by matching against INDUSTRY_KEYWORDS"""
    text_clean = re.sub(r'[^a-zA-Z\s\+\#]', ' ', text.lower())
    tokens = [lemmatizer.lemmatize(w.strip()) for w in text_clean.split() if len(w.strip()) > 1]
    tokens_joined = " ".join(tokens)

    # Build flat set of all known skills from INDUSTRY_KEYWORDS
    all_known_skills = set()
    for category in INDUSTRY_KEYWORDS.values():
        for skill in category:
            all_known_skills.add(skill.lower().strip())

    found = set()
    for skill in all_known_skills:
        # Multi-word skill matching (e.g. "machine learning", "deep learning")
        skill_clean = re.sub(r'[^a-zA-Z\s\+\#]', ' ', skill.lower()).strip()
        skill_tokens = [lemmatizer.lemmatize(t) for t in skill_clean.split() if t]
        if all(t in tokens_joined for t in skill_tokens):
            found.add(skill)

    return found


# ─────────────────────────────────────────────
# NEW: Precision, Recall, F1 Score for Skill Match
# ─────────────────────────────────────────────
def calculate_skill_metrics(resume_text, jd_text):
    """
    Calculate Precision, Recall, F1 Score for skill matching.

    Definitions:
    TP = skills present in BOTH resume and JD  (true matches)
    FP = skills in resume but NOT in JD        (irrelevant/extra skills)
    FN = skills in JD but NOT in resume        (missing skills / gaps)

    Precision = TP / (TP + FP)  → How relevant resume skills are to JD
    Recall    = TP / (TP + FN)  → How many JD skills are covered in resume
    F1 Score  = 2 * P * R / (P + R) → Harmonic mean of Precision & Recall
    """
    resume_skills = extract_skills_set(resume_text)
    jd_skills     = extract_skills_set(jd_text)

    TP = resume_skills & jd_skills      # Intersection — matched skills
    FP = resume_skills - jd_skills      # In resume, not in JD
    FN = jd_skills - resume_skills      # In JD, not in resume

    tp = len(TP)
    fp = len(FP)
    fn = len(FN)

    precision = round(tp / (tp + fp) * 100, 2) if (tp + fp) > 0 else 0.0
    recall    = round(tp / (tp + fn) * 100, 2) if (tp + fn) > 0 else 0.0
    f1        = round(2 * precision * recall / (precision + recall), 2) if (precision + recall) > 0 else 0.0

    return {
        "precision"      : precision,
        "recall"         : recall,
        "f1_score"       : f1,
        "matched_skills" : sorted(TP),
        "missing_skills" : sorted(FN),
        "extra_skills"   : sorted(FP),
        "tp"             : tp,
        "fp"             : fp,
        "fn"             : fn
    }