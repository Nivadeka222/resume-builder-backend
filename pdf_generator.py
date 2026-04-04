from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_CENTER


def generate_resume_pdf(data: dict, output_path: str = "resume_output.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.6 * inch,
        leftMargin=0.6 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch
    )

    name_style = ParagraphStyle("Name", fontSize=20, fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
    contact_style = ParagraphStyle("Contact", fontSize=9, fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
    section_style = ParagraphStyle("Section", fontSize=11, fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=2)
    institution_style = ParagraphStyle("Institution", fontSize=10, fontName="Helvetica-Bold", spaceAfter=1)
    degree_style = ParagraphStyle("Degree", fontSize=9, fontName="Helvetica-Oblique", spaceAfter=4)
    normal_style = ParagraphStyle("Normal", fontSize=9, fontName="Helvetica", spaceAfter=2)
    bullet_style = ParagraphStyle("Bullet", fontSize=9, fontName="Helvetica", leftIndent=12, spaceAfter=1, bulletIndent=4, bulletText="•")
    role_style = ParagraphStyle("Role", fontSize=9, fontName="Helvetica-Oblique", spaceAfter=1)
    project_style = ParagraphStyle("Project", fontSize=9, fontName="Helvetica-Bold", spaceAfter=1)
    skill_style = ParagraphStyle("Skill", fontSize=9, fontName="Helvetica", spaceAfter=3)
    cert_style = ParagraphStyle("Cert", fontSize=9, fontName="Helvetica", leftIndent=12, spaceAfter=2, bulletIndent=4, bulletText="•")

    def two_col(left, right, ls, rs):
        t = Table([[Paragraph(left, ls), Paragraph(right, rs)]], colWidths=["70%", "30%"])
        t.setStyle(TableStyle([
            ("ALIGN", (0, 0), (0, 0), "LEFT"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
        return t

    def section(title):
        return [Paragraph(title, section_style), HRFlowable(width="100%", thickness=0.8, color=colors.black, spaceAfter=4)]

    story = []

    # Name
    story.append(Paragraph(data.get("name", ""), name_style))

    # Contact
    parts = []
    if data.get("phone"): parts.append(f"📞 {data['phone']}")
    if data.get("email"): parts.append(f"✉ {data['email']}")
    if data.get("linkedin"): parts.append(f"🔗 {data['linkedin']}")
    if data.get("github"): parts.append(f"💻 {data['github']}")
    story.append(Paragraph("  |  ".join(parts), contact_style))
    story.append(Spacer(1, 6))

    # Education
    if data.get("education"):
        story += section("Education")
        for edu in data["education"]:
            block = [
                two_col(edu.get("institution", ""), edu.get("location", ""), institution_style, institution_style),
                two_col(edu.get("degree", ""), edu.get("dates", ""), degree_style, degree_style),
            ]
            story.append(KeepTogether(block))

    # Experience
    if data.get("experience"):
        story += section("Experience")
        for exp in data["experience"]:
            block = [
                two_col(f"<b>{exp.get('company','')}</b>", exp.get("location", ""), institution_style, normal_style),
                two_col(exp.get("role", ""), exp.get("dates", ""), role_style, role_style),
            ]
            for b in exp.get("bullets", []):
                block.append(Paragraph(b, bullet_style))
            block.append(Spacer(1, 4))
            story.append(KeepTogether(block))

    # Projects
    if data.get("projects"):
        story += section("Projects")
        for proj in data["projects"]:
            title = f"<b>{proj.get('name','')}</b>"
            if proj.get("tech"): title += f" | <i>{proj['tech']}</i>"
            block = [two_col(title, proj.get("dates", ""), project_style, normal_style)]
            for b in proj.get("bullets", []):
                block.append(Paragraph(b, bullet_style))
            block.append(Spacer(1, 4))
            story.append(KeepTogether(block))

    # Skills
    if data.get("skills"):
        story += section("Technical Skills")
        for cat, items in data["skills"].items():
            story.append(Paragraph(f"<b>{cat}:</b> {items}", skill_style))

    # Certifications
    if data.get("certifications"):
        story += section("Certifications")
        for cert in data["certifications"]:
            story.append(Paragraph(cert, cert_style))

    doc.build(story)
    return output_path