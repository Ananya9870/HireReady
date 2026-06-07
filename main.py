import streamlit as st
import io
import datetime

from db.connection import SessionLocal
from db.queries    import save_resume, delete_resume
from utils.agents  import get_ats_analysis, get_tailored_resume, extract_text_from_pdf, calculate_skill_metrics
from utils.chatbot import get_chatbot_response
from utils.generator import generate_resume

def load_css():
    with open(".streamlit/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def init_session_state():
    defaults = {
        "current_chat": [],
        "current_chat_id": None,
        "chat_sessions": {},   # { id: { "title": str, "messages": [], "timestamp": str } }
        "generated_pdf": None,
        "user_name": "User",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def save_current_chat_to_history():
    """Save current active chat into chat_sessions"""
    msgs = st.session_state.current_chat
    if not msgs:
        return
    cid = st.session_state.current_chat_id
    title = msgs[0]["content"][:40] + "..." if len(msgs[0]["content"]) > 40 else msgs[0]["content"]
    timestamp = datetime.datetime.now().strftime("%d %b, %I:%M %p")
    if cid and cid in st.session_state.chat_sessions:
        # Update existing session
        st.session_state.chat_sessions[cid]["messages"] = msgs
    else:
        # New session
        new_id = f"chat_{len(st.session_state.chat_sessions) + 1}_{datetime.datetime.now().strftime('%H%M%S')}"
        st.session_state.chat_sessions[new_id] = {
            "title": title,
            "messages": msgs,
            "timestamp": timestamp,
        }
        st.session_state.current_chat_id = new_id

def start_new_chat():
    save_current_chat_to_history()
    st.session_state.current_chat = []
    st.session_state.current_chat_id = None
    st.rerun()

def load_chat(cid):
    save_current_chat_to_history()
    st.session_state.current_chat = st.session_state.chat_sessions[cid]["messages"]
    st.session_state.current_chat_id = cid
    st.rerun()

def delete_chat(cid):
    if cid in st.session_state.chat_sessions:
        del st.session_state.chat_sessions[cid]
    if st.session_state.current_chat_id == cid:
        st.session_state.current_chat = []
        st.session_state.current_chat_id = None
    st.rerun()

def render_sidebar(resume_file_holder, job_desc_holder):
    with st.sidebar:
        st.markdown("## 📂 Data Center")
        resume_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
        job_desc = st.text_area("🎯 Target Job Description", height=180)

        st.markdown("---")

        # Header row
        col_h, col_n = st.columns([3, 2])
        col_h.markdown("## 💬 Chats")
        if col_n.button("＋ New", use_container_width=True, key="new_chat_btn"):
            start_new_chat()

        # Chat list — newest first
        sessions = st.session_state.chat_sessions
        if not sessions:
            st.markdown(
                "<p style='color:#555; font-size:0.82rem; padding: 8px 4px;'>No saved chats yet.<br>Start a conversation in Interview Coach.</p>",
                unsafe_allow_html=True
            )
        else:
            for cid, session in reversed(list(sessions.items())):
                is_active = (cid == st.session_state.current_chat_id)

                active_style = "background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.3);" if is_active else "background:#1C1C1C; border:1px solid rgba(255,255,255,0.06);"

                st.markdown(f"""
                    <div style='{active_style} border-radius:8px; padding:10px 12px; margin-bottom:6px;'>
                        <div style='font-size:0.85rem; font-weight:600; color:#F1F1F1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;'>
                            {"🟢 " if is_active else "🗨️ "}{session["title"]}
                        </div>
                        <div style='font-size:0.72rem; color:#555; margin-top:2px;'>{session["timestamp"]}</div>
                    </div>
                """, unsafe_allow_html=True)

                btn_col1, btn_col2 = st.columns([3, 1])
                with btn_col1:
                    if st.button("Open", key=f"open_{cid}", use_container_width=True):
                        load_chat(cid)
                with btn_col2:
                    if st.button("🗑", key=f"del_{cid}", use_container_width=True):
                        delete_chat(cid)

        resume_file_holder.append(resume_file)
        job_desc_holder.append(job_desc)

def main():
    st.set_page_config(page_title="AI Resume Architect", layout="wide", page_icon="🎯")
    load_css()
    init_session_state()

    resume_file_holder = []
    job_desc_holder = []
    render_sidebar(resume_file_holder, job_desc_holder)

    resume_file = resume_file_holder[0] if resume_file_holder else None
    job_desc    = job_desc_holder[0]    if job_desc_holder    else ""

    # --- MAIN PAGE ---
    st.title("🚀 Smart Agentic ATS Resume Architect")
    st.markdown(
        "<p style='color:#6B6B6B; font-size:1rem; margin-top:-8px; margin-bottom:20px;'>"
        "AI-powered resume optimization & interview coaching</p>",
        unsafe_allow_html=True
    )

    tab1, tab2, tab3 = st.tabs(["📊 ATS Analysis", "💬 Interview Coach", "📝 Resume Builder"])

    resume_text = ""
    if resume_file:
        file_bytes = resume_file.getvalue()
        resume_text = extract_text_from_pdf(file_bytes) if resume_file.name.endswith('.pdf') else file_bytes.decode()

    # ─── TAB 1: ATS ANALYSIS ───
    with tab1:
        st.markdown("#### Upload your resume & paste JD in the sidebar, then run analysis.")
        if st.button("🔥 Run ATS Simulation"):
            if not resume_text or not job_desc:
                st.error("⚠️ Please provide both Resume and Job Description.")
            else:
                with st.spinner("🤖 Analyzing your profile..."):
                    analysis, sem_score = get_ats_analysis(resume_text, job_desc)
                    tailored_text = get_tailored_resume(resume_text, job_desc)
                    skill_metrics = calculate_skill_metrics(resume_text, job_desc)

                st.markdown("### 🏆 Overall Score")
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.metric("Total ATS Score", f"{analysis['total_score']}%")
                    st.metric("Semantic Match",  f"{sem_score}%")
                with c2:
                    cats = analysis.get('category_scores', {})
                    cols = st.columns(5)
                    cols[0].metric("🛠 Skills",   f"{cats.get('skills', 0)}%")
                    cols[1].metric("💼 Exp",      f"{cats.get('experience', 0)}%")
                    cols[2].metric("🔑 Keywords", f"{cats.get('keywords', 0)}%")
                    cols[3].metric("🎓 Edu",      f"{cats.get('education', 0)}%")
                    cols[4].metric("📖 Read",     f"{cats.get('readability', 0)}%")

                st.divider()
                st.subheader("🔍 Skill Gap Analysis")
                m_data = analysis.get('missing_keywords', {})
                col_t, col_s = st.columns(2)
                with col_t:
                    st.markdown("#### 💻 Technical Skills")
                    st.write(" • ".join(m_data.get('technical', [])) or "✅ No gaps")
                with col_s:
                    st.markdown("#### 🤝 Soft Skills")
                    st.write(", ".join(m_data.get('soft_skills', [])) or "✅ No gaps")

                st.divider()
                st.subheader("🎯 Skill Match Accuracy — Precision / Recall / F1")
                m1, m2, m3 = st.columns(3)
                m1.metric("Precision", f"{skill_metrics['precision']}%")
                m2.metric("Recall",    f"{skill_metrics['recall']}%")
                m3.metric("F1 Score",  f"{skill_metrics['f1_score']}%")
                st.caption(
                    f"✅ TP (Matched): {skill_metrics['tp']}  |  "
                    f"➕ FP (Extra): {skill_metrics['fp']}  |  "
                    f"❌ FN (Missing): {skill_metrics['fn']}"
                )
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**✅ Matched Skills**")
                    st.write(", ".join(skill_metrics['matched_skills']) or "None found")
                with col_b:
                    st.markdown("**❌ Missing Skills**")
                    st.write(", ".join(skill_metrics['missing_skills']) or "Perfect match! 🎉")
                with st.expander("🔍 Extra Skills in Resume (not in JD)"):
                    st.write(", ".join(skill_metrics['extra_skills']) or "None")

                st.divider()
                st.subheader("📄 Tailored Resume")
                st.text_area("Optimized Content", tailored_text, height=300)
                st.download_button("📥 Download Analysis", tailored_text, "Tailored_Resume.txt")

                # ── Auto-save tailored resume to DB ──
                with SessionLocal() as db:
                    save_resume(db, user_id=None,
                                content=tailored_text.encode("utf-8"),
                                filename=f"ATS_Tailored_{datetime.datetime.now().strftime('%d%b_%H%M')}.txt")

    # ─── TAB 2: INTERVIEW COACH ───
    with tab2:
        st.subheader("🤖 Interview & Career Coach")

        if not resume_text or not job_desc:
            st.warning("⚠️ Please upload a Resume and JD in the Sidebar to begin.")
        else:
            # Active chat indicator
            active_id = st.session_state.current_chat_id
            if active_id and active_id in st.session_state.chat_sessions:
                active_title = st.session_state.chat_sessions[active_id]["title"]
                st.markdown(
                    f"<div style='background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2); "
                    f"border-radius:8px; padding:8px 14px; margin-bottom:12px; font-size:0.85rem; color:#A3A3A3;'>"
                    f"🟢 Active: <span style='color:#34D399; font-weight:600;'>{active_title}</span></div>",
                    unsafe_allow_html=True
                )
            else:
                pass

            # Render messages
            for message in st.session_state.current_chat:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Chat input
            if user_input := st.chat_input("Ask about your interview, skills, or career..."):
                st.session_state.current_chat.append({"role": "user", "content": user_input})
                with st.chat_message("user"):
                    st.markdown(user_input)

                with st.chat_message("assistant"):
                    with st.spinner("Coach is thinking..."):
                        response = get_chatbot_response(
                            st.session_state.current_chat, resume_text, job_desc
                        )
                        st.markdown(response)
                        st.session_state.current_chat.append({"role": "assistant", "content": response})

                # Auto-save after every message
                save_current_chat_to_history()
                st.rerun()

    # ─── TAB 3: RESUME BUILDER ───
    with tab3:
        st.subheader("📝 Professional PDF Resume Generator")
        template_choice = st.radio(
            "Choose Style:",
            ["Engineering/Academic (Template 1)", "Modern/Creative (Template 2)"],
            horizontal=True
        )
        t_idx = 1 if "Engineering" in template_choice else 2
        st.divider()

        with st.form("resume_form"):
            st.markdown("### 👤 Personal Information")
            name = st.text_input("Full Name", value=st.session_state.user_name)
            col1, col2 = st.columns(2)
            email    = col1.text_input("Email")
            phone    = col2.text_input("Phone")
            linkedin = st.text_input("LinkedIn URL")
            github   = st.text_input("GitHub URL")
            summary  = st.text_area("Professional Summary")

            st.markdown("### 🎓 Education")
            edu_uni  = st.text_input("University")
            edu_deg  = st.text_input("Degree")
            edu_grad = st.text_input("Graduation Year")
            edu_gpa  = st.text_input("CGPA")

            st.markdown("### 🛠 Skills")
            sk_col1, sk_col2 = st.columns(2)
            skills_lang   = sk_col1.text_input("Languages (Python, SQL, etc.)")
            skills_tools  = sk_col2.text_input("Tools/Frameworks (React, Docker, etc.)")
            skills_course = st.text_input("Relevant Coursework")

            st.markdown("### 💼 Experience")
            exp_comp = st.text_input("Company Name")
            exp_role = st.text_input("Job Title")
            exp_dur  = st.text_input("Duration")
            exp_desc = st.text_area("Experience Bullets (One per line)")

            st.markdown("### 🚀 Academic Projects")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                p1_title = st.text_input("Project 1 Title")
                p1_dur   = st.text_input("Project 1 Duration")
                p1_desc  = st.text_area("Project 1 Bullets (One per line)")
            with col_p2:
                p2_title = st.text_input("Project 2 Title")
                p2_dur   = st.text_input("Project 2 Duration")
                p2_desc  = st.text_area("Project 2 Bullets (One per line)")

            submit_btn = st.form_submit_button("🔨 Generate PDF Resume")

            if submit_btn:
                user_data = {
                    "name": name, "phone": phone, "email": email,
                    "linkedin": linkedin, "github": github, "summary": summary,
                    "education": [{"degree": edu_deg, "university": edu_uni,
                                   "graduation": edu_grad, "gpa": edu_gpa}],
                    "skills": {"languages": skills_lang, "tools": skills_tools,
                               "coursework": skills_course},
                    "experience": [{"company": exp_comp, "title": exp_role,
                                    "duration": exp_dur, "bullets": exp_desc.split('\n')}],
                    "projects": [
                        {"title": p1_title, "duration": p1_dur, "bullets": p1_desc.split('\n')},
                        {"title": p2_title, "duration": p2_dur, "bullets": p2_desc.split('\n')},
                    ]
                }
                with st.spinner("✨ Generating PDF..."):
                    st.session_state.generated_pdf = generate_resume(user_data, template=t_idx)
                    st.session_state.user_name = name
                    # ── Auto-save PDF to DB ──
                    with SessionLocal() as db:
                        save_resume(db, user_id=None,
                                    content=st.session_state.generated_pdf,
                                    filename=f"{name}_Resume_{datetime.datetime.now().strftime('%d%b_%H%M')}.pdf")

        if st.session_state.generated_pdf:
            st.success(f"✅ Resume for **{st.session_state.user_name}** is ready!")
            st.download_button(
                label="📥 Download Resume PDF",
                data=st.session_state.generated_pdf,
                file_name=f"{st.session_state.user_name}_Resume.pdf",
                mime="application/pdf"
            )

    # ─── DB HISTORY ───
    st.divider()
    st.markdown("## 📜 Saved Reports History")

    db = SessionLocal()
    try:
        items = delete_resume(db, list_only=True)
        if not items:
            st.markdown(
                "<p style='color:#555; font-size:0.85rem;'>No saved reports yet. "
                "Run ATS Analysis or generate a Resume to see records here.</p>",
                unsafe_allow_html=True
            )
        else:
            # Header row
            hdr = st.columns([4, 2, 2, 1])
            hdr[0].markdown("<span style='color:#6B6B6B; font-size:0.75rem; font-weight:700; letter-spacing:1px;'>FILENAME</span>", unsafe_allow_html=True)
            hdr[1].markdown("<span style='color:#6B6B6B; font-size:0.75rem; font-weight:700; letter-spacing:1px;'>TYPE</span>", unsafe_allow_html=True)
            hdr[2].markdown("<span style='color:#6B6B6B; font-size:0.75rem; font-weight:700; letter-spacing:1px;'>DATE</span>", unsafe_allow_html=True)
            hdr[3].markdown("<span style='color:#6B6B6B; font-size:0.75rem; font-weight:700; letter-spacing:1px;'>DEL</span>", unsafe_allow_html=True)
            st.markdown("<hr style='margin:4px 0 8px 0; border-color:rgba(255,255,255,0.06);'>", unsafe_allow_html=True)

            delete_id = None
            for itm in reversed(items):
                is_pdf = itm.filename.endswith(".pdf")
                icon   = "📄" if is_pdf else "📝"
                ftype  = "PDF Resume" if is_pdf else "ATS Analysis"
                fc = st.columns([4, 2, 2, 1])
                fc[0].markdown(f"<span style='font-size:0.88rem;'>{icon} {itm.filename}</span>", unsafe_allow_html=True)
                fc[1].markdown(f"<span style='font-size:0.82rem; color:#A3A3A3;'>{ftype}</span>", unsafe_allow_html=True)
                fc[2].markdown(f"<span style='font-size:0.82rem; color:#A3A3A3;'>{itm.created_at.strftime('%d %b %Y, %H:%M')}</span>", unsafe_allow_html=True)
                if fc[3].button("🗑", key=f"dbdel_{itm.id}"):
                    delete_id = itm.id

            if delete_id:
                delete_resume(db, delete_id)
                db.commit()
                st.rerun()
    finally:
        db.close()

if __name__ == "__main__":
    main()