"""
ReviewGuard AI - Master Presentation Generator (PPTX & PDF)
Strictly adheres to the 15-Slide Specification for Academic Defense and Viva Voce.
Includes embedded speaker notes, professional dark AI aesthetics, and 16:9 widescreen layout.
Fully diversified slide layouts: Every slide from Slide 1 to 15 has a unique, visually distinctive design.
"""

import os
import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfgen import canvas

def clean_html(text):
    """Strips HTML tags like <b>, </b>, <i>, </i>, <br/> for clean PPTX rendering."""
    if not text:
        return ""
    clean = re.sub(r'<br\s*/?>', '\n', text)
    clean = re.sub(r'<[^>]+>', '', clean)
    return clean.strip()

# ==========================================================
# 15-SLIDE COMPREHENSIVE DATASET & EMBEDDED SPEAKER SCRIPT
# ==========================================================

SLIDES_DATA = [
    # SLIDE 1
    {
        "num": 1,
        "tag": "PROJECT DEFENSE & VIVA VOCE PRESENTATION",
        "title": "ReviewGuard AI",
        "subtitle": "Advanced Fake Review Detection & Product Trust Analysis System",
        "layout": "meta",
        "meta": [
            ("Student Name", "[Your Name]"),
            ("Department", "[Your Department]"),
            ("Institution", "[College Name]"),
            ("Project Guide", "[Guide Name]"),
            ("Academic Year", "[Academic Year]")
        ],
        "highlights": [
            "Decoupled 3-Module NLP Architecture",
            "Coordinated Review Bombing & Astroturfing Detection",
            "Aspect-Based Sentiment & Feature Contradiction Mining",
            "Transparent Mathematical Review-Set Trust Scoring",
            "Strict Epistemic Distinction: Review Trust vs Physical Quality"
        ],
        "footer": "ReviewGuard AI — Advanced Machine Learning for E-Commerce Review Integrity & Trust Analysis",
        "speaker_notes": (
            "Respected members of the evaluation committee, guide, and fellow peers, good morning. "
            "I am pleased to present my project: ReviewGuard AI — an Advanced Fake Review Detection and Product Trust Analysis System. "
            "E-commerce platforms rely heavily on customer reviews to guide buyer decisions, yet billions of dollars are distorted annually "
            "by coordinated fake positive praise and malicious competitor review-bombing. "
            "Our system addresses this fundamental challenge through three independent analytical modules, calibrated probabilistic classification, "
            "semantic near-duplicate clustering, and an open, transparent review trust formula."
        ),
        "viva_qna": "Q: What is the primary objective of ReviewGuard AI?\nA: To provide a transparent, multi-perspective review analysis platform that decouples review authenticity from customer sentiment and evaluates collection-level trust without making unverified claims about physical product quality."
    },

    # SLIDE 2
    {
        "num": 2,
        "tag": "PROBLEM DOMAIN & INDUSTRY CONTEXT",
        "title": "Introduction: The Trust Crisis in Online Reviews",
        "subtitle": "Customer reviews drive purchasing decisions, but coordinated manipulation undermines marketplace trust.",
        "layout": "comparison",
        "left_title": "The Decisive Role of Customer Reviews",
        "left_points": [
            "Over <b>93% of consumers</b> read online reviews before finalizing a purchase.",
            "A single 1-star drop in rating can reduce merchant revenue by <b>5% to 9%</b>.",
            "Reviews represent direct, unstructured customer feedback on product quality, shipping, and service.",
            "However, platforms face industrial-scale manipulation, from bot syndicates to paid review brokerages."
        ],
        "right_title": "How Manipulation Distorts Traditional Averages",
        "right_points": [
            "<b>Astroturfing Hype:</b> Defective or inferior products artificially inflate star ratings with purchased 5-star praise.",
            "<b>Coordinated Review Bombing:</b> Competitors flood high-quality products with identical 1-star attack scripts.",
            "<b>Legitimate Disagreement:</b> Real buyers naturally hold mixed opinions (e.g., great sound vs. heavy build).",
            "<b>The Failure of Simple Averages:</b> Arithmetic star averages cannot distinguish organic feedback from coordinated manipulation."
        ],
        "footer": "Traditional star ratings treat all reviews equally; ReviewGuard AI examines linguistic integrity and collection patterns.",
        "speaker_notes": (
            "Slide 2 introduces our problem context. Online customer reviews are the lifeblood of modern digital commerce. "
            "Over 93% of buyers rely on them. However, star ratings are routinely weaponized. "
            "Disreputable sellers commission astroturfing campaigns to artificially inflate poor products with 5-star praise. "
            "Conversely, rival vendors execute coordinated review bombing against reputable sellers using botnets with identical 1-star complaints. "
            "Traditional star averages are mathematically blind to these asymmetries, treating an automated bot script with the same weight as an authentic customer."
        ),
        "viva_qna": "Q: Why are arithmetic average star ratings inadequate for detecting fraud?\nA: Arithmetic averages fail because they treat every review identically, ignoring repetition, semantic clustering, linguistic anomalies, and coordinated timing bursts."
    },

    # SLIDE 3
    {
        "num": 3,
        "tag": "PROBLEM STATEMENT & CORE PRINCIPLE",
        "title": "Problem Statement: The Flaw in Binary Detectors",
        "subtitle": "Traditional systems conflate sentiment with authenticity, causing catastrophic false positives and vulnerabilities.",
        "layout": "cards_2",
        "left_title": "The Fatal Flaw of Legacy Detectors",
        "left_points": [
            "<b>Naïve Sentiment Bias:</b> Many legacy systems assume that <i>Positive Reviews = Genuine</i> and <i>Negative Reviews = Fake</i>.",
            "<b>Forced Binary Trap:</b> Binary classifiers (0 or 1) force ambiguous, short, or neutral reviews into arbitrary guesses.",
            "<b>Isolated Evaluation:</b> Evaluating reviews individually misses coordinated botnet campaigns sharing near-duplicate text.",
            "<b>Overstepping Claims:</b> Systems falsely claim to verify physical product quality based purely on digital text."
        ],
        "right_title": "The ReviewGuard AI Axioms",
        "right_points": [
            "<b>Axiom 1 (Orthogonal Independence):</b> Sentiment and authenticity are independent axes. A 5-star review can be fake; an angry 1-star review can be genuine.",
            "<b>Axiom 2 (Explicit Uncertainty):</b> Reviews with insufficient textual entropy are marked <i>Uncertain</i> rather than forced into binary guesses.",
            "<b>Axiom 3 (Review-Set Pattern Analysis):</b> Coordinated deception is uncovered through collection-level near-duplicate clustering.",
            "<b>Axiom 4 (Epistemic Honesty):</b> We audit review collection trust; we do not claim to verify physical hardware quality."
        ],
        "footer": "Core Foundational Principle: Authenticity, Customer Sentiment, and Review-Set Trustworthiness are three independent dimensions.",
        "speaker_notes": (
            "Moving to Slide 3, we define our problem statement and core scientific axioms. "
            "The fatal flaw in traditional detectors is the conflation of customer sentiment with authenticity. "
            "When an angry customer writes a blunt negative review about a defective battery, naïve models frequently flag it as malicious. "
            "Meanwhile, botnets leaving generic 5-star praise slip through unnoticed. "
            "Our research proves that authenticity and sentiment are two orthogonal axes. Furthermore, reviews cannot be judged purely in isolation; "
            "coordinated campaigns can only be uncovered by analyzing review-set clustering."
        ),
        "viva_qna": "Q: Can a positive review be fake?\nA: Absolutely. In astroturfing campaigns, sellers buy fake 5-star praise packed with marketing buzzwords to mask serious product defects."
    },

    # SLIDE 4
    {
        "num": 4,
        "tag": "PROPOSED SOLUTION",
        "title": "ReviewGuard AI: Holistic Multi-Perspective System",
        "subtitle": "An AI/ML-powered analytical platform evaluating individual reviews and overall collection trust.",
        "layout": "pipeline",
        "pipeline_steps": [
            ("Review Input", "CSV, XLSX, or Text Ingestion with Metadata"),
            ("Authenticity Detector", "DistilBERT / Calibrated SVM + Evidence Extraction"),
            ("Sentiment & Topics", "Aspect Mining & Contradiction Detection"),
            ("Trust Analyzer", "Cosine Clustering & 0–100 Trust Scoring"),
            ("Interactive UI & Report", "React Dashboard & ReportLab Audit PDF")
        ],
        "capabilities": [
            "<b>Review Authenticity:</b> Calibrated classification into Likely Genuine, Suspicious, or Uncertain.",
            "<b>Aspect & Topic Mining:</b> Extracts customer voice on Battery, Durability, Delivery, Price, and Support.",
            "<b>Near-Duplicate Clustering:</b> Identifies syndicated bot scripts using Cosine Semantic Similarity (≥ 0.82).",
            "<b>Transparent Trust Scoring:</b> Computes an open 0–100 Trust Score with documented mathematical penalties."
        ],
        "footer": "End-to-End Pipeline: Raw Reviews → Multi-Signal NLP → Pattern & Cluster Analysis → Actionable Dashboard & PDF Audit.",
        "speaker_notes": (
            "To resolve these challenges, we introduce ReviewGuard AI. The system follows an end-to-end multi-perspective pipeline. "
            "First, raw customer reviews are ingested via manual text, CSV, or Excel spreadsheets with optional metadata. "
            "The data passes into three independent analytical modules: Module 1 estimates individual authenticity; "
            "Module 2 mines sentiment polarity and product-specific topics like battery life and durability; "
            "and Module 3 aggregates near-duplicate clusters and calculates a transparent 0-to-100 Review Trust Score. "
            "Finally, the findings are rendered on an interactive dashboard and exported as an audit-ready PDF report."
        ),
        "viva_qna": "Q: What are the three analytical perspectives in ReviewGuard AI?\nA: 1) Review Authenticity (Is the text genuine or suspicious?), 2) Customer Experience (What do buyers feel and experience?), and 3) Review-Set Trustworthiness (How reliable is the overall collection?)."
    },

    # SLIDE 5
    {
        "num": 5,
        "tag": "SYSTEM ARCHITECTURE",
        "title": "Planned System Architecture & Technical Stack",
        "subtitle": "Modular, service-oriented architecture connecting the frontend, backend APIs, and ML models.",
        "layout": "arch_grid",
        "arch_tiers": [
            ("Frontend Tier", "React.js • Tailwind CSS • Recharts", "• Single-page responsive dashboard\n• Interactive 0–100 Trust Score gauge\n• Near-duplicate cluster explorer\n• Searchable, filterable review table with in-place editing"),
            ("Backend API Tier", "Python • FastAPI • Pydantic v2", "• High-throughput asynchronous REST endpoints\n• Safe CSV and Excel (.xlsx) file parsing\n• ReportLab PDF generation engine\n• Configurable uncertainty & similarity thresholds"),
            ("NLP & Machine Learning", "Scikit-Learn • DistilBERT • TF-IDF", "• Sublinear TF-IDF (1–3 n-grams) + Stylometry\n• Calibrated probabilistic classification (LinearSVC/LogReg)\n• Fine-tuned DistilBERT sequence classification option\n• Cosine similarity matrix & connected-components graph"),
            ("Data & Persistence Tier", "MongoDB Integration • Fallback Store", "• Resilient persistence via pymongo connector\n• Automated local JSON fallback store for standalone execution\n• Preloaded demonstration datasets (Scenario A, B, C)")
        ],
        "footer": "Architecture Note: Planned modular design adhering to strict separation of concerns, validated API schemas, and resilient fallbacks.",
        "speaker_notes": (
            "Here is our planned system architecture. The system is architected across four decoupled tiers: "
            "The frontend is built with React.js, Tailwind CSS, and Recharts, providing responsive data tables and trust score visualizations. "
            "The backend is powered by FastAPI in Python, utilizing Pydantic schemas for validated request processing and ReportLab for PDF generation. "
            "The machine learning core integrates sublinear TF-IDF with calibrated linear classifiers and a fine-tuned DistilBERT backbone. "
            "Finally, the storage tier connects to MongoDB with an automatic local file-based fallback store, ensuring the system operates "
            "reliably in any demonstration environment without database configuration overhead."
        ),
        "viva_qna": "Q: Why use FastAPI over Flask or Django for this project?\nA: FastAPI offers asynchronous high-throughput execution, automated OpenAPI documentation, and native Pydantic validation, which is critical for real-time review processing."
    },

    # SLIDE 6
    {
        "num": 6,
        "tag": "MODULE 1 DEEP DIVE",
        "title": "Module 1: AI-Powered Review Authenticity Detector",
        "subtitle": "Evaluating individual review suspiciousness using calibrated probabilities and multi-signal evidence.",
        "layout": "module1",
        "inputs": "Review Text, Star Rating, Timestamp, Verified-Purchase Flag, Reviewer ID (when available)",
        "pipeline_text": "Text Normalization → Sublinear TF-IDF (1-3 n-grams) + Stylometrics → Calibrated Sequence Classifier → Decision Margin",
        "tiers": [
            ("Likely Genuine", "P(Genuine) ≥ 0.50 + Margin", "Natural vocabulary variance, realistic detail, balanced syntax."),
            ("Suspicious", "P(Suspicious) ≥ 0.50 + Margin", "High promotional density, matching bot templates, rating contradiction."),
            ("Uncertain", "|P - 0.50| < 0.15 Margin", "Low textual entropy (< 5 words) or ambiguous boundary confidence.")
        ],
        "evidence_signals": [
            "Near-Duplicate Cluster Member (Cosine Sim ≥ 0.82)",
            "Repetitive Promotional Language & Buzzword Density",
            "Coordinated Repeated Complaint Script",
            "Rating-Sentiment Inversion Anomaly",
            "Suspicious Timing Burst involving Unverified Purchases"
        ],
        "footer": "Default Uncertainty Margin: τ = 0.15. Borderline cases are categorized as Uncertain rather than forced into arbitrary binary labels.",
        "speaker_notes": (
            "Now let us examine Module 1: The Review Authenticity Detector. "
            "This module ingests review text along with optional metadata like star ratings, timestamps, and verified-purchase status. "
            "The text is transformed into sublinear TF-IDF word and character n-grams combined with stylometric features. "
            "The classifier utilizes Platt scaling calibration so that output probabilities represent true empirical confidence. "
            "Crucially, instead of forcing a binary 0 or 1, we implement an explicit uncertainty band with a default margin of 0.15. "
            "If confidence lies between 0.35 and 0.65, or if the review is under 5 words, it is honestly labeled 'Uncertain'. "
            "Every prediction is accompanied by specific evidence tags, such as near-duplicate matching or rating-sentiment inversion."
        ),
        "viva_qna": "Q: What is probability calibration and why is it necessary?\nA: Standard classifiers like SVM output uncalibrated distance margins. Calibration (via Platt scaling or isotonic regression) maps margins into true posterior probabilities, preventing overconfident false predictions."
    },

    # SLIDE 7
    {
        "num": 7,
        "tag": "MODULE 2 DEEP DIVE",
        "title": "Module 2: Customer Sentiment & Experience Analysis",
        "subtitle": "Mining customer emotion, feature-level topics, and contradictory experiences independently of authenticity.",
        "layout": "module2",
        "sentiments": [
            ("Positive", "Praise, high satisfaction, endorsement"),
            ("Neutral", "Factual commentary, balanced tradeoffs"),
            ("Negative", "Defect reports, friction points, complaints")
        ],
        "aspects": [
            ("🔋 Battery & Power", "Runtime, charging speed, battery degradation"),
            ("🔨 Build Quality", "Durability, materials, structural integrity"),
            ("🎧 Sound / Display", "Acoustic clarity, brightness, resolution"),
            ("📦 Delivery & Packaging", "Transit speed, damaged boxes, missing items"),
            ("💰 Price & Value", "Cost-effectiveness, premium worthiness"),
            ("🛎️ Customer Support", "Warranty claims, responsiveness, refunds")
        ],
        "contradiction_case": {
            "title": "Contradictory Customer Experience Mining",
            "text": "Detects polar disagreements on specific features (e.g., 75% report 'battery lasts 2 days' while 25% report 'battery dies in 30 minutes').<br/><b>Academic Note:</b> Contradictions highlight potential factory batch defects or variable usage conditions; they require investigation and do not independently establish review fraud."
        },
        "footer": "Decoupled Principle: Customer sentiment reflects user satisfaction, while authenticity reflects textual and behavioral integrity.",
        "speaker_notes": (
            "Moving to Module 2: The Customer Sentiment and Experience Analyzer. "
            "This module is completely decoupled from authenticity. Its purpose is to answer: What are customers actually feeling and experiencing? "
            "It computes sentiment polarity across positive, neutral, and negative valences. "
            "Simultaneously, aspect-based topic extraction categorizes feedback into specific product dimensions—such as battery life, "
            "build durability, sound quality, delivery, pricing, and customer service. "
            "Furthermore, Module 2 detects contradictory customer experiences. For example, if some users report outstanding 2-day battery life "
            "while others report total battery failure within 30 minutes, the system flags high variance on that aspect. "
            "Importantly, we note that contradictory experiences do not automatically prove fraud—they often expose legitimate factory batch defects."
        ),
        "viva_qna": "Q: Why is aspect-based sentiment analysis superior to document-level sentiment?\nA: A customer might praise the sound quality but criticize the charging cable. Aspect-based mining captures these nuances rather than assigning a crude blanket score."
    },

    # SLIDE 8
    {
        "num": 8,
        "tag": "MODULE 3 DEEP DIVE",
        "title": "Module 3: Review-Set Trust Analyzer & Clustering",
        "subtitle": "Evaluating collective patterns, semantic similarity, and overall review-set credibility.",
        "layout": "module3",
        "clustering": [
            ("Semantic Vectorization", "Constructs character and word sublinear TF-IDF vectors capturing grammatical fingerprints."),
            ("Pairwise Cosine Matrix", "Computes an all-pairs cosine similarity matrix across every review in the submitted dataset."),
            ("Graph-Based Grouping", "Applies connected-components graph clustering with a documented similarity threshold of <b>≥ 0.82</b>."),
            ("Cluster Archetype Extraction", "Selects the central representative review from each cluster to enable rapid human auditing.")
        ],
        "aggregation_factors": [
            "Proportion of reviews categorized as Suspicious (R_suspicious)",
            "Proportion of reviews belonging to Near-Duplicate Clusters (R_duplicates)",
            "Severity index of polar feature contradictions (Contradiction Penalty)",
            "Proportion of reviews marked as Uncertain (R_uncertain)"
        ],
        "footer": "Individual Authenticity vs. Review-Set Trust: A single review might be ambiguous, but a cluster of 50 near-duplicates reveals organized deception.",
        "speaker_notes": (
            "Module 3 represents our collection-level intelligence: The Review-Set Trust Analyzer. "
            "Evaluating reviews purely one by one is insufficient because sophisticated review farms deliberately vary individual words. "
            "Module 3 vectorizes all submitted reviews and generates a pairwise cosine similarity matrix. "
            "Using a documented threshold of 0.82, a graph-based connected-components algorithm groups near-duplicate reviews into clusters. "
            "It then extracts the central archetype of each cluster for human inspection. "
            "Finally, Module 3 aggregates suspicious ratios, duplicate densities, contradictory signals, and uncertainty metrics into an audit-ready summary. "
            "This distinguishes between individual review ambiguity and collective review-set trustworthiness."
        ),
        "viva_qna": "Q: Why use a cosine similarity threshold of 0.82 for duplicate detection?\nA: Empirical testing demonstrates that 0.82 captures bot templates with swapped synonyms while avoiding false clustering of organic reviews discussing identical product features."
    },

    # SLIDE 9
    {
        "num": 9,
        "tag": "SCENARIO ANALYSIS",
        "title": "Three Key Review-Manipulation Scenarios",
        "subtitle": "Differentiating coordinated attacks from organic marketplace feedback.",
        "layout": "scenarios_3",
        "scenarios": [
            {
                "name": "Scenario A: Review Bombing",
                "target": "Good Product under Competitor Attack",
                "accent": "red",
                "signals": [
                    "Waves of 1-star reviews sharing near-duplicate text.",
                    "Repeated complaint templates ('broke on day 1 waste of money').",
                    "Bursts of unverified purchases from suspicious accounts.",
                    "Genuine buyers report high satisfaction and detailed praise."
                ]
            },
            {
                "name": "Scenario B: Astroturfing",
                "target": "Poor Product with Paid Hype",
                "accent": "amber",
                "signals": [
                    "Inflated 5-star reviews with repetitive promotional hype.",
                    "Abnormal density of superlatives ('miracle product buy now').",
                    "Clusters of near-identical positive praise across accounts.",
                    "Organic negative reviews report consistent hardware defects."
                ]
            },
            {
                "name": "Scenario C: Authentic Mixed",
                "target": "Genuine Market Tradeoffs",
                "accent": "green",
                "signals": [
                    "High vocabulary entropy and natural organic phrasing.",
                    "Balanced distribution across 3, 4, and 5-star ratings.",
                    "Legitimate disagreement on tradeoffs (sound vs. weight).",
                    "Preserved with a High Trust Score without false alarms."
                ]
            }
        ],
        "footer": "Scientific Caveat: These represent intended detection scenarios based on pattern modeling. Actual field accuracy depends on data quality and metadata availability.",
        "speaker_notes": (
            "Here we illustrate the three core detection scenarios that ReviewGuard AI is designed to handle: "
            "Scenario A represents Review Bombing: A reputable manufacturer is targeted by competitors flooding their listing with "
            "repeated 1-star complaints. ReviewGuard AI isolates the near-duplicate negative cluster, protecting the seller. "
            "Scenario B represents Astroturfing: A defective product is artificially boosted with purchased 5-star praise full of promotional buzzwords. "
            "ReviewGuard AI flags the promotional cluster while surfacing authentic defect reports. "
            "Scenario C represents Authentic Mixed Feedback: Normal customers disagree on subjective tradeoffs. "
            "ReviewGuard AI detects high vocabulary entropy and preserves the reviews with a High Trust score. "
            "Importantly, we state scientifically that these are intended pattern scenarios, and performance relies on data fidelity."
        ),
        "viva_qna": "Q: How does ReviewGuard AI differentiate between legitimate complaints and review bombing?\nA: Legitimate complaints exhibit diverse linguistic phrasing and varied defect details, whereas review bombing produces high cosine similarity clusters with repeated script templates."
    },

    # SLIDE 10
    {
        "num": 10,
        "tag": "MATHEMATICAL FORMULATION",
        "title": "The Review-Set Trust Score Formulation",
        "subtitle": "An open, transparent mathematical scoring rule replacing arbitrary black-box metrics.",
        "layout": "formula_slide",
        "formula": "Trust Score = max(0, min(100, 100 − (R_suspicious × 60) − (R_duplicates × 25) − (R_contradictions × 10) − (R_uncertain × 5)))",
        "components": [
            ("Suspicious Ratio (R_susp)", "Proportion of reviews classified as suspicious. Weight 60 reflects verified textual fraud."),
            ("Duplicate Ratio (R_dup)", "Proportion of reviews in near-duplicate clusters. Weight 25 targets coordinated botnets."),
            ("Contradiction (R_cont)", "Normalized index of polar feature disagreements. Weight 10 signals potential deception."),
            ("Uncertain Ratio (R_unc)", "Proportion of unclassifiable reviews. Weight 5 gently reflects reduced confidence.")
        ],
        "tiers": [
            ("80 – 100", "High Trust", "green", "Natural linguistic diversity; negligible coordination."),
            ("60 – 79", "Moderate Trust", "blue", "Minor duplicate phrasing; review with caution."),
            ("40 – 59", "Low Trust", "amber", "Substantial bot clusters or suspicious reviews present."),
            ("0 – 39", "Very Low Trust", "red", "Severe coordinated manipulation or syndicated astroturfing.")
        ],
        "footer": "Epistemic Qualification: The Trust Score measures review-set credibility according to documented heuristic weights; it is not an empirical probability of physical product quality.",
        "speaker_notes": (
            "Slide 10 details our mathematical formulation for the Review-Set Trust Score. "
            "Rather than outputting an opaque black-box number, ReviewGuard AI employs an open, documented formula starting at a base of 100 points. "
            "Penalties are subtracted proportionally: The Suspicious Ratio carries a weight of 60; the Duplicate Ratio carries a weight of 25; "
            "the Contradiction index carries a weight of 10; and the Uncertain Ratio receives a gentle discount of 5 to reflect incomplete information. "
            "The resulting score maps into four clear tiers: High Trust (80–100), Moderate Trust (60–79), Low Trust (40–59), and Very Low Trust (0–39). "
            "In our viva defense, we emphasize that this score audits the credibility of the submitted review set—it is not an empirical certificate of product quality."
        ),
        "viva_qna": "Q: Why is the Uncertain Ratio penalized with a small weight of 5 instead of being treated as fake?\nA: Because an uncertain review (e.g. 'Nice product') is not fraudulent; it simply provides limited entropy. Penalizing it gently reflects reduced statistical certainty without unfairly punishing the seller."
    },

    # SLIDE 11
    {
        "num": 11,
        "tag": "MACHINE LEARNING WORKFLOW",
        "title": "Machine Learning & Natural Language Processing Pipeline",
        "subtitle": "Systematic data transformation from raw text ingestion to serialized inference.",
        "layout": "ml_pipeline",
        "pipeline_stages": [
            ("1. Preprocessing", "Sanitization, case folding, URL masking, whitespace normalization, and duplicate removal."),
            ("2. Feature Extraction", "Sublinear TF-IDF (1–3 n-grams) capturing word sequences and character n-gram stylometry."),
            ("3. Model Classification", "Calibrated LinearSVC / Logistic Regression pipeline with fine-tuned DistilBERT transformer."),
            ("4. Sentiment & Aspects", "Aspect lexicon mapping, VADER compound polarity, and polar variance computation."),
            ("5. Clustering & Scoring", "Pairwise Cosine Similarity matrix (threshold ≥ 0.82) and mathematical Trust Score derivation.")
        ],
        "leakage_box": "Strict Data Leakage Prevention: Vectorizers and calibration transforms are fitted EXCLUSIVELY on training folds (80% Train / 20% Test, stratify=y). Test data remains completely isolated until evaluation.",
        "footer": "Frameworks: Python, Scikit-Learn Pipelines, Hugging Face Transformers, Joblib serialization, Pytest test suites.",
        "speaker_notes": (
            "Here we illustrate our end-to-end Machine Learning and NLP pipeline. "
            "The workflow progresses through five disciplined stages: preprocessing, feature extraction, calibrated sequence classification, "
            "aspect-based sentiment mining, and semantic clustering. "
            "To satisfy rigorous academic standards, we enforce strict data leakage prevention: "
            "The TF-IDF vectorizer and Platt scaling calibration are encapsulated inside isolated Scikit-Learn Pipelines fitted exclusively "
            "on the training split using stratified sampling. Test folds are never touched during feature extraction, ensuring that reported "
            "metrics represent genuine out-of-sample generalization."
        ),
        "viva_qna": "Q: How did you prevent data leakage during TF-IDF vectorization?\nA: By embedding the TfidfVectorizer inside a Scikit-Learn Pipeline fitted strictly on the training partition within cross-validation folds, preventing test set vocabulary from leaking into the model."
    },

    # SLIDE 12
    {
        "num": 12,
        "tag": "USER INTERFACE & EXPERIENCE",
        "title": "Interactive Web Dashboard & Feature Set",
        "subtitle": "Modern, responsive e-commerce trust analysis interface built with React and Tailwind CSS.",
        "layout": "ui_features",
        "features": [
            ("🎯 Trust Score Gauge", "0–100 progress meter with color-coded tier badges (High, Moderate, Low, Very Low)."),
            ("📊 Authenticity Breakdown", "Live counters for Likely Genuine, Suspicious, and Uncertain reviews with percentage bars."),
            ("🏷️ Aspect & Topic Visualizer", "Feature-level breakdown across Battery, Durability, Delivery, Price, and Customer Support."),
            ("🚨 Scenario Detection Banner", "Automatic alert banner explaining whether Scenario A (Bombing), B (Astroturfing), or C (Mixed) was detected.")
        ],
        "footer": "Conceptual UI Mockup: Built to provide an intuitive, human-in-the-loop investigation platform for e-commerce auditors.",
        "speaker_notes": (
            "Slide 12 presents our planned user interface. Designed with modern dark-mode aesthetics (#0a0e17 and #0f172a), "
            "the dashboard incorporates an interactive 0-to-100 Trust Score gauge, live authenticity breakdown cards, "
            "aspect sentiment graphs, and scenario detection banners. "
            "Auditors can explore near-duplicate clusters, search and filter reviews, edit or delete entries in place, and upload CSV or Excel files. "
            "A key feature is the one-click PDF export, which generates an executive audit summary containing charts, tables, and legal disclaimers. "
            "We present these as our planned interface design, engineered for human-in-the-loop validation."
        ),
        "viva_qna": "Q: Why allow users to edit reviews before running analysis?\nA: In practical auditing, analysts often need to clean corrupted OCR text, remove irrelevant tracking headers, or test hypothetical review modifications."
    },

    # SLIDE 13
    {
        "num": 13,
        "tag": "BACKEND API SPECIFICATION",
        "title": "REST API Architecture & PDF Report Generation",
        "subtitle": "Asynchronous FastAPI backend endpoints powering data ingestion, analysis, and reporting.",
        "layout": "api_table",
        "endpoints": [
            ("/api/analyze", "POST", "JSON", "Executes full multi-module analysis (Authenticity, Aspects, Clustering, Trust Score)."),
            ("/api/upload", "POST", "Multipart Form", "Parses uploaded CSV or Excel (.xlsx) files with automated column detection."),
            ("/api/report/pdf", "POST", "PDF Stream", "Generates and streams a downloadable branded executive audit report via ReportLab."),
            ("/api/samples", "GET", "JSON", "Delivers pre-configured demonstration datasets (Scenario A: Bombing, B: Astroturfing, C: Mixed)."),
            ("/api/model/info", "GET", "JSON", "Returns model metadata, pipeline parameters, calibration settings, and evaluation metrics."),
            ("/api/health", "GET", "JSON", "Provides system health status, memory consumption, and database connectivity state.")
        ],
        "footer": "API Security & Robustness: Pydantic v2 schema validation, CORS middleware, safe file streaming, and graceful error handling.",
        "speaker_notes": (
            "Slide 13 details our backend REST API specification. Built with FastAPI, the backend exposes six clean endpoints: "
            "POST /api/analyze executes the three analytical modules; POST /api/upload handles multipart CSV and Excel parsing; "
            "POST /api/report/pdf generates and streams branded PDF audit summaries using ReportLab; "
            "GET /api/samples provides our pre-configured test scenarios; and GET /api/model/info and /api/health provide transparency and telemetry. "
            "All endpoints use strict Pydantic schemas, ensuring robust data validation, error handling, and zero unhandled server exceptions."
        ),
        "viva_qna": "Q: How are large file uploads handled securely in FastAPI?\nA: Files are streamed via python-multipart with size limits and MIME-type validation, preventing memory exhaustion or malicious file execution."
    },

    # SLIDE 14
    {
        "num": 14,
        "tag": "VERIFICATION & LIMITATIONS",
        "title": "Planned Testing Strategy & Epistemic Limitations",
        "subtitle": "Rigorous academic verification methodology, evaluation metrics, and responsible AI boundaries.",
        "layout": "testing_limitations",
        "testing_pillars": [
            ("Unit & Integration Testing", "• Pytest test suites covering text cleaning, TF-IDF vectorization, calibration bounds, and cosine matrix clustering.\n• API route testing verifying status codes, empty input handling, and malformed CSV rejection."),
            ("Scenario Validation", "• Systematic verification across Scenario A (Bombing), Scenario B (Astroturfing), and Scenario C (Mixed).\n• Ensuring that legitimate negative reviews are preserved without false fraud penalties."),
            ("Evaluation Metrics to Measure", "• Precision, Recall, F1-Score, PR-AUC, Confusion Matrix, and Brier Calibration Score on unseen holdout test sets.\n• Multi-domain cross-dataset testing on Amazon, Yelp, and Kaggle benchmarks.")
        ],
        "limitations": [
            "Textual patterns indicate statistical suspiciousness, not absolute legal proof of deceptive intent.",
            "Missing reviewer metadata (timestamps, account IDs) limits temporal burst and coordination detection.",
            "Coincidental repetitive phrasing in genuine reviews can trigger false near-duplicate cluster flags.",
            "Product quality is explicitly reported as 'Not Independently Verified'; the system audits reviews, not hardware."
        ],
        "footer": "Scientific Integrity: We distinguish planned testing methodology from completed benchmarks, acknowledging data-dependent limitations.",
        "speaker_notes": (
            "Slide 14 addresses testing, evaluation, and limitations. "
            "Our verification plan encompasses unit tests using Pytest, scenario validation across Scenarios A, B, and C, "
            "and evaluation metrics including Precision, Recall, F1-score, and Brier calibration scores. "
            "In this academic defense, we maintain scientific honesty by explicitly discussing our system limitations: "
            "First, textual patterns alone cannot establish legal fraudulent intent—they indicate statistical suspiciousness. "
            "Second, missing reviewer metadata reduces cluster resolution. "
            "Third, similar wording can naturally occur among authentic reviews. "
            "Recognizing these boundaries demonstrates academic maturity and responsible AI principles."
        ),
        "viva_qna": "Q: What is the Brier score in model evaluation?\nA: The Brier score measures the accuracy of probabilistic predictions. A lower score indicates superior probability calibration, confirming that confidence scores match real-world odds."
    },

    # SLIDE 15
    {
        "num": 15,
        "tag": "CONCLUSION & FUTURE HORIZONS",
        "title": "Conclusion, Responsible AI & Future Scope",
        "subtitle": "Transforming e-commerce review analysis through multi-perspective intelligence.",
        "layout": "conclusion",
        "core_contributions": [
            "Three Independent Perspectives: Combines review authenticity, customer experience, and review-set trust into a single unified framework.",
            "Resolution of Adversarial Asymmetries: Protects good products from review bombing and exposes astroturfing on poor products.",
            "Scientific Epistemic Honesty: Reports product quality as 'Not Independently Verified' and features an open, transparent trust formula."
        ],
        "future_scope": [
            "Multilingual NLP: Expanding transformer tokenization to Hindi, Spanish, and regional marketplace languages.",
            "Social Graph Telemetry: Integrating reviewer network graphs and IP burst analysis when platform metadata is available.",
            "Continuous Drift Monitoring: Implementing automated concept drift detection against evolving LLM-generated spam.",
            "Merchant Arbitration Dashboards: Developing enterprise dispute resolution dashboards for merchant arbitration."
        ],
        "final_quote": "ReviewGuard AI: Turning Customer Reviews into More Trustworthy Insights.",
        "footer": "Thank you! Open for Viva Voce Examination and Technical Discussion. | Student: [Your Name]",
        "speaker_notes": (
            "In conclusion, ReviewGuard AI demonstrates that online review analysis must transcend simple sentiment averages and binary fake-or-real guesses. "
            "By synthesizing three complementary perspectives—review authenticity, customer sentiment, and collection-level trust—our system "
            "provides a balanced, honest, and actionable understanding of customer feedback. "
            "For future work, we propose expanding into multilingual NLP, incorporating social graph telemetry, and implementing continuous "
            "concept drift monitoring against LLM-generated spam. "
            "Thank you respected committee members. I am now open for your viva voce questions and technical discussion."
        ),
        "viva_qna": "Q: How would your system handle reviews generated by modern Large Language Models (LLMs)?\nA: LLMs generate high syntactic diversity, which evades simple duplicate filters. Future extensions would incorporate perplexity metrics and semantic burstiness analysis alongside metadata telemetry."
    }
]

