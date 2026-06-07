# utils/generator.py
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import io

# ─────────────────────────────────────────────
# TEMPLATE 1 — Engineering / Academic Style (Sparky Sundevil Style)
# ─────────────────────────────────────────────
def generate_template1(user_data: dict) -> bytes:
    """Classic 1-page engineering resume style with fixed spacing and alignment"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.45 * inch,
        leftMargin=0.45 * inch,
        topMargin=0.4 * inch,
        bottomMargin=0.4 * inch,
    )
    styles = getSampleStyleSheet()
    story = []

    BLACK = colors.HexColor("#000000")

    # --- Custom Professional Styles ---
    # Fix: Increased spaceAfter to prevent overlap with contact info
    name_style = ParagraphStyle(
        "NameStyle", 
        fontSize=20, 
        fontName="Helvetica-Bold", 
        textColor=BLACK, 
        alignment=TA_CENTER, 
        spaceAfter=12
    )
    
    # Fix: Leading and spacing to ensure clean horizontal alignment
    contact_style = ParagraphStyle(
        "ContactStyle", 
        fontSize=9, 
        fontName="Helvetica", 
        textColor=BLACK, 
        alignment=TA_CENTER, 
        leading=11,
        spaceAfter=8
    )
    
    section_header_style = ParagraphStyle(
        "SectionHeader", 
        fontSize=11, 
        fontName="Helvetica-Bold", 
        textColor=BLACK, 
        spaceBefore=6, 
        spaceAfter=2, 
        textTransform="uppercase"
    )
    
    body_style = ParagraphStyle("BodyStyle", fontSize=9.5, fontName="Helvetica", textColor=BLACK, leading=11)
    bullet_style = ParagraphStyle("BulletStyle", fontSize=9, fontName="Helvetica", textColor=BLACK, leftIndent=12, leading=10, spaceAfter=1)

    def add_section_divider():
        story.append(HRFlowable(width="100%", thickness=1, color=BLACK, spaceAfter=4))

    # --- NAME & CONTACT ---
    story.append(Paragraph(user_data.get("name", "Your Name").upper(), name_style))
    contact_parts = [v for v in [user_data.get("phone"), user_data.get("email"), user_data.get("linkedin"), user_data.get("github")] if v]
    # Using Pipe separator for cleaner horizontal order
    story.append(Paragraph(" | ".join(contact_parts), contact_style))

    # --- SUMMARY ---
    if user_data.get("summary"):
        story.append(Paragraph("SUMMARY", section_header_style))
        add_section_divider()
        story.append(Paragraph(user_data["summary"], body_style))

    # --- EDUCATION ---
    if user_data.get("education"):
        story.append(Paragraph("EDUCATION", section_header_style))
        add_section_divider()
        for edu in user_data["education"]:
            # Table ensures University (Left) and Graduation (Right) alignment
            edu_data = [[
                Paragraph(f"<b>{edu.get('university', '')}</b>", body_style), 
                Paragraph(edu.get("graduation", ""), ParagraphStyle("Right", fontSize=9, alignment=TA_RIGHT))
            ]]
            et = Table(edu_data, colWidths=[5.5*inch, 1.7*inch])
            et.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
            story.append(et)
            story.append(Paragraph(f"{edu.get('degree', '')} | GPA: {edu.get('gpa', '')}", body_style))
            story.append(Spacer(1, 4))

    # --- SKILLS ---
    if user_data.get("skills"):
        story.append(Paragraph("TECHNICAL SKILLS", section_header_style))
        add_section_divider()
        skills = user_data.get("skills", {})
        if isinstance(skills, dict):
            skill_lines = []
            if skills.get('languages'): skill_lines.append(f"<b>Languages:</b> {skills['languages']}")
            if skills.get('tools'): skill_lines.append(f"<b>Tools:</b> {skills['tools']}")
            # Integrated Relevant Coursework Feature
            if skills.get('coursework'): skill_lines.append(f"<b>Relevant Coursework:</b> {skills['coursework']}")
            
            for line in skill_lines:
                story.append(Paragraph(line, body_style))
        else:
            story.append(Paragraph(str(skills), body_style))

    # --- EXPERIENCE ---
    if user_data.get("experience"):
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_header_style))
        add_section_divider()
        for exp in user_data["experience"]:
            exp_data = [[
                Paragraph(f"<b>{exp.get('company', '')}</b>: {exp.get('title', '')}", body_style), 
                Paragraph(exp.get("duration", ""), ParagraphStyle("Right", fontSize=9, alignment=TA_RIGHT))
            ]]
            ext = Table(exp_data, colWidths=[5.5*inch, 1.7*inch])
            ext.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
            story.append(ext)
            for bullet in exp.get("bullets", []):
                if bullet.strip():
                    story.append(Paragraph(f"• {bullet.strip()}", bullet_style))
            story.append(Spacer(1, 4))

    # --- ACADEMIC PROJECTS ---
    if user_data.get("projects"):
        story.append(Paragraph("ACADEMIC PROJECTS", section_header_style))
        add_section_divider()
        for proj in user_data["projects"]:
            if proj.get("title"):
                proj_data = [[
                    Paragraph(f"<b>{proj.get('title', '')}</b>", body_style), 
                    Paragraph(proj.get("duration", ""), ParagraphStyle("Right", fontSize=9, alignment=TA_RIGHT))
                ]]
                pt = Table(proj_data, colWidths=[5.5*inch, 1.7*inch])
                pt.setStyle(TableStyle([('LEFTPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))
                story.append(pt)
                for bullet in proj.get("bullets", []):
                    if bullet.strip():
                        story.append(Paragraph(f"• {bullet.strip()}", bullet_style))
                story.append(Spacer(1, 4))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()

# ─────────────────────────────────────────────
# TEMPLATE 2 — Modern / Creative Style
# ─────────────────────────────────────────────
def generate_template2(user_data: dict) -> bytes:
    """Modern executive style with accent colors"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch
    )
    story = []
    ACCENT = colors.HexColor("#2E4057")
    DARK_GRAY = colors.HexColor("#444444")

    name_style = ParagraphStyle("NameStyle", fontSize=22, fontName="Helvetica-Bold", textColor=ACCENT, spaceAfter=3)
    contact_style = ParagraphStyle("ContactStyle", fontSize=9, fontName="Helvetica", textColor=DARK_GRAY, spaceAfter=8)
    section_header_style = ParagraphStyle("SectionHeader", fontSize=11, fontName="Helvetica-Bold", textColor=ACCENT, spaceBefore=10, spaceAfter=3)
    body_style = ParagraphStyle("BodyStyle", fontSize=9.5, fontName="Helvetica", textColor=DARK_GRAY, leading=14)
    bullet_style = ParagraphStyle("BulletStyle", fontSize=9.5, fontName="Helvetica", textColor=DARK_GRAY, leftIndent=14, leading=12)

    def add_modern_header(title):
        story.append(Paragraph(title.upper(), section_header_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=ACCENT, spaceAfter=4))

    story.append(Paragraph(user_data.get("name", "Your Name"), name_style))
    contact_parts = [v for v in [user_data.get("phone"), user_data.get("email"), user_data.get("linkedin"), user_data.get("github")] if v]
    story.append(Paragraph(" | ".join(contact_parts), contact_style))

    if user_data.get("experience"):
        add_modern_header("Experience")
        for exp in user_data["experience"]:
            story.append(Paragraph(f"<b>{exp.get('company', '')}</b> — {exp.get('duration', '')}", body_style))
            story.append(Paragraph(f"<i>{exp.get('title', '')}</i>", body_style))
            for b in exp.get("bullets", []):
                story.append(Paragraph(f"• {b}", bullet_style))
            story.append(Spacer(1, 5))

    if user_data.get("projects"):
        add_modern_header("Academic Projects")
        for proj in user_data["projects"]:
            story.append(Paragraph(f"<b>{proj.get('title', '')}</b> — {proj.get('duration', '')}", body_style))
            for b in proj.get("bullets", []):
                story.append(Paragraph(f"• {b}", bullet_style))
            story.append(Spacer(1, 5))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()

# ─────────────────────────────────────────────
# MAIN DISPATCHER
# ─────────────────────────────────────────────
def generate_resume(user_data: dict, template: int = 1) -> bytes:
    """Entry point for PDF generation"""
    if template == 1:
        return generate_template1(user_data)
    elif template == 2:
        return generate_template2(user_data)
    else:
        raise ValueError("Template must be 1 or 2")