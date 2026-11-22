"""
MediScan AI - PDF Summary Report Generator
Generates a downloadable PDF document summarizing the medical document classification,
extracted text summary, confidence scores, and safety disclaimers using ReportLab.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_report_pdf(report_data: dict, user_name: str) -> io.BytesIO:
    """Generate a formatted PDF report stream."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0f172a')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748b')
    )
    section_style = ParagraphStyle(
        'DocSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#0369a1'),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )
    code_style = ParagraphStyle(
        'DocCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )
    disclaimer_style = ParagraphStyle(
        'DisclaimerText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#991b1b')
    )

    # Header
    header_data = [
        [
            Paragraph("<b>MediScan AI</b>", title_style),
            Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>User: {user_name}", subtitle_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[320, 210])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=14))

    # Document Overview Table
    uploaded_at = report_data.get('uploaded_at')
    if isinstance(uploaded_at, datetime):
        uploaded_str = uploaded_at.strftime('%B %d, %Y - %I:%M %p')
    else:
        uploaded_str = str(uploaded_at or 'N/A')

    confidence = report_data.get('confidence_score', 0.0)
    confidence_pct = f"{confidence * 100:.1f}%"

    meta_data = [
        [Paragraph("<b>Report ID:</b>", body_style), Paragraph(f"#{report_data.get('id', 'N/A')}", body_style),
         Paragraph("<b>Uploaded Date:</b>", body_style), Paragraph(uploaded_str, body_style)],
        [Paragraph("<b>File Name:</b>", body_style), Paragraph(str(report_data.get('filename', 'N/A')), body_style),
         Paragraph("<b>Processing Status:</b>", body_style), Paragraph(str(report_data.get('processing_status', 'Completed')).upper(), body_style)],
        [Paragraph("<b>Classification:</b>", body_style), Paragraph(f"<b><font color='#0369a1' size=11>{report_data.get('predicted_category', 'Unclassified')}</font></b>", body_style),
         Paragraph("<b>Model Confidence:</b>", body_style), Paragraph(f"<b><font color='#16a34a' size=11>{confidence_pct}</font></b>", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[95, 170, 105, 160])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # Extracted Text Section
    story.append(Paragraph("Extracted Document Content Preview", section_style))
    extracted = report_data.get('extracted_text', '') or 'No text content available.'
    # Truncate preview if very long to prevent overflow
    preview_text = extracted[:1800] + ('...' if len(extracted) > 1800 else '')
    # Clean text for XML/Paragraph
    safe_preview = preview_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br/>')

    text_table = Table([[Paragraph(safe_preview, code_style)]], colWidths=[530])
    text_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(text_table)
    story.append(Spacer(1, 16))

    # Medical Disclaimer Callout Box
    disclaimer_html = (
        "<b>IMPORTANT NOTICE & MEDICAL DISCLAIMER:</b><br/>"
        "MediScan AI is an artificial intelligence-powered document classification and categorization tool. "
        "The predicted category and extracted information are for record organization, indexing, and workflow routing only. "
        "This software DOES NOT evaluate clinical conditions, offer medical diagnosis, provide clinical prognosis, "
        "or replace the professional consultation, judgment, and care of a licensed healthcare practitioner."
    )
    disclaimer_table = Table([[Paragraph(disclaimer_html, disclaimer_style)]], colWidths=[530])
    disclaimer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef2f2')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#f87171')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(disclaimer_table)

    # Build document
    doc.build(story)
    buffer.seek(0)
    return buffer
