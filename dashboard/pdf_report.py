from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def generate_pdf(report, df, filename="Executive_Report.pdf"):

    doc = SimpleDocTemplate(filename)

    story = []

    # Title
    story.append(Paragraph("<b>CustomerPulse AI</b>", styles["Title"]))
    story.append(Paragraph("AI Executive Business Report", styles["Heading1"]))
    story.append(Spacer(1,20))

    # KPIs
    total_reviews = len(df)
    avg_rating = round(df["rating"].mean(),2)

    table_data = [
        ["Metric","Value"],
        ["Total Reviews", total_reviews],
        ["Average Rating", avg_rating],
        ["Products", df["product"].nunique()],
        ["Regions", df["region"].nunique()]
    ]

    table = Table(table_data)

    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.grey),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("BOTTOMPADDING",(0,0),(-1,0),10),
    ]))

    story.append(table)
    story.append(Spacer(1,25))

    story.append(Paragraph("<b>AI Executive Summary</b>",styles["Heading2"]))

    for line in report.split("\n"):

        if line.strip():
            story.append(Paragraph(line,styles["BodyText"]))

    doc.build(story)

    return filename