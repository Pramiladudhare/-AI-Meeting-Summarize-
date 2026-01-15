#
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap


def chunk_text(text: str, max_chars: int = 3000):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + max_chars])
        start += max_chars
    return chunks


def build_markdown(summary_bullets, action_items) -> str:
    md = "## 📝 Meeting Summary\n\n"
    for s in summary_bullets:
        md += f"- {s}\n"

    if action_items:
        md += "\n## ✅ Action Items\n\n"
        for a in action_items:
            md += f"- {a}\n"

    return md


# -------- PDF BUILDER (IMPORTANT PART) --------
def build_pdf(summary_bullets, action_items) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    x = 40
    y = height - 50

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(x, y, "Meeting Summary")
    y -= 25

    pdf.setFont("Helvetica", 10)

    for point in summary_bullets:
        lines = wrap(point, 90)
        for line in lines:
            if y < 40:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = height - 50
            pdf.drawString(x, y, f"- {line}")
            y -= 14
        y -= 4

    if action_items:
        y -= 20
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(x, y, "Action Items")
        y -= 25
        pdf.setFont("Helvetica", 10)

        for item in action_items:
            lines = wrap(item, 90)
            for line in lines:
                if y < 40:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 10)
                    y = height - 50
                pdf.drawString(x, y, f"- {line}")
                y -= 14
            y -= 4

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()
