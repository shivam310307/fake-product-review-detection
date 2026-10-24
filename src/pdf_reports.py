"""
Academic PDF Report Generation Module (ReportLab)
=================================================
Generates audit-ready, high-resolution downloadable PDF reports:
1. Individual Review Prediction Report
2. Model Performance & Evaluation Benchmark Report
3. Product URL Batch Analysis Report
4. Dataset Summary & Preprocessing Audit Report
"""

import os
import json
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.pdfgen import canvas

from src.visualization import generate_matplotlib_charts

class NumberedCanvas(canvas.Canvas):
    """Adds running headers and footers with page numbering."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(HexColor("#64748b"))
        
        # Header line & label
        self.drawString(54, 750, "ReviewGuard AI — Advanced Machine Learning Fake Review Detection System")
        self.setStrokeColor(HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)
        
        # Footer line & page number
        self.line(54, 45, 558, 45)
        self.drawString(54, 32, "Confidential Academic Audit Report • Developed for Teacher & Viva Evaluation")
        self.drawRightString(558, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def _get_report_styles():
    """Returns standardized academic typography styles."""
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=HexColor("#0f172a"), spaceAfter=4))
    styles.add(ParagraphStyle('DocSubtitle', fontName='Helvetica', fontSize=10.5, leading=14, textColor=HexColor("#475569"), spaceAfter=14))
    styles.add(ParagraphStyle('SectionHead', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=HexColor("#0284c7"), spaceBefore=10, spaceAfter=6))
    styles.add(ParagraphStyle('BodyTextDark', fontName='Helvetica', fontSize=9, leading=13, textColor=HexColor("#1e293b")))
    styles.add(ParagraphStyle('BodyTextMuted', fontName='Helvetica', fontSize=8, leading=11, textColor=HexColor("#64748b")))
    styles.add(ParagraphStyle('TableHead', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=HexColor("#ffffff")))
    styles.add(ParagraphStyle('DisclaimerBox', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=HexColor("#475569")))
    return styles

def generate_prediction_pdf(pred_data: dict, output_path: str):
    """Generates single review prediction report."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = _get_report_styles()
    story = []
    
    # Title
    story.append(Paragraph("ReviewGuard AI: Individual Review Analysis Report", styles['DocTitle']))
    story.append(Paragraph(f"Generated on {time.strftime('%B %d, %Y at %H:%M:%S')} • Model: {pred_data.get('model_used')}", styles['DocSubtitle']))
    
    # Overview Table
    is_fake = pred_data.get('prediction_binary') == 1
    badge_bg = "#f43f5e" if is_fake else "#10b981"
    
    overview_data = [
        [Paragraph("<b>Evaluation Parameter</b>", styles['TableHead']), Paragraph("<b>Value / System Assessment</b>", styles['TableHead'])],
        [Paragraph("<b>Prediction Classification</b>", styles['BodyTextDark']), Paragraph(f"<b><font color='{badge_bg}'>{pred_data.get('prediction_label')}</font></b>", styles['BodyTextDark'])],
        [Paragraph("<b>Model Confidence</b>", styles['BodyTextDark']), Paragraph(f"{pred_data.get('confidence_percentage')}%", styles['BodyTextDark'])],
        [Paragraph("<b>Class Probabilities</b>", styles['BodyTextDark']), Paragraph(f"Genuine: {pred_data.get('probability_genuine')}%  |  Fake: {pred_data.get('probability_fake')}%", styles['BodyTextDark'])],
        [Paragraph("<b>Selected Algorithm</b>", styles['BodyTextDark']), Paragraph(str(pred_data.get('model_used')), styles['BodyTextDark'])],
        [Paragraph("<b>Text Character Count</b>", styles['BodyTextDark']), Paragraph(str(pred_data.get('stats', {}).get('text_length', len(str(pred_data.get('raw_text', ''))))), styles['BodyTextDark'])],
        [Paragraph("<b>Word Count</b>", styles['BodyTextDark']), Paragraph(str(pred_data.get('stats', {}).get('word_count', len(str(pred_data.get('raw_text', '')).split()))), styles['BodyTextDark'])],
        [Paragraph("<b>Vocabulary Richness</b>", styles['BodyTextDark']), Paragraph(str(pred_data.get('stats', {}).get('vocabulary_richness', 'N/A')), styles['BodyTextDark'])],
        [Paragraph("<b>Estimated Sentences</b>", styles['BodyTextDark']), Paragraph(str(pred_data.get('stats', {}).get('sentence_count', 1)), styles['BodyTextDark'])]
    ]

    if pred_data.get('decoupling'):
        dec = pred_data['decoupling']
        overview_data.insert(2, [
            Paragraph("<b>Marketplace Scenario</b>", styles['BodyTextDark']), 
            Paragraph(f"<b>{dec.get('scenario_title', 'Decoupled Evaluation')}</b>", styles['BodyTextDark'])
        ])
        overview_data.insert(3, [
            Paragraph("<b>Reviewer Sentiment</b>", styles['BodyTextDark']), 
            Paragraph(f"{dec.get('sentiment', 'Neutral')}", styles['BodyTextDark'])
        ])

    t_over = Table(overview_data, colWidths=[200, 304])
    t_over.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#ffffff"), HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_over)

    if pred_data.get('decoupling'):
        dec = pred_data['decoupling']
        story.append(Spacer(1, 6))
        story.append(Table([[
            Paragraph(f"<b>Academic Decoupling Defense:</b> {dec.get('teacher_summary')}", styles['DisclaimerBox'])
        ]], colWidths=[504], style=[
            ('BACKGROUND', (0,0), (-1,-1), HexColor("#eff6ff")),
            ('BOX', (0,0), (-1,-1), 1, HexColor("#bfdbfe")),
            ('PADDING', (0,0), (-1,-1), 6)
        ]))

    story.append(Spacer(1, 10))
    
    # Review Text Body
    story.append(Paragraph("Evaluated Review Text", styles['SectionHead']))
    review_table = Table([[Paragraph(f"“{pred_data.get('raw_text')}”", styles['BodyTextDark'])]], colWidths=[504])
    review_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(review_table)
    story.append(Spacer(1, 10))
    
    # Salient Keywords
    keywords = pred_data.get("salient_keywords", [])
    if keywords:
        story.append(Paragraph("Top Indicative Terms (TF-IDF Feature Significance)", styles['SectionHead']))
        kw_rows = [[Paragraph("<b>Feature Term</b>", styles['TableHead']), Paragraph("<b>TF-IDF Weight</b>", styles['TableHead'])]]
        for kw in keywords:
            w_name = kw["word"] if isinstance(kw, dict) else str(kw)
            w_wt = str(kw.get("tfidf_weight", "")) if isinstance(kw, dict) else ""
            kw_rows.append([Paragraph(w_name, styles['BodyTextDark']), Paragraph(w_wt, styles['BodyTextDark'])])
        t_kw = Table(kw_rows, colWidths=[252, 252])
        t_kw.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), HexColor("#0284c7")),
            ('GRID', (0,0), (-1,-1), 0.5, HexColor("#cbd5e1")),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#ffffff"), HexColor("#f8fafc")]),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_kw)
        story.append(Spacer(1, 10))
        
    # Academic Disclaimer
    story.append(Spacer(1, 12))
    discl_table = Table([[
        Paragraph(f"<b>Notice:</b> {pred_data.get('disclaimer')}", styles['DisclaimerBox'])
    ]], colWidths=[504])
    discl_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#fef2f2" if is_fake else "#f0fdf4")),
        ('BOX', (0,0), (-1,-1), 1, HexColor("#fecaca" if is_fake else "#bbf7d0")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(discl_table)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    return output_path

def generate_performance_pdf(metadata: dict, output_path: str):
    """Generates comparative model performance and benchmark report."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = _get_report_styles()
    story = []
    
    story.append(Paragraph("ReviewGuard AI: Model Benchmark & Evaluation Report", styles['DocTitle']))
    story.append(Paragraph(f"Empirical Evaluation Results • Generated on {time.strftime('%B %d, %Y at %H:%M:%S')}", styles['DocSubtitle']))
    
    if not metadata or "models" not in metadata:
        story.append(Paragraph("No model training metadata available.", styles['BodyTextDark']))
        doc.build(story, canvasmaker=NumberedCanvas)
        return output_path
        
    # Comparative Metrics Table
    story.append(Paragraph("1. Overall Model Comparison Table", styles['SectionHead']))
    dt = metadata["models"].get("Decision Tree", {})
    ada = metadata["models"].get("AdaBoost", {})
    
    comp_data = [
        [
            Paragraph("<b>Evaluation Metric</b>", styles['TableHead']),
            Paragraph("<b>Decision Tree Classifier</b>", styles['TableHead']),
            Paragraph("<b>AdaBoost Classifier</b>", styles['TableHead']),
            Paragraph("<b>Leading Algorithm</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>Testing Accuracy</b>", styles['BodyTextDark']),
            Paragraph(f"{dt.get('accuracy', 0)*100:.2f}%", styles['BodyTextDark']),
            Paragraph(f"{ada.get('accuracy', 0)*100:.2f}%", styles['BodyTextDark']),
            Paragraph("AdaBoost" if ada.get('accuracy', 0) >= dt.get('accuracy', 0) else "Decision Tree", styles['BodyTextDark'])
        ],
        [
            Paragraph("<b>Precision (Fake Class)</b>", styles['BodyTextDark']),
            Paragraph(f"{dt.get('precision', 0)*100:.2f}%", styles['BodyTextDark']),
            Paragraph(f"{ada.get('precision', 0)*100:.2f}%", styles['BodyTextDark']),
            Paragraph("AdaBoost" if ada.get('precision', 0) >= dt.get('precision', 0) else "Decision Tree", styles['BodyTextDark'])
        ],
        [
            Paragraph("<b>Recall (Fake Class)</b>", styles['BodyTextDark']),
            Paragraph(f"{dt.get('recall', 0)*100:.2f}%", styles['BodyTextDark']),
            Paragraph(f"{ada.get('recall', 0)*100:.2f}%", styles['BodyTextDark']),
            Paragraph("AdaBoost" if ada.get('recall', 0) >= dt.get('recall', 0) else "Decision Tree", styles['BodyTextDark'])
        ],
        [
            Paragraph("<b>F1-Score (Fake Class)</b>", styles['BodyTextDark']),
            Paragraph(f"{dt.get('f1_score', 0)*100:.2f}%", styles['BodyTextDark']),
            Paragraph(f"{ada.get('f1_score', 0)*100:.2f}%", styles['BodyTextDark']),
            Paragraph("AdaBoost" if ada.get('f1_score', 0) >= dt.get('f1_score', 0) else "Decision Tree", styles['BodyTextDark'])
        ],
        [
            Paragraph("<b>Training Time</b>", styles['BodyTextDark']),
            Paragraph(f"{dt.get('train_time_sec', 0):.4f} s", styles['BodyTextDark']),
            Paragraph(f"{ada.get('train_time_sec', 0):.4f} s", styles['BodyTextDark']),
            Paragraph("Decision Tree" if dt.get('train_time_sec', 0) <= ada.get('train_time_sec', 0) else "AdaBoost", styles['BodyTextDark'])
        ]
    ]
    t_comp = Table(comp_data, colWidths=[140, 120, 120, 124])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#ffffff"), HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))
    
    # Embed Matplotlib Static Chart
    chart_dir = os.path.join(os.path.dirname(output_path), "charts")
    charts = generate_matplotlib_charts(metadata, chart_dir)
    if "performance_chart" in charts and os.path.exists(charts["performance_chart"]):
        story.append(Paragraph("2. Graphical Performance Visualization", styles['SectionHead']))
        img = Image(charts["performance_chart"], width=480, height=240)
        story.append(img)
        story.append(Spacer(1, 10))
        
    # Academic Interpretation
    story.append(Paragraph("3. Academic Discussion & Interpretation", styles['SectionHead']))
    interpretation_text = (
        f"In this evaluation run on {metadata.get('total_records', 0)} total dataset records "
        f"({metadata.get('train_samples', 0)} training, {metadata.get('test_samples', 0)} testing), "
        f"both classifiers demonstrate strong discriminatory capability over sublinear TF-IDF features. "
        f"The best overall performing model by F1-Score is <b>{metadata.get('best_model_by_f1')}</b>. "
        f"AdaBoost operates as an ensemble boosting algorithm that iteratively increases weights on harder-to-classify samples, "
        f"yielding robust boundary separation against subtle promotional astroturfing phrasing."
    )
    story.append(Paragraph(interpretation_text, styles['BodyTextDark']))
    story.append(Spacer(1, 10))
    
    # Epistemic Disclaimer
    story.append(Table([[
        Paragraph(
            "<b>Epistemic Qualification:</b> Evaluation metrics are empirically calculated on the holdout test set "
            "using stratified 80/20 partitioning. Real-world accuracy on out-of-domain marketplace products varies based "
            "on data distribution shifts and adversarial text modifications.", styles['DisclaimerBox']
        )
    ]], colWidths=[504], style=[
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    return output_path

def generate_url_analysis_pdf(url_data: dict, output_path: str):
    """Generates batch product URL audit report."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    styles = _get_report_styles()
    story = []
    
    story.append(Paragraph("ReviewGuard AI: Product URL Review Trust Audit", styles['DocTitle']))
    story.append(Paragraph(f"URL: {url_data.get('url')} • Generated on {time.strftime('%B %d, %Y at %H:%M:%S')}", styles['DocSubtitle']))
    
    # Summary Metrics Table
    summary_data = [
        [Paragraph("<b>Audit Parameter</b>", styles['TableHead']), Paragraph("<b>Result</b>", styles['TableHead'])],
        [Paragraph("<b>Product Name</b>", styles['BodyTextDark']), Paragraph(url_data.get('product_name', 'N/A'), styles['BodyTextDark'])],
        [Paragraph("<b>Total Reviews Evaluated</b>", styles['BodyTextDark']), Paragraph(str(url_data.get('total_reviews', 0)), styles['BodyTextDark'])],
        [Paragraph("<b>Predicted Genuine Reviews</b>", styles['BodyTextDark']), Paragraph(f"<font color='#10b981'><b>{url_data.get('genuine_count', 0)}</b></font>", styles['BodyTextDark'])],
        [Paragraph("<b>Predicted Fake / Bot Reviews</b>", styles['BodyTextDark']), Paragraph(f"<font color='#f43f5e'><b>{url_data.get('fake_count', 0)}</b></font>", styles['BodyTextDark'])],
        [Paragraph("<b>Estimated Fake Ratio</b>", styles['BodyTextDark']), Paragraph(f"<b>{url_data.get('fake_percentage', 0)}%</b>", styles['BodyTextDark'])],
        [Paragraph("<b>Collection Trust Status</b>", styles['BodyTextDark']), Paragraph(f"<b>{url_data.get('trust_status', 'N/A')}</b>", styles['BodyTextDark'])],
        [Paragraph("<b>Classifier Utilized</b>", styles['BodyTextDark']), Paragraph(url_data.get('model_used', 'AdaBoost'), styles['BodyTextDark'])]
    ]
    t_sum = Table(summary_data, colWidths=[200, 304])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#ffffff"), HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 10))
    
    # Individual Extracted Review Breakdown
    story.append(Paragraph("Extracted Review Sample & Predictions", styles['SectionHead']))
    rev_rows = [
        [
            Paragraph("<b>#</b>", styles['TableHead']),
            Paragraph("<b>Review Excerpt</b>", styles['TableHead']),
            Paragraph("<b>Prediction</b>", styles['TableHead']),
            Paragraph("<b>Confidence</b>", styles['TableHead'])
        ]
    ]
    for idx, r in enumerate(url_data.get("reviews", [])[:10], start=1):
        is_fk = r.get("prediction_binary") == 1
        lbl = "<font color='#f43f5e'><b>Fake</b></font>" if is_fk else "<font color='#10b981'><b>Genuine</b></font>"
        raw_t = r.get("raw_text", r.get("text", ""))
        excerpt = raw_t[:100] + ("..." if len(raw_t) > 100 else "")
        conf = r.get('confidence_percentage', round(r.get('confidence_score', 0) * 100, 1))
        rev_rows.append([
            Paragraph(str(idx), styles['BodyTextDark']),
            Paragraph(excerpt, styles['BodyTextDark']),
            Paragraph(lbl, styles['BodyTextDark']),
            Paragraph(f"{conf}%", styles['BodyTextDark'])
        ])
        
    t_rev = Table(rev_rows, colWidths=[24, 300, 90, 90])
    t_rev.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor("#0284c7")),
        ('GRID', (0,0), (-1,-1), 0.5, HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor("#ffffff"), HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_rev)
    story.append(Spacer(1, 12))
    
    # Disclaimer
    story.append(Table([[
        Paragraph(f"<b>Disclaimer:</b> {url_data.get('disclaimer')}", styles['DisclaimerBox'])
    ]], colWidths=[504], style=[
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    return output_path

# =====================================================================
# Direct-Call Aliases Supporting Varied Parameter Signatures
# =====================================================================

def generate_prediction_report(pred_data: dict, output_path: str):
    """Wrapper normalizing dictionary fields for single prediction PDF generation."""
    data = dict(pred_data)
    if 'raw_text' not in data:
        data['raw_text'] = data.get('review_text', '')
    if 'confidence_percentage' not in data and 'confidence_score' in data:
        data['confidence_percentage'] = round(data['confidence_score'] * 100, 1)
    if 'probability_genuine' not in data and 'genuine_probability' in data:
        data['probability_genuine'] = round(data['genuine_probability'] * 100, 1)
    if 'probability_fake' not in data and 'fake_probability' in data:
        data['probability_fake'] = round(data['fake_probability'] * 100, 1)
    if 'prediction_binary' not in data:
        data['prediction_binary'] = 1 if data.get('prediction_label') == 'Fake' else 0
    if 'model_used' not in data:
        data['model_used'] = data.get('model_name', 'AdaBoost')
    if 'salient_keywords' not in data and 'top_keywords' in data:
        data['salient_keywords'] = [
            {'word': k, 'tfidf_weight': ''} if isinstance(k, str) else k 
            for k in data['top_keywords']
        ]
    if 'disclaimer' not in data:
        data['disclaimer'] = "Academic & Responsible AI Disclaimer: Statistical prediction based on linguistic features."
    return generate_prediction_pdf(data, output_path)

def generate_model_evaluation_report(metadata_path, output_pdf_path: str):
    """Wrapper loading metadata JSON if path provided, then generating evaluation PDF."""
    if isinstance(metadata_path, str) and os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            meta = json.load(f)
    elif isinstance(metadata_path, dict):
        meta = metadata_path
    else:
        meta = {}
    return generate_performance_pdf(meta, output_pdf_path)

def generate_url_analysis_report(analysis: dict, output_path: str):
    """Wrapper normalizing live URL batch audit fields for PDF generation."""
    data = dict(analysis)
    if 'reviews' not in data:
        data['reviews'] = data.get('detailed_reviews', [])
    if 'product_name' not in data:
        data['product_name'] = data.get('product_title', 'E-Commerce Product Page')
    if 'total_reviews' not in data:
        data['total_reviews'] = data.get('reviews_analyzed_count', len(data.get('reviews', [])))
    if 'fake_percentage' not in data:
        data['fake_percentage'] = 100 - data.get('trust_score', 50)
    if 'trust_status' not in data:
        data['trust_status'] = data.get('trust_level', 'Moderate')
    if 'disclaimer' not in data:
        data['disclaimer'] = "Audit Disclaimer: Evaluated via automated NLP review text parsing with SSRF protection."
    return generate_url_analysis_pdf(data, output_path)
