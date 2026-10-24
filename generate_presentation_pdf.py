"""
ReviewGuard AI - High-Impact 15-Slide Presentation PDF Generator
Designed for Auditorium Visibility (120 People) in 16:9 Widescreen.
Uses ReportLab to render a clean, high-contrast, modern dark-navy slide deck.
"""

import os
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas

# 16:9 Widescreen Dimensions in Points (960 pt x 540 pt)
PAGE_WIDTH = 960
PAGE_HEIGHT = 540

# Custom Modern Color Palette
C_BG_PAGE = HexColor("#07090e")
C_BG_CARD = HexColor("#0d1322")
C_BG_INNER = HexColor("#151d30")
C_BORDER = HexColor("#23314e")
C_PRIMARY = HexColor("#38bdf8")     # Electric Sky Blue
C_SECONDARY = HexColor("#818cf8")   # Neon Violet
C_GREEN = HexColor("#10b981")       # Emerald
C_RED = HexColor("#f43f5e")         # Rose Red
C_AMBER = HexColor("#f59e0b")       # Amber
C_TEXT_MAIN = HexColor("#ffffff")
C_TEXT_SUB = HexColor("#cbd5e1")
C_TEXT_MUTED = HexColor("#94a3b8")

class NumberedCanvas(canvas.Canvas):
    """Custom canvas that draws dark background, top banner, and footer on every slide."""
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
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, total_pages):
        # 1. Dark Full-Bleed Background
        self.setFillColor(C_BG_PAGE)
        self.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)

        # 2. Top Header Line & Brand Badge
        self.setFillColor(C_BG_CARD)
        self.rect(0, PAGE_HEIGHT - 48, PAGE_WIDTH, 48, fill=1, stroke=0)
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(1)
        self.line(0, PAGE_HEIGHT - 48, PAGE_WIDTH, PAGE_HEIGHT - 48)

        # Brand Logo Text
        self.setFont("Helvetica-Bold", 14)
        self.setFillColor(C_PRIMARY)
        self.drawString(36, PAGE_HEIGHT - 32, "ReviewGuard AI")

        self.setFont("Helvetica", 10)
        self.setFillColor(C_TEXT_MUTED)
        self.drawString(160, PAGE_HEIGHT - 32, "|   Advanced Fake Review Detection & Trust Analysis")

        # Slide Number Badge
        self.setFont("Helvetica-Bold", 11)
        self.setFillColor(C_PRIMARY)
        page_str = f"SLIDE {self._pageNumber} / {total_pages}"
        self.drawRightString(PAGE_WIDTH - 36, PAGE_HEIGHT - 32, page_str)

        # 3. Bottom Footer Accent Bar
        self.setStrokeColor(C_BORDER)
        self.line(36, 32, PAGE_WIDTH - 36, 32)
        
        self.setFont("Helvetica", 9)
        self.setFillColor(C_TEXT_MUTED)
        self.drawString(36, 18, "Auditorium & Keynote Defense Edition  *  College ML & NLP Project")
        self.drawRightString(PAGE_WIDTH - 36, 18, "Confidential - For Academic Presentation")


def build_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='SlideTag',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=C_PRIMARY,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='SlideTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=C_TEXT_MAIN,
        spaceAfter=4
    ))

    styles.add(ParagraphStyle(
        name='SlideSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=C_TEXT_MUTED,
        spaceAfter=14
    ))

    styles.add(ParagraphStyle(
        name='CardHeading',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=C_TEXT_MAIN,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='CardBody',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=C_TEXT_SUB,
    ))

    styles.add(ParagraphStyle(
        name='QuoteBox',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=C_TEXT_MAIN,
    ))

    styles.add(ParagraphStyle(
        name='TakeawayBox',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=C_PRIMARY,
    ))

    styles.add(ParagraphStyle(
        name='TakeawayBody',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=C_TEXT_SUB,
    ))

    return styles