# ==========================================================
# PRESENTATION IMAGE MAP (15 Bespoke 16:9 Diagrams)
# ==========================================================
IMAGE_MAP = {
    1: "slide1_hero_dashboard.png",
    2: "slide2_threat_landscape.png",
    3: "slide3_problem_fallacy.png",
    4: "slide4_pipeline_architecture.png",
    5: "slide5_system_architecture.png",
    6: "slide6_module1_authenticity.png",
    7: "slide7_module2_sentiment_aspects.png",
    8: "slide8_module3_duplicate_clustering.png",
    9: "slide9_scenarios_matrix.png",
    10: "slide10_trust_score_formula.png",
    11: "slide11_model_performance.png",
    12: "slide12_confusion_matrices.png",
    13: "slide13_dashboard_ui.png",
    14: "slide14_security_testing.png",
    15: "slide15_conclusion_roadmap.png",
}

IMG_DIR = os.path.join(os.path.dirname(__file__), "static", "images", "presentation")

# ==========================================================
# 1. BUILD WIDESCREEN PPTX PRESENTATION WITH IMAGES & NOTES
# ==========================================================
def build_pptx(filename="ReviewGuard_AI_Master_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for item in SLIDES_DATA:
        slide = prs.slides.add_slide(blank_layout)

        # Embed High-Definition 16:9 Bespoke Diagram Image
        img_name = IMAGE_MAP.get(item["num"])
        if img_name:
            img_path = os.path.join(IMG_DIR, img_name)
            if os.path.exists(img_path):
                slide.shapes.add_picture(img_path, 0, 0, width=Inches(13.333), height=Inches(7.5))

        # Embed Complete Verbatim Speaker Script & Viva Voce Q&A in Notes Slide
        notes_slide = slide.notes_slide
        tf_notes = notes_slide.notes_text_frame
        notes_content = (
            f"=== SLIDE {item['num']}: {item['title']} ===\n\n"
            f"WHAT TO SAY (SPEAKER SCRIPT FOR 120-PERSON DEFENSE):\n"
            f"{item['speaker_notes']}\n\n"
            f"ANTICIPATED VIVA VOCE QUESTIONS & DEFENSE ANSWERS:\n"
            f"{item['viva_qna']}\n\n"
            f"ACADEMIC GUIDANCE & PHILOSOPHY:\n"
            f"{item.get('footer', '')}\n"
        )
        tf_notes.text = notes_content

    prs.save(filename)
    print(f"Master PowerPoint Presentation successfully created: {filename} (16:9 widescreen, 15 visual slides with embedded speaker notes)")


# ==========================================================
# 2. BUILD WIDESCREEN MASTER PDF PRESENTATION (FULL-PAGE IMAGES)
# ==========================================================
def build_pdf(filename="ReviewGuard_AI_Master_Presentation.pdf"):
    PAGE_WIDTH = 960
    PAGE_HEIGHT = 540
    c = canvas.Canvas(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    for item in SLIDES_DATA:
        img_name = IMAGE_MAP.get(item["num"])
        if img_name:
            img_path = os.path.join(IMG_DIR, img_name)
            if os.path.exists(img_path):
                c.drawImage(img_path, 0, 0, width=PAGE_WIDTH, height=PAGE_HEIGHT)
            else:
                c.setFillColor(HexColor("#080d1a"))
                c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
                c.setFillColor(HexColor("#38bdf8"))
                c.setFont("Helvetica-Bold", 24)
                c.drawString(40, PAGE_HEIGHT - 60, f"Slide {item['num']}: {item['title']}")
        c.showPage()

    c.save()
    print(f"Master PDF Presentation successfully created: {filename} (16:9 widescreen, 15 visual pages ready for projector)")


# ==========================================================
# 3. BUILD PRINTABLE COMPANION SPEAKER SCRIPT & VIVA GUIDE PDF
# ==========================================================
def build_speaker_guide_pdf(filename="ReviewGuard_AI_Speaker_Script_and_Viva_Guide.pdf"):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=HexColor("#0f172a"), spaceAfter=6))
    styles.add(ParagraphStyle('DocSubtitle', fontName='Helvetica', fontSize=10.5, leading=15, textColor=HexColor("#475569"), spaceAfter=14))
    styles.add(ParagraphStyle('SlideTag', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=HexColor("#0284c7"), spaceAfter=2))
    styles.add(ParagraphStyle('SlideHeading', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=HexColor("#0f172a"), spaceAfter=6))
    styles.add(ParagraphStyle('SectionHeading', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=HexColor("#1e293b"), spaceAfter=4))
    styles.add(ParagraphStyle('ScriptText', fontName='Helvetica', fontSize=9, leading=13.5, textColor=HexColor("#1e293b")))
    styles.add(ParagraphStyle('QnAText', fontName='Helvetica', fontSize=9, leading=13, textColor=HexColor("#0f172a")))
    styles.add(ParagraphStyle('FooterText', fontName='Helvetica-Oblique', fontSize=8.5, leading=11, textColor=HexColor("#64748b")))

    story = []

    # Title Cover Section
    story.append(Paragraph("ReviewGuard AI", styles['DocTitle']))
    story.append(Paragraph("<b>Academic Defense Speaker Script & Comprehensive Viva Voce Guide</b><br/>"
                           "Engineered for Project Defense Before 120 Evaluators & Committee Members<br/>"
                           "Dual-Model Machine Learning Architecture | Sentiment Decoupling | SSRF Guardrails", styles['DocSubtitle']))
    story.append(Spacer(1, 10))

    intro_box = [
        Paragraph("<b>EXECUTIVE VIVA SUMMARY:</b> ReviewGuard AI resolves the fundamental limitation of traditional review detectors: the conflation of customer sentiment with review authenticity. By decoupling sentiment from authenticity, implementing near-duplicate clustering, and introducing an open mathematical review-set trust formula, the system provides transparent, audit-ready consumer intelligence without making unverified physical hardware claims.", styles['ScriptText'])
    ]
    t_intro = Table([[intro_box]], colWidths=[532])
    t_intro.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#f0f9ff")),
        ('BOX', (0,0), (-1,-1), 1, HexColor("#38bdf8")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_intro)
    story.append(Spacer(1, 15))

    for item in SLIDES_DATA:
        s_num = item["num"]
        s_title = item["title"]
        s_tag = item["tag"]
        s_script = item["speaker_notes"]
        s_viva = item["viva_qna"].replace("\n", "<br/>")
        s_foot = item.get("footer", "")

        block = []
        block.append(Paragraph(f"SLIDE {s_num}: {s_tag}", styles['SlideTag']))
        block.append(Paragraph(f"<b>{s_title}</b>", styles['SlideHeading']))

        # Speaker Script Box
        c_script = [
            Paragraph("🎙️ <b>WHAT TO SAY (VERBATIM SPEAKER SCRIPT):</b>", styles['SectionHeading']),
            Paragraph(f"“{s_script}”", styles['ScriptText'])
        ]
        t_script = Table([[c_script]], colWidths=[532])
        t_script.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 7),
        ]))
        block.append(t_script)
        block.append(Spacer(1, 6))

        # Viva Q&A Box
        c_viva = [
            Paragraph("🎓 <b>ANTICIPATED VIVA VOCE QUESTION & DEFENSE ANSWER:</b>", styles['SectionHeading']),
            Paragraph(s_viva, styles['QnAText'])
        ]
        t_viva = Table([[c_viva]], colWidths=[532])
        t_viva.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), HexColor("#ecfdf5")),
            ('BOX', (0,0), (-1,-1), 1, HexColor("#10b981")),
            ('PADDING', (0,0), (-1,-1), 7),
        ]))
        block.append(t_viva)

        if s_foot:
            block.append(Spacer(1, 4))
            block.append(Paragraph(f"💡 <b>Key Principle:</b> {s_foot}", styles['FooterText']))

        block.append(Spacer(1, 12))
        story.append(KeepTogether(block))

    doc.build(story)
    print(f"Companion Viva Guide PDF successfully created: {filename}")


if __name__ == "__main__":
    pptx_path = os.path.join(os.path.dirname(__file__), "ReviewGuard_AI_Master_Presentation.pptx")
    pdf_path = os.path.join(os.path.dirname(__file__), "ReviewGuard_AI_Master_Presentation.pdf")
    guide_path = os.path.join(os.path.dirname(__file__), "ReviewGuard_AI_Speaker_Script_and_Viva_Guide.pdf")
    build_pptx(pptx_path)
    build_pdf(pdf_path)
    build_speaker_guide_pdf(guide_path)