def create_presentation_pdf(output_filename="ReviewGuard_AI_Presentation.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=36
    )

    styles = build_styles()
    story = []

    # Slide 1: Welcome & Overview
    story.append(Paragraph("KEYNOTE INTRODUCTION", styles['SlideTag']))
    story.append(Paragraph("ReviewGuard AI", styles['SlideTitle']))
    story.append(Paragraph("Smart Fake Review Detection & Product Trust Analysis Platform", styles['SlideSubtitle']))
    
    col1 = [
        Paragraph("The $152B Problem", styles['CardHeading']),
        Paragraph("Over 30% of reviews on top e-commerce websites are manipulated by botnets, incentivized reviewers, or competitor attacks.", styles['CardBody'])
    ]
    col2 = [
        Paragraph("The Fatal Flaw", styles['CardHeading']),
        Paragraph("Traditional detectors assume <b>'Happy = Genuine'</b> and <b>'Angry = Fake'</b>. In modern adversarial e-commerce, this assumption fails.", styles['CardBody'])
    ]
    col3 = [
        Paragraph("The Solution", styles['CardHeading']),
        Paragraph("ReviewGuard AI decouples Authenticity from Sentiment, detects coordinated bot attacks, and computes a transparent 0-100 Trust Score.", styles['CardBody'])
    ]
    
    t1 = Table([[col1, col2, col3]], colWidths=[285, 285, 285])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('LINEBEFORE', (1,0), (2,0), 1, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t1)
    story.append(Spacer(1, 14))
    
    banner1 = Table([[
        Paragraph("🎯 <b>Core Project Objective:</b> Build an AI system capable of identifying <b>competitor review bombing</b> (fake negatives) and <b>paid astroturfing</b> (fake positives) while preserving legitimate customer voices.", styles['QuoteBox'])
    ]], colWidths=[888])
    banner1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#0f1c30")),
        ('BOX', (0,0), (-1,-1), 1, C_PRIMARY),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(banner1)
    story.append(PageBreak())

    # Slide 2: The Core Industry Flaw
    story.append(Paragraph("THE FUNDAMENTAL PROBLEM", styles['SlideTag']))
    story.append(Paragraph("Why 90% of Fake Review Detectors Fail", styles['SlideTitle']))
    story.append(Paragraph("The fatal error: Conflating Customer Emotion with Review Authenticity.", styles['SlideSubtitle']))
    
    col_left = [
        Paragraph("<font color='#f43f5e'>❌ What Old Systems Do (Wrong)</font>", styles['CardHeading']),
        Paragraph("• They assume 5-star positive praise is always genuine satisfaction.<br/>"
                  "• They assume 1-star negative complaints are automatically fake attacks.<br/>"
                  "• They force every review into an arbitrary binary 50/50 guess.<br/>"
                  "• They claim to know physical product quality from unverified text alone.", styles['CardBody'])
    ]
    col_right = [
        Paragraph("<font color='#10b981'>✅ What ReviewGuard AI Does (Right)</font>", styles['CardHeading']),
        Paragraph("• <b>Decouples Sentiment:</b> A legitimate customer can be angry. A fake bot can leave glowing 5-star praise!<br/>"
                  "• Introduces an <b>Uncertain Band</b> when text evidence is insufficient.<br/>"
                  "• Discovers <b>Coordinated Botnet Clusters</b> across multiple accounts.<br/>"
                  "• Audits <b>Review-Set Trust</b>, not physical factory hardware.", styles['CardBody'])
    ]
    t2 = Table([[col_left, col_right]], colWidths=[432, 432])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor("#1a1018")),
        ('BACKGROUND', (1,0), (1,0), HexColor("#0f1e18")),
        ('BOX', (0,0), (0,0), 1.5, C_RED),
        ('BOX', (1,0), (1,0), 1.5, C_GREEN),
        ('TOPPADDING', (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (-1,-1), 16),
        ('RIGHTPADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t2)
    story.append(Spacer(1, 14))
    
    box2 = Table([[
        Paragraph("💡 <b>The Independence Axiom:</b> P(Authentic | Text) ≠ f(Sentiment Polarity). Authenticity and Sentiment are orthogonal dimensions!", styles['TakeawayBox'])
    ]], colWidths=[888])
    box2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#12192c")),
        ('BOX', (0,0), (-1,-1), 1, C_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(box2)
    story.append(PageBreak())

    # Slide 3: Scenario A - Review Bombing
    story.append(Paragraph("REAL-WORLD ATTACK 1", styles['SlideTag']))
    story.append(Paragraph("Scenario A: Competitor Review Bombing", styles['SlideTitle']))
    story.append(Paragraph("When an authentic, high-quality product is attacked with coordinated fake negative reviews.", styles['SlideSubtitle']))
    
    col_a1 = [
        Paragraph("The Competitor Attack", styles['CardHeading']),
        Paragraph("A rival seller hires a botnet or click-farm to post waves of 1-star complaints using identical phrases. Their goal is to artificially depress product ranking.", styles['CardBody']),
        Spacer(1, 6),
        Paragraph("<b>Bot Review #1:</b> 'Total garbage broke on day 1 do not buy waste of money!'<br/>"
                  "<b>Bot Review #2:</b> 'Total garbage broke on day 2 do not buy waste of cash!'", styles['QuoteBox'])
    ]
    col_a2 = [
        Paragraph("ReviewGuard AI Defense", styles['CardHeading']),
        Paragraph("• Calculates <b>Cosine Similarity (≥ 0.82)</b> across negative reviews.<br/>"
                  "• Identifies the shared template phrasing and unverified burst timing.<br/>"
                  "• Isolates the attack cluster so real positive customer reviews are not drowned out.<br/>"
                  "• <b>Status:</b> Flagged as <font color='#f43f5e'><b>Negative Attack Cluster</b></font>.", styles['CardBody'])
    ]
    t3 = Table([[col_a1, col_a2]], colWidths=[432, 432])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1.5, C_RED),
        ('LINEBEFORE', (1,0), (1,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t3)
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # Slide 4: Scenario B - Astroturfing
    story.append(Paragraph("REAL-WORLD ATTACK 2", styles['SlideTag']))
    story.append(Paragraph("Scenario B: Astroturfing (Paid 5-Star Hype)", styles['SlideTitle']))
    story.append(Paragraph("When a poor-quality or defective item buys fake positive reviews to fool consumers.", styles['SlideSubtitle']))
    
    col_b1 = [
        Paragraph("The Paid Hype Scheme", styles['CardHeading']),
        Paragraph("A seller of cheap, broken goods floods the page with 5-star praise full of promotional superlatives to drown out legitimate customer complaints.", styles['CardBody']),
        Spacer(1, 6),
        Paragraph("<b>Paid Review:</b> 'THIS IS THE GREATEST SMARTWATCH IN HUMAN HISTORY! MIRACLE PRODUCT 1000% RECOMMENDED BUY NOW!'", styles['QuoteBox'])
    ]
    col_b2 = [
        Paragraph("ReviewGuard AI Defense", styles['CardHeading']),
        Paragraph("• Detects <b>abnormally high promotional buzzword density</b> and excessive punctuation.<br/>"
                  "• Identifies near-duplicate 5-star clusters across new or unverified accounts.<br/>"
                  "• Protects consumers by exposing artificial positive sentiment.<br/>"
                  "• <b>Status:</b> Flagged as <font color='#f59e0b'><b>Promotional Astroturfing Cluster</b></font>.", styles['CardBody'])
    ]
    t4 = Table([[col_b1, col_b2]], colWidths=[432, 432])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1.5, C_AMBER),
        ('LINEBEFORE', (1,0), (1,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t4)
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # Slide 5: Scenario C - Authentic Mixed
    story.append(Paragraph("AUTHENTIC MARKETPLACE DYNAMICS", styles['SlideTag']))
    story.append(Paragraph("Scenario C: Authentic Mixed Feedback", styles['SlideTitle']))
    story.append(Paragraph("Preserving healthy customer disagreement without false fraud alarms.", styles['SlideSubtitle']))
    
    col_c1 = [
        Paragraph("Normal Customer Variance", styles['CardHeading']),
        Paragraph("Real customers legitimately disagree! One user loves the bass response; another finds the headband too tight. Diverse opinions are healthy, not fraudulent.", styles['CardBody']),
        Spacer(1, 6),
        Paragraph("<b>Real Review:</b> 'Sound quality is great for audiobooks, but the charging cable was a bit shorter than I wanted. Solid 4 stars.'", styles['QuoteBox'])
    ]
    col_c2 = [
        Paragraph("ReviewGuard AI Defense", styles['CardHeading']),
        Paragraph("• Measures <b>high vocabulary entropy</b> (natural, organic writing diversity).<br/>"
                  "• Detects realistic distribution across 3, 4, and 5-star ratings.<br/>"
                  "• Does NOT penalize negative reviews as fake.<br/>"
                  "• <b>Status:</b> Verified as <font color='#10b981'><b>High Trust Organic Feedback</b></font>.", styles['CardBody'])
    ]
    t5 = Table([[col_c1, col_c2]], colWidths=[432, 432])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1.5, C_GREEN),
        ('LINEBEFORE', (1,0), (1,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t5)
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # Slide 6: Architecture & Three Modules
    story.append(Paragraph("SYSTEM ARCHITECTURE", styles['SlideTag']))
    story.append(Paragraph("The Three Independent Modules", styles['SlideTitle']))
    story.append(Paragraph("Decoupling security, customer experience, and review-set trust.", styles['SlideSubtitle']))
    
    m1 = [
        Paragraph("<font color='#38bdf8'>MODULE 1</font>", styles['SlideTag']),
        Paragraph("Authenticity Detector", styles['CardHeading']),
        Paragraph("Evaluates each review text using DistilBERT / Calibrated Classifiers to determine if it is Likely Genuine, Suspicious, or Uncertain.", styles['CardBody'])
    ]
    m2 = [
        Paragraph("<font color='#818cf8'>MODULE 2</font>", styles['SlideTag']),
        Paragraph("Sentiment & Topics", styles['CardHeading']),
        Paragraph("Mines customer opinions across product aspects: Battery, Durability, Delivery, Packaging, Price, and Customer Support.", styles['CardBody'])
    ]
    m3 = [
        Paragraph("<font color='#10b981'>MODULE 3</font>", styles['SlideTag']),
        Paragraph("Trust Analyzer", styles['CardHeading']),
        Paragraph("Discovers duplicate clusters, coordinates pattern checks, and computes the transparent 0–100 Review Trust Score.", styles['CardBody'])
    ]
    t6 = Table([[m1, m2, m3]], colWidths=[285, 285, 285])
    t6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1.5, C_BORDER),
        ('LINEBEFORE', (1,0), (2,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t6)
    story.append(Spacer(1, 14))
    
    b6 = Table([[
        Paragraph("<b>Separation of Concerns:</b> Security checking (Module 1) never contaminates customer voice mining (Module 2). Trust scoring (Module 3) aggregates patterns across the entire collection.", styles['QuoteBox'])
    ]], colWidths=[888])
    b6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#0f1c30")),
        ('BOX', (0,0), (-1,-1), 1, C_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(b6)
    story.append(PageBreak())

    # Slide 7: Module 1 ML Pipeline
    story.append(Paragraph("MODULE 1 DEEP DIVE", styles['SlideTag']))
    story.append(Paragraph("AI Authenticity Classification Pipeline", styles['SlideTitle']))
    story.append(Paragraph("Combining Sequence Transformers, Feature Calibration, and Stylometry.", styles['SlideSubtitle']))
    
    p1 = [
        Paragraph("Machine Learning Core", styles['CardHeading']),
        Paragraph("• <b>Sequence Transformer:</b> Fine-tuned DistilBERT / Calibrated LinearSVC.<br/>"
                  "• <b>Feature Extraction:</b> Sublinear TF-IDF (1–3 n-grams) capturing subtle stylistic patterns.<br/>"
                  "• <b>Stylometric Metrics:</b> Lexical entropy, punctuation frequency, capitalization ratio.<br/>"
                  "• <b>Calibration:</b> Platt Scaling / Sigmoid calibration ensures probabilities match real-world odds.", styles['CardBody'])
    ]
    p2 = [
        Paragraph("Three Decision Tiers", styles['CardHeading']),
        Paragraph("<b>1. Likely Genuine:</b> Natural phrasing, high lexical entropy, grounded product details.<br/><br/>"
                  "<b>2. Suspicious:</b> High promotional jargon, repeated bot templates, or rating mismatch.<br/><br/>"
                  "<b>3. Uncertain:</b> Statistical confidence falls within the ambiguous boundary margin.", styles['CardBody'])
    ]
    t7 = Table([[p1, p2]], colWidths=[432, 432])
    t7.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('LINEBEFORE', (1,0), (1,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t7)
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # Slide 8: The Uncertain Category Innovation
    story.append(Paragraph("SCIENTIFIC INTEGRITY", styles['SlideTag']))
    story.append(Paragraph("The 'Uncertain' Category Innovation", styles['SlideTitle']))
    story.append(Paragraph("Why honest AI refuses to force arbitrary 50/50 binary decisions.", styles['SlideSubtitle']))
    
    u1 = [
        Paragraph("The Problem with Binary AI", styles['CardHeading']),
        Paragraph("Imagine a short 2-word review: <i>'Good product.'</i><br/><br/>"
                  "Is it a real customer in a rush? Or an automated spam bot?<br/>"
                  "<b>There is simply not enough textual entropy to know!</b><br/>"
                  "Binary models flip a coin, producing massive false-positive spikes.", styles['CardBody'])
    ]
    u2 = [
        Paragraph("The ReviewGuard Solution", styles['CardHeading']),
        Paragraph("If confidence falls within our decision margin (τ = 0.15 around 0.50), ReviewGuard AI categorizes the review as <b>Uncertain</b> with an explicit explanation.<br/><br/>"
                  "<b>Viva Key Point:</b> In scientific machine learning, honest uncertainty is far superior to forced fake certainty.", styles['CardBody'])
    ]
    t8 = Table([[u1, u2]], colWidths=[432, 432])
    t8.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1.5, C_AMBER),
        ('LINEBEFORE', (1,0), (1,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t8)
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # Slide 9: Multi-Signal Evidence Engine
    story.append(Paragraph("EXPLAINABLE AI (XAI)", styles['SlideTag']))
    story.append(Paragraph("Multi-Signal Evidence Extraction", styles['SlideTitle']))
    story.append(Paragraph("Every flagged prediction is accompanied by human-auditable proof.", styles['SlideSubtitle']))
    
    signals = [
        [Paragraph("<b>Detection Signal</b>", styles['CardHeading']), Paragraph("<b>Mechanism</b>", styles['CardHeading']), Paragraph("<b>Evidence Badge</b>", styles['CardHeading'])],
        [Paragraph("Near-Duplicate Text", styles['CardBody']), Paragraph("Cosine Similarity ≥ 0.82 across review database", styles['CardBody']), Paragraph("<font color='#f43f5e'><b>[Near-Duplicate Cluster]</b></font>", styles['CardBody'])],
        [Paragraph("Promotional Buzzwords", styles['CardBody']), Paragraph("Hyperbolic sales vocabulary & exclamation density", styles['CardBody']), Paragraph("<font color='#f59e0b'><b>[Promotional Hype Script]</b></font>", styles['CardBody'])],
        [Paragraph("Rating Contradiction", styles['CardBody']), Paragraph("1-star rating containing 5-star praise text", styles['CardBody']), Paragraph("<font color='#f43f5e'><b>[Rating Inversion Anomaly]</b></font>", styles['CardBody'])],
        [Paragraph("Coordinated Complaints", styles['CardBody']), Paragraph("Identical complaint templates across unverified accounts", styles['CardBody']), Paragraph("<font color='#f43f5e'><b>[Repeated Complaint Script]</b></font>", styles['CardBody'])],
        [Paragraph("Low Textual Entropy", styles['CardBody']), Paragraph("Review length < 5 words or margin near 50%", styles['CardBody']), Paragraph("<font color='#38bdf8'><b>[High Uncertainty Margin]</b></font>", styles['CardBody'])],
    ]
    t9 = Table(signals, colWidths=[200, 420, 260])
    t9.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor("#111a2e")),
        ('BACKGROUND', (0,1), (-1,-1), C_BG_CARD),
        ('GRID', (0,0), (-1,-1), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t9)
    story.append(PageBreak())

    # Slide 10: Near-Duplicate Clustering Engine
    story.append(Paragraph("BOTNET DETECTION", styles['SlideTag']))
    story.append(Paragraph("Near-Duplicate Clustering Engine", styles['SlideTitle']))
    story.append(Paragraph("Catching bot campaigns and syndicated spam via Semantic Cosine Clustering.", styles['SlideSubtitle']))
    
    cl1 = [
        Paragraph("How Botnets Evade Simple Filters", styles['CardHeading']),
        Paragraph("Click-farms change one or two words to bypass exact string matching:<br/><br/>"
                  "<b>Bot #1:</b> 'Defective item died in 1 day do not buy waste of money!'<br/>"
                  "<b>Bot #2:</b> 'Defective item died in 2 days do not buy waste of cash!'<br/><br/>"
                  "Exact matching fails completely. <b>ReviewGuard AI spots it instantly!</b>", styles['CardBody'])
    ]
    cl2 = [
        Paragraph("Our Clustering Algorithm", styles['CardHeading']),
        Paragraph("• Generates an all-pairs <b>Cosine Similarity Matrix</b> using sublinear character & word TF-IDF.<br/>"
                  "• Runs graph-based Connected Components at threshold <b>≥ 0.82</b>.<br/>"
                  "• Identifies cluster archetypes and displays member reviews together for quick auditing.<br/>"
                  "• <b>Similarity: 0.89 → Flagged in Cluster #1</b>", styles['CardBody'])
    ]
    t10 = Table([[cl1, cl2]], colWidths=[432, 432])
    t10.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1.5, C_PRIMARY),
        ('LINEBEFORE', (1,0), (1,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t10)
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # Slide 11: Module 2 - Sentiment & Aspects
    story.append(Paragraph("MODULE 2 DEEP DIVE", styles['SlideTag']))
    story.append(Paragraph("Customer Sentiment & Aspect Mining", styles['SlideTitle']))
    story.append(Paragraph("Extracting genuine customer voice across specific product features.", styles['SlideSubtitle']))
    
    as1 = [
        Paragraph("1. Sentiment Polarity", styles['CardHeading']),
        Paragraph("Calculates distribution across the review collection without biasing authenticity:<br/><br/>"
                  "• <font color='#10b981'><b>Positive (62%)</b></font><br/>"
                  "• <font color='#f59e0b'><b>Neutral (14%)</b></font><br/>"
                  "• <font color='#f43f5e'><b>Negative (24%)</b></font>", styles['CardBody'])
    ]
    as2 = [
        Paragraph("2. Feature Aspects", styles['CardHeading']),
        Paragraph("Mines opinions on core product dimensions:<br/><br/>"
                  "• 🔋 <b>Battery Life & Power</b><br/>"
                  "• 🔨 <b>Build Quality & Durability</b><br/>"
                  "• 📦 <b>Delivery & Packaging</b><br/>"
                  "• 💰 <b>Price & Value for Money</b>", styles['CardBody'])
    ]
    as3 = [
        Paragraph("3. Strengths vs Weaknesses", styles['CardHeading']),
        Paragraph("Actionable feedback summary:<br/><br/>"
                  "• <font color='#10b981'><b>Top Strength:</b></font> 'Clear audio, fast bluetooth pairing.'<br/><br/>"
                  "• <font color='#f43f5e'><b>Top Complaint:</b></font> 'Charging cable too short.'", styles['CardBody'])
    ]
    t11 = Table([[as1, as2, as3]], colWidths=[285, 285, 285])
    t11.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('LINEBEFORE', (1,0), (2,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t11)
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # Slide 12: Contradictory Experiences
    story.append(Paragraph("DIAGNOSTIC INTELLIGENCE", styles['SlideTag']))
    story.append(Paragraph("Detecting Contradictory Customer Experiences", styles['SlideTitle']))
    story.append(Paragraph("Highlighting extreme polar disagreements across specific product features.", styles['SlideSubtitle']))
    
    co1 = [
        Paragraph("The Battery Life Contradiction", styles['CardHeading']),
        Paragraph("<b>Customer A:</b> 'Battery lasted my entire 3-day weekend camping trip easily.'<br/><br/>"
                  "<b>Customer B:</b> 'Battery died in 30 minutes, won't hold charge at all.'<br/><br/>"
                  "ReviewGuard AI flags: <font color='#f59e0b'><b>[High Polar Variance on Battery Life]</b></font>", styles['CardBody'])
    ]
    co2 = [
        Paragraph("Diagnostic Value for Sellers & Buyers", styles['CardHeading']),
        Paragraph("• <b>Catches Factory Batch Defects:</b> Helps the manufacturer discover that 5% of units from a specific batch had bad battery cells.<br/><br/>"
                  "• <b>Exposes Astroturfing:</b> If genuine buyers report failures, repetitive 5-star praise stands out immediately.<br/><br/>"
                  "• <b>Protects Consumers:</b> Alerts shoppers to potential inconsistencies before purchase.", styles['CardBody'])
    ]
    t12 = Table([[co1, co2]], colWidths=[432, 432])
    t12.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1.5, C_SECONDARY),
        ('LINEBEFORE', (1,0), (1,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(t12)
    story.append(Spacer(1, 14))
    story.append(PageBreak())

    # Slide 13: Module 3 Trust Score Formula
    story.append(Paragraph("MODULE 3 DEEP DIVE", styles['SlideTag']))
    story.append(Paragraph("The Transparent Trust Score (0–100)", styles['SlideTitle']))
    story.append(Paragraph("An open, mathematically grounded formula with zero black-box mystery.", styles['SlideSubtitle']))
    
    f_box = Table([[
        Paragraph("<b>Review Trust Score Formula:</b><br/>"
                  "Trust Score = max(0, min(100, 100 - (R_suspicious × 60) - (R_duplicates × 25) - (R_contradictions × 10) - (R_uncertain × 5)))", styles['QuoteBox'])
    ]], colWidths=[888])
    f_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#111a2e")),
        ('BOX', (0,0), (-1,-1), 1, C_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(f_box)
    story.append(Spacer(1, 14))
    
    tr1 = [Paragraph("<font color='#10b981'><b>80 – 100</b></font><br/><b>High Trust</b>", styles['CardHeading']), Paragraph("Organic linguistic variance, negligible duplicate clusters.", styles['CardBody'])]
    tr2 = [Paragraph("<font color='#38bdf8'><b>60 – 79</b></font><br/><b>Moderate Trust</b>", styles['CardHeading']), Paragraph("Minor duplicate phrasing; inspect reviews with caution.", styles['CardBody'])]
    tr3 = [Paragraph("<font color='#f59e0b'><b>40 – 59</b></font><br/><b>Low Trust</b>", styles['CardHeading']), Paragraph("Substantial bot clusters or high suspicious ratio.", styles['CardBody'])]
    tr4 = [Paragraph("<font color='#f43f5e'><b>0 – 39</b></font><br/><b>Very Low Trust</b>", styles['CardHeading']), Paragraph("Heavy coordinated manipulation, severe duplicates, bot attack.", styles['CardBody'])]
    
    t13 = Table([[tr1, tr2, tr3, tr4]], colWidths=[210, 210, 210, 210])
    t13.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('LINEBEFORE', (1,0), (-1,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(t13)
    story.append(PageBreak())

    # Slide 14: Responsible AI & Quality Disclaimer
    story.append(Paragraph("RESPONSIBLE AI & ETHICS", styles['SlideTag']))
    story.append(Paragraph("Product Quality Limitation & Disclaimer", styles['SlideTitle']))
    story.append(Paragraph("Scientific integrity means refusing to make claims beyond the data's epistemic reach.", styles['SlideSubtitle']))
    
    disc_box = Table([[
        Paragraph("⚖️ <b>The ReviewGuard AI Epistemic Limitation:</b><br/><br/>"
                  "<i>'ReviewGuard AI analyzes review patterns and customer-reported experiences. It cannot independently verify actual product quality, product authenticity, reviewer intent, or whether a review is fraudulent. Suspicious patterns require further investigation.'</i><br/><br/>"
                  "<b>Product Quality Status: <font color='#38bdf8'>Not Independently Verified</font></b>", styles['QuoteBox'])
    ]], colWidths=[888])
    disc_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#0e1a2f")),
        ('BOX', (0,0), (-1,-1), 1.5, C_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 16),
    ]))
    story.append(disc_box)
    story.append(Spacer(1, 14))
    
    disc_t = Table([[
        [Paragraph("What We Audit", styles['CardHeading']), Paragraph("The authenticity, pattern consistency, and trustworthiness of the <b>submitted customer review collection</b>.", styles['CardBody'])],
        [Paragraph("What We Refuse to Fabricate", styles['CardHeading']), Paragraph("We do not claim to physically test hardware in a laboratory or independently confirm manufacturing claims.", styles['CardBody'])]
    ]], colWidths=[432, 432])
    disc_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('LINEBEFORE', (1,0), (1,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(disc_t)
    story.append(PageBreak())

    # Slide 15: Conclusion & Viva Defense
    story.append(Paragraph("DEFENSE & KEY TAKEAWAYS", styles['SlideTag']))
    story.append(Paragraph("Conclusion & Viva Defense Cheat Sheet", styles['SlideTitle']))
    story.append(Paragraph("Top three questions evaluators will ask and exact winning answers.", styles['SlideSubtitle']))
    
    v1 = [
        Paragraph("<font color='#38bdf8'>Q1: Can positive reviews be fake?</font>", styles['CardHeading']),
        Paragraph("<b>Answer:</b> 'Yes! In Astroturfing, sellers buy fake 5-star praise to mask poor products. That is why ReviewGuard AI decouples sentiment from authenticity.'", styles['CardBody'])
    ]
    v2 = [
        Paragraph("<font color='#f59e0b'>Q2: How do you prevent Data Leakage?</font>", styles['CardHeading']),
        Paragraph("<b>Answer:</b> 'Feature vectorizers and calibration transforms are fitted exclusively on training splits inside isolated Scikit-Learn Pipelines.'", styles['CardBody'])
    ]
    v3 = [
        Paragraph("<font color='#10b981'>Q3: What makes this project unique?</font>", styles['CardHeading']),
        Paragraph("<b>Answer:</b> 'It solves review bombing, includes an Uncertain band, generates a 0-100 Trust Score, extracts product aspects, and exports audit PDFs.'", styles['CardBody'])
    ]
    t15 = Table([[v1, v2, v3]], colWidths=[285, 285, 285])
    t15.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1.5, C_BORDER),
        ('LINEBEFORE', (1,0), (2,0), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(t15)
    story.append(Spacer(1, 14))
    
    fin_box = Table([[
        Paragraph("🎉 <b>Summary:</b> ReviewGuard AI is an honest, scientifically grounded, and production-ready NLP system built for real-world e-commerce trust analysis.", styles['QuoteBox'])
    ]], colWidths=[888])
    fin_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#0f1e18")),
        ('BOX', (0,0), (-1,-1), 1, C_GREEN),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(fin_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Presentation PDF successfully built: {output_filename} ({PAGE_WIDTH}x{PAGE_HEIGHT} pt 16:9 widescreen, 15 pages)")

if __name__ == "__main__":
    create_presentation_pdf("c:/Shivam/Coding/ML PROJECT/fake review detector/ReviewGuard_AI_Presentation.pdf")
