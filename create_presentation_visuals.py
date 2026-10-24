"""
ReviewGuard AI - Presentation Visuals Generator
===============================================
Generates 15 high-definition, bespoke 16:9 diagram images (one for every presentation slide)
using Matplotlib with modern dark-mode AI aesthetics:
- High contrast for 120-person audience and projector legibility
- Deep navy background (#080d1a), cyan (#38bdf8), indigo (#818cf8), green (#10b981), red (#f43f5e), amber (#f59e0b)
- Crisp technical flowcharts, architecture diagrams, confusion matrices, and metrics
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Rectangle

OUT_DIR = os.path.join(os.path.dirname(__file__), "static", "images", "presentation")
os.makedirs(OUT_DIR, exist_ok=True)

# Theme Palette
C_BG = "#080d1a"
C_CARD = "#0f172a"
C_CARD_BORDER = "#1e293b"
C_CYAN = "#38bdf8"
C_INDIGO = "#818cf8"
C_GREEN = "#10b981"
C_RED = "#f43f5e"
C_AMBER = "#f59e0b"
C_WHITE = "#ffffff"
C_SUB = "#cbd5e1"
C_MUTED = "#64748b"


def setup_figure(title=""):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=140)
    fig.patch.set_facecolor(C_BG)
    ax.set_facecolor(C_BG)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    return fig, ax


def add_rounded_card(ax, x, y, w, h, bg=C_CARD, border=C_CARD_BORDER, lw=1.5, radius=0.25):
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=bg, edgecolor=border, linewidth=lw, zorder=1
    )
    ax.add_patch(rect)
    return rect


# ==============================================================================
# SLIDE 1: Hero Dashboard & Title Visual
# ==============================================================================
def make_slide1():
    fig, ax = setup_figure()
    
    # Outer Frame Card
    add_rounded_card(ax, 0.8, 0.6, 14.4, 7.8, bg="#0d1424", border=C_CYAN, lw=2)
    
    # Header Badge
    ax.text(8, 7.6, "PROJECT DEFENSE & TECHNICAL VIVA VOCE", color=C_CYAN, fontsize=12, fontweight='bold', ha='center', va='center')
    ax.text(8, 6.8, "ReviewGuard AI", color=C_WHITE, fontsize=32, fontweight='heavy', ha='center', va='center')
    ax.text(8, 6.2, "Advanced Fake Product Review Detection & Trust Analysis System", color=C_SUB, fontsize=14, ha='center', va='center')
    
    # Left Card: Candidate Details
    add_rounded_card(ax, 1.4, 1.4, 6.2, 4.2, bg=C_CARD, border="#233554", lw=1.5)
    ax.text(1.8, 5.1, "ACADEMIC PROJECT PROFILE", color=C_CYAN, fontsize=12, fontweight='bold', va='center')
    
    details = [
        ("Candidate Name:", "[Your Name]"),
        ("Department:", "Computer Science & Engineering"),
        ("Project Domain:", "Machine Learning & Natural Language Processing"),
        ("Project Guide:", "[Guide Name]"),
        ("Target Audience:", "120-Person Academic Viva & Project Defense"),
        ("System Architecture:", "Dual-Model NLP Pipeline (CART + SAMME)")
    ]
    for i, (k, v) in enumerate(details):
        y_pos = 4.5 - i * 0.55
        ax.text(1.8, y_pos, k, color=C_MUTED, fontsize=10, fontweight='bold', va='center')
        ax.text(4.2, y_pos, v, color=C_WHITE, fontsize=10, va='center')
        
    # Right Card: Live System Diagnostics Meter
    add_rounded_card(ax, 8.4, 1.4, 6.2, 4.2, bg=C_CARD, border=C_GREEN, lw=1.5)
    ax.text(8.8, 5.1, "OPERATIONAL TRUST TELEMETRY", color=C_GREEN, fontsize=12, fontweight='bold', va='center')
    
    # Trust Score Dial graphic
    wedge_bg = Wedge((11.5, 3.2), 1.4, 0, 180, width=0.35, color="#1e293b", zorder=2)
    wedge_val = Wedge((11.5, 3.2), 1.4, 0, 180 * 0.88, width=0.35, color=C_CYAN, zorder=3)
    ax.add_patch(wedge_bg)
    ax.add_patch(wedge_val)
    ax.text(11.5, 3.2, "88%", color=C_WHITE, fontsize=24, fontweight='heavy', ha='center', va='center')
    ax.text(11.5, 2.7, "Product Trust Score", color=C_SUB, fontsize=10, ha='center', va='center')
    ax.text(11.5, 2.3, "Verified High Trust Level", color=C_GREEN, fontsize=10, fontweight='bold', ha='center', va='center')
    
    # Bottom Pills
    pills = ["Dual-Model Pipeline", "Sentiment Decoupled", "SSRF Protected Scraper", "ReportLab PDF Engine"]
    for i, p in enumerate(pills):
        px = 1.4 + i * 3.4
        add_rounded_card(ax, px, 0.8, 3.0, 0.45, bg="#131e33", border="#233554", lw=1)
        ax.text(px + 1.5, 1.02, p, color=C_CYAN, fontsize=9, fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide1_hero_dashboard.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 2: Threat Landscape Comparison
# ==============================================================================
def make_slide2():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "THE E-COMMERCE REVIEW MANIPULATION CRISIS", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Why Traditional Star Averages Fail Against Coordinated Marketplace Fraud", color=C_SUB, fontsize=12, ha='center', va='center')
    
    cards = [
        {
            "title": "ORGANIC REVIEWS",
            "subtitle": "Authentic Customer Experiences",
            "color": C_GREEN,
            "x": 0.8,
            "items": [
                "Natural vocabulary richness (TTR ~ 0.75+)",
                "Balanced pros and cons (constructive)",
                "Specific experiential nouns & details",
                "Gradual, organic distribution over time",
                "Example: 'Battery lasts 7h, case slightly slippery.'"
            ]
        },
        {
            "title": "5-STAR ASTROTURFING",
            "subtitle": "Paid Sybil Promotion (Inflating Bad Goods)",
            "color": C_AMBER,
            "x": 5.8,
            "items": [
                "Low lexical entropy / template copy",
                "Extreme emotional hyperbole without facts",
                "Excessive punctuation (WOW!!! BEST EVER!!!)",
                "Temporal burst clusters from new accounts",
                "Example: 'AMAZING MIRACLE PRODUCT FIVE STARS BUY!'"
            ]
        },
        {
            "title": "1-STAR REVIEW BOMBING",
            "subtitle": "Competitor Smear Attacks (Damaging Good Goods)",
            "color": C_RED,
            "x": 10.8,
            "items": [
                "Hostile smear templates without product defect facts",
                "Targeted coordinated attack on rival merchants",
                "Zero verified purchase authentication",
                "Drives legitimate sellers out of business",
                "Example: 'CHEATER SCAMMER WORST TRASH DO NOT BUY!'"
            ]
        }
    ]
    
    for c in cards:
        add_rounded_card(ax, c["x"], 1.8, 4.4, 5.4, bg=C_CARD, border=c["color"], lw=2)
        ax.text(c["x"] + 2.2, 6.7, c["title"], color=c["color"], fontsize=13, fontweight='heavy', ha='center', va='center')
        ax.text(c["x"] + 2.2, 6.3, c["subtitle"], color=C_MUTED, fontsize=9, ha='center', va='center')
        
        # separator line
        ax.plot([c["x"] + 0.4, c["x"] + 4.0], [6.0, 6.0], color="#233554", lw=1)
        
        for idx, itm in enumerate(c["items"]):
            y_i = 5.4 - idx * 0.7
            ax.text(c["x"] + 0.4, y_i, f"• {itm}", color=C_WHITE, fontsize=9.5, va='top', wrap=True)

    # Bottom takeaway bar
    add_rounded_card(ax, 0.8, 0.5, 14.4, 0.9, bg="#131e33", border=C_CYAN, lw=1.5)
    ax.text(8, 0.95, "CORE VIVA FINDING: Traditional arithmetic averages treat all 3 categories equally. ReviewGuard AI mathematically separates them.",
            color=C_CYAN, fontsize=10.5, fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide2_threat_landscape.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 3: Problem Fallacy (Sentiment vs Authenticity Decoupling)
# ==============================================================================
def make_slide3():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "THE CONFLATION FALLACY: SENTIMENT VS. AUTHENTICITY", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Addressing the Teacher's Core Challenge: A Good Product with Fake Reviews", color=C_SUB, fontsize=12, ha='center', va='center')
    
    # 2x2 Matrix Cards
    quadrants = [
        {
            "x": 1.0, "y": 4.2, "w": 6.8, "h": 3.1,
            "title": "QUADRANT 1: GENUINE POSITIVE",
            "subtitle": "Authentic Customer Endorsement",
            "color": C_GREEN,
            "desc": "Real buyers praising high-quality products.\n• Features detailed usage facts & natural TTR.\n• Example: 'Earbuds fit snugly, 7h battery life.'\n• System Action: Accepted into Product Trust Index."
        },
        {
            "x": 8.2, "y": 4.2, "w": 6.8, "h": 3.1,
            "title": "QUADRANT 2: FAKE POSITIVE (ASTROTURFING)",
            "subtitle": "Manipulative Promotional Astroturfing",
            "color": C_AMBER,
            "desc": "Inorganic 5-star praise on good OR bad products.\n• Saturated with extreme superlatives & bot templates.\n• Example: 'MIRACLE BEST PRODUCT IN HISTORY 1000%!'\n• System Action: Flagged as Fake; Penalized in Trust Score."
        },
        {
            "x": 1.0, "y": 0.8, "w": 6.8, "h": 3.1,
            "title": "QUADRANT 3: GENUINE NEGATIVE",
            "subtitle": "Constructive Customer Defect Feedback",
            "color": C_CYAN,
            "desc": "Real buyers reporting legitimate product defects.\n• Concrete aspect complaints with balanced wording.\n• Example: 'Screen arrived cracked, RMA took 3 days.'\n• System Action: Retained as Genuine; Vital for seller QA."
        },
        {
            "x": 8.2, "y": 0.8, "w": 6.8, "h": 3.1,
            "title": "QUADRANT 4: FAKE NEGATIVE (SMEAR ATTACK)",
            "subtitle": "Competitor Review Bombing on Good Products",
            "color": C_RED,
            "desc": "Malicious 1-star attack aimed at ruining honest sellers.\n• Hostile hyperbole without verifiable transaction facts.\n• Example: 'SCAMMER CHEATED ME ZERO STARS TRASH!'\n• System Action: Neutralized by ReviewGuard AI to protect seller."
        }
    ]
    
    for q in quadrants:
        add_rounded_card(ax, q["x"], q["y"], q["w"], q["h"], bg=C_CARD, border=q["color"], lw=2)
        ax.text(q["x"] + 0.4, q["y"] + q["h"] - 0.4, q["title"], color=q["color"], fontsize=11, fontweight='heavy', va='top')
        ax.text(q["x"] + 0.4, q["y"] + q["h"] - 0.8, q["subtitle"], color=C_MUTED, fontsize=9, va='top')
        ax.text(q["x"] + 0.4, q["y"] + q["h"] - 1.2, q["desc"], color=C_SUB, fontsize=9, va='top')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide3_problem_fallacy.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 4: End-to-End Pipeline Flow
# ==============================================================================
def make_slide4():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "END-TO-END MULTI-STAGE ANALYSIS PIPELINE", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "From Raw Review Ingestion to Calibrated Machine Learning & Trust Formulation", color=C_SUB, fontsize=12, ha='center', va='center')
    
    stages = [
        ("STAGE 1\nINGESTION", "CSV Dataset Upload\nLive E-Commerce URL\nDirect Text Input\nSSRF Security Filter", C_CYAN),
        ("STAGE 2\nPREPROCESSING", "Unicode Normalization\nTokenization & Regex\nMissing Value Handler\nStratified 80/20 Split", C_INDIGO),
        ("STAGE 3\nFEATURE ENG.", "Sublinear TF-IDF N-Grams\nStylometric Lexical TTR\nExclamation Frequency\nAspect Key Extract", "#38bdf8"),
        ("STAGE 4\nML INFERENCE", "Decision Tree (CART)\nAdaBoost (SAMME)\nCalibrated Probability\nExplainable Keywords", C_AMBER),
        ("STAGE 5\nAUDIT & REPORT", "Collection Trust Score\nDynamic Chart.js Visuals\nSQLite Audit Logging\nReportLab PDF Reports", C_GREEN)
    ]
    
    for i, (st, desc, col) in enumerate(stages):
        x = 0.8 + i * 2.95
        add_rounded_card(ax, x, 2.5, 2.7, 4.6, bg=C_CARD, border=col, lw=2)
        
        # Circle badge
        c = Circle((x + 1.35, 6.3), 0.45, facecolor="#1e293b", edgecolor=col, lw=2, zorder=2)
        ax.add_patch(c)
        ax.text(x + 1.35, 6.3, str(i+1), color=col, fontsize=14, fontweight='heavy', ha='center', va='center', zorder=3)
        
        ax.text(x + 1.35, 5.4, st, color=col, fontsize=11, fontweight='heavy', ha='center', va='center')
        ax.plot([x + 0.3, x + 2.4], [4.7, 4.7], color="#233554", lw=1)
        ax.text(x + 1.35, 4.3, desc, color=C_SUB, fontsize=9.5, ha='center', va='top')
        
        # Arrow connecting stages
        if i < 4:
            ax.annotate("", xy=(x + 2.95, 4.8), xytext=(x + 2.7, 4.8),
                        arrowprops=dict(arrowstyle="->", color=C_CYAN, lw=2))

    # Bottom summary card
    add_rounded_card(ax, 0.8, 0.8, 14.4, 1.2, bg="#131e33", border="#233554", lw=1)
    ax.text(8, 1.4, "ZERO DATA LEAKAGE PROTOCOL: Feature vectorizer is strictly fitted ONLY on the 80% training split.",
            color=C_WHITE, fontsize=11, fontweight='bold', ha='center', va='center')
    ax.text(8, 1.05, "Holdout evaluation remains 100% blind to prevent optimistic validation bias.",
            color=C_MUTED, fontsize=9.5, ha='center', va='center')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide4_pipeline_architecture.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 5: System Architecture Diagram
# ==============================================================================
def make_slide5():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "REVIEWGUARD AI MULTI-TIER SYSTEM ARCHITECTURE", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Decoupled Web Layer, Analytical Processing Core, and Security Guardrails", color=C_SUB, fontsize=12, ha='center', va='center')
    
    tiers = [
        ("TIER 1: PRESENTATION & CLIENT INTERFACE", 
         "Flask Jinja2 Templates  •  Dark Glassmorphism Theme  •  Chart.js Visualizations  •  Responsive Viewport",
         C_CYAN, 6.2),
        ("TIER 2: APPLICATION & ROUTING CONTROLLER", 
         "Flask 3.1 Application Factory  •  21 REST & Web Endpoints  •  CSRF Security  •  SSRF Protection Engine",
         C_INDIGO, 4.5),
        ("TIER 3: ANALYTICAL & MACHINE LEARNING CORE", 
         "TF-IDF Sublinear N-Grams  •  Decision Tree (CART)  •  AdaBoost Classifier  •  Stylometric Extractor",
         C_AMBER, 2.8),
        ("TIER 4: STORAGE & REPORTING INFRASTRUCTURE", 
         "SQLite (reviewguard.db)  •  Joblib Model Serializer  •  ReportLab PDF Engine  •  Training Metadata JSON",
         C_GREEN, 1.1)
    ]
    
    for tname, tdesc, col, y in tiers:
        add_rounded_card(ax, 1.2, y, 13.6, 1.35, bg=C_CARD, border=col, lw=2)
        ax.text(1.6, y + 0.95, tname, color=col, fontsize=11, fontweight='heavy', va='center')
        ax.text(1.6, y + 0.45, tdesc, color=C_WHITE, fontsize=10, va='center')
        
    # Vertical connecting arrows
    for y_a in [5.95, 4.25, 2.55]:
        ax.annotate("", xy=(8.0, y_a), xytext=(8.0, y_a + 0.25),
                    arrowprops=dict(arrowstyle="<->", color=C_CYAN, lw=2))

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide5_system_architecture.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 6: Module 1 — Review Authenticity Detector
# ==============================================================================
def make_slide6():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "MODULE 1: REVIEW AUTHENTICITY CLASSIFIER", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Supervised Learning on Stylometrics & Calibrated Probabilistic Decisions", color=C_SUB, fontsize=12, ha='center', va='center')
    
    # Left: Feature Extraction Box
    add_rounded_card(ax, 1.0, 1.2, 6.8, 6.0, bg=C_CARD, border=C_CYAN, lw=2)
    ax.text(1.4, 6.7, "FEATURE EXTRACTION PIPELINE", color=C_CYAN, fontsize=12, fontweight='bold', va='center')
    
    feats = [
        ("Sublinear TF-IDF 1-2 N-Grams:", "Discounts word frequency bursts; dampens spam repetitions."),
        ("Type-Token Ratio (TTR):", "Measures vocabulary richness. Spammers repeat identical words."),
        ("Average Word Length:", "Synthetic and low-effort bot reviews show lower linguistic depth."),
        ("Exclamation Mark Density:", "Astroturfed reviews use excessive punctuation for artificial hype."),
        ("Sentence Count & Structure:", "Detects unnatural single-run-on phrases typical of botnets.")
    ]
    for idx, (h, d) in enumerate(feats):
        y = 5.8 - idx * 0.95
        ax.text(1.4, y, f"• {h}", color=C_WHITE, fontsize=9.5, fontweight='bold', va='top')
        ax.text(1.6, y - 0.35, d, color=C_MUTED, fontsize=8.5, va='top')
        
    # Right: Classification Output Cards
    add_rounded_card(ax, 8.2, 4.3, 6.8, 2.9, bg="#0d1f18", border=C_GREEN, lw=2)
    ax.text(8.6, 6.7, "PREDICTED GENUINE CLASS (Label 0)", color=C_GREEN, fontsize=11, fontweight='heavy', va='center')
    ax.text(8.6, 6.0, "• Natural linguistic entropy & realistic variance\n• Contains grounded experiential details & balanced tone\n• Posterior Confidence: P(Genuine) >= 50.0%", color=C_SUB, fontsize=9.5, va='top')
    
    add_rounded_card(ax, 8.2, 1.2, 6.8, 2.8, bg="#210e14", border=C_RED, lw=2)
    ax.text(8.6, 3.5, "PREDICTED FAKE CLASS (Label 1)", color=C_RED, fontsize=11, fontweight='heavy', va='center')
    ax.text(8.6, 2.8, "• Template phrase matching & low lexical richness\n• Hyperbolic astroturfed praise or generic hostile smear\n• Posterior Confidence: P(Fake) >= 50.0%", color=C_SUB, fontsize=9.5, va='top')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide6_module1_authenticity.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 7: Module 2 — Sentiment & Aspect Extraction
# ==============================================================================
def make_slide7():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "MODULE 2: CUSTOMER SENTIMENT & ASPECT MINING", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Fine-Grained Feature Satisfaction & Rating-Content Contradiction Detection", color=C_SUB, fontsize=12, ha='center', va='center')
    
    # Left: Aspect Satisfaction Meter
    add_rounded_card(ax, 1.0, 1.2, 6.8, 6.0, bg=C_CARD, border=C_INDIGO, lw=2)
    ax.text(1.4, 6.7, "ASPECT-BASED SENTIMENT POLARITY", color=C_INDIGO, fontsize=12, fontweight='bold', va='center')
    
    aspects = [
        ("Battery Life & Power", 0.82, C_GREEN),
        ("Sound Quality & Bass", 0.91, C_GREEN),
        ("Build & Ergonomics", 0.74, C_GREEN),
        ("Software & Bluetooth Sync", 0.58, C_AMBER),
        ("Shipping & Customer Care", 0.38, C_RED)
    ]
    for i, (asp, score, col) in enumerate(aspects):
        y = 5.7 - i * 0.95
        ax.text(1.4, y, asp, color=C_WHITE, fontsize=9.5, fontweight='bold', va='center')
        ax.text(7.2, y, f"{int(score*100)}%", color=col, fontsize=9.5, fontweight='bold', ha='right', va='center')
        # bar bg
        add_rounded_card(ax, 1.4, y - 0.35, 5.8, 0.22, bg="#1e293b", border="#1e293b", radius=0.1)
        # bar fill
        add_rounded_card(ax, 1.4, y - 0.35, 5.8 * score, 0.22, bg=col, border=col, radius=0.1)
        
    # Right: Contradiction Detection Box
    add_rounded_card(ax, 8.2, 1.2, 6.8, 6.0, bg=C_CARD, border=C_AMBER, lw=2)
    ax.text(8.6, 6.7, "RATING-CONTENT CONTRADICTION ENGINE", color=C_AMBER, fontsize=12, fontweight='bold', va='center')
    
    contradictions = [
        ("5-Star Rating + Negative Text", "Rating: ★★★★★ (5 Stars)\nText: 'Product died on Day 1, seller refused refund.'\nFlag: Contradiction Anomaly (Inadvertent or Sarcastic Bot)"),
        ("1-Star Rating + Glowing Praise", "Rating: ★☆☆☆☆ (1 Star)\nText: 'Best headphones ever, perfect sound, love it!'\nFlag: Inverted Rating Astroturfing Anomaly"),
        ("Aspect Discrepancy", "High overall rating despite multiple critical failures across hardware components.")
    ]
    for i, (h, b) in enumerate(contradictions):
        y = 5.7 - i * 1.6
        add_rounded_card(ax, 8.6, y - 1.1, 6.0, 1.4, bg="#1a1c29", border="#2b3147", radius=0.15)
        ax.text(8.8, y + 0.1, h, color=C_CYAN, fontsize=9.5, fontweight='bold', va='center')
        ax.text(8.8, y - 0.5, b, color=C_SUB, fontsize=8.5, va='center')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide7_module2_sentiment_aspects.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 8: Module 3 — Duplicate Clustering
# ==============================================================================
def make_slide8():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "MODULE 3: NEAR-DUPLICATE CLUSTERING & BOTNETS", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Pairwise Cosine Similarity over TF-IDF Space to Detect Coordinated Campaigns", color=C_SUB, fontsize=12, ha='center', va='center')
    
    # Left: Cosine Similarity Heatmap Matrix
    add_rounded_card(ax, 1.0, 1.2, 6.8, 6.0, bg=C_CARD, border=C_CYAN, lw=2)
    ax.text(1.4, 6.7, "PAIRWISE TF-IDF COSINE SIMILARITY", color=C_CYAN, fontsize=12, fontweight='bold', va='center')
    
    # Simulated 4x4 matrix
    matrix = np.array([
        [1.00, 0.94, 0.89, 0.12],
        [0.94, 1.00, 0.91, 0.15],
        [0.89, 0.91, 1.00, 0.08],
        [0.12, 0.15, 0.08, 1.00]
    ])
    labels = ["Rev #104", "Rev #119", "Rev #142", "Rev #201"]
    
    for row in range(4):
        for col in range(4):
            val = matrix[row, col]
            cell_col = C_RED if val >= 0.85 and row != col else (C_CYAN if row == col else "#1e293b")
            rect = FancyBboxPatch((1.6 + col * 1.4, 5.0 - row * 1.0), 1.2, 0.8,
                                  boxstyle="round,pad=0,rounding_size=0.1",
                                  facecolor=cell_col, edgecolor="#334155", lw=1)
            ax.add_patch(rect)
            ax.text(2.2 + col * 1.4, 5.4 - row * 1.0, f"{val:.2f}", color=C_WHITE, fontsize=10, fontweight='bold', ha='center', va='center')
            
    ax.text(1.6, 1.5, "Threshold theta = 0.85: Identifies Botnet Cluster (Rev 104, 119, 142)", color=C_AMBER, fontsize=9.5, fontweight='bold', va='center')
    
    # Right: Cluster Details
    add_rounded_card(ax, 8.2, 1.2, 6.8, 6.0, bg=C_CARD, border=C_RED, lw=2)
    ax.text(8.6, 6.7, "DETECTED BOT CLUSTER ARCHETYPE (#1)", color=C_RED, fontsize=12, fontweight='bold', va='center')
    
    clones = [
        ("Original Template (#104):", "'Defective item died on day 1 do not buy complete waste of money!!!'"),
        ("Bot Clone A (#119):", "'Defective item died on day 2 do not buy absolute waste of money!!!'"),
        ("Bot Clone B (#142):", "'Defective item broke on day 1 do not buy complete waste of cash!!!'"),
        ("Organic Baseline (#201):", "'Decent battery life but the volume button takes firm pressure.'")
    ]
    for idx, (h, t) in enumerate(clones):
        y = 5.8 - idx * 1.15
        ax.text(8.6, y, h, color=C_AMBER if "Clone" in h or "Template" in h else C_GREEN, fontsize=9.5, fontweight='bold', va='top')
        ax.text(8.6, y - 0.35, t, color=C_WHITE, fontsize=8.5, va='top', wrap=True)
        
    ax.text(8.6, 1.6, "Penalty Deducted in R_duplicates component of Trust Score Formula.", color=C_CYAN, fontsize=9.5, va='center')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide8_module3_duplicate_clustering.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 9: Three Manipulation Scenarios
# ==============================================================================
def make_slide9():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "THREE KEY REVIEW-MANIPULATION SCENARIOS", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Addressing Concrete Marketplace Fraud Tactics Detected by ReviewGuard AI", color=C_SUB, fontsize=12, ha='center', va='center')
    
    scenarios = [
        {
            "x": 0.8, "title": "SCENARIO A: REVIEW BOMBING",
            "tag": "Smear Campaign on Good Products",
            "col": C_RED,
            "pts": [
                "Target: Legitimate high-quality merchant",
                "Attacker: Competitor syndicates / botnets",
                "Tactic: Flood product with 1-star reviews",
                "Linguistic Marker: Hostile generic copy",
                "ReviewGuard Solution: Flags smear burst; preserves genuine merchant rating."
            ]
        },
        {
            "x": 5.8, "title": "SCENARIO B: ASTROTURFING",
            "tag": "Inorganic 5-Star Rating Hype",
            "col": C_AMBER,
            "pts": [
                "Target: Inferior or deceptive product",
                "Attacker: Shady seller purchasing reviews",
                "Tactic: Buy hundred 5-star generic praises",
                "Linguistic Marker: Extreme superlatives (WOW)",
                "ReviewGuard Solution: Deducts promotional bias; alerts prospective buyers."
            ]
        },
        {
            "x": 10.8, "title": "SCENARIO C: AUTHENTIC NUANCE",
            "tag": "Organic Customer Disagreement",
            "col": C_GREEN,
            "pts": [
                "Target: Normal commercial merchandise",
                "Attacker: None (Real human customers)",
                "Tactic: Diverse genuine opinions & ratings",
                "Linguistic Marker: High TTR & specific facts",
                "ReviewGuard Solution: Authenticates mixed reviews; computes true trust."
            ]
        }
    ]
    
    for s in scenarios:
        add_rounded_card(ax, s["x"], 1.2, 4.4, 6.0, bg=C_CARD, border=s["col"], lw=2)
        ax.text(s["x"] + 2.2, 6.7, s["title"], color=s["col"], fontsize=12, fontweight='heavy', ha='center', va='center')
        ax.text(s["x"] + 2.2, 6.25, s["tag"], color=C_MUTED, fontsize=9, ha='center', va='center')
        ax.plot([s["x"] + 0.4, s["x"] + 4.0], [5.95, 5.95], color="#233554", lw=1)
        
        for idx, p in enumerate(s["pts"]):
            ax.text(s["x"] + 0.4, 5.4 - idx * 0.85, f"• {p}", color=C_WHITE, fontsize=9.2, va='top', wrap=True)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide9_scenarios_matrix.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 10: Mathematical Trust Score Formulation
# ==============================================================================
def make_slide10():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "REVIEW-SET TRUST SCORE MATHEMATICAL FORMULATION", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Transparent Collection-Level Trust Index with Multi-Factor Penalty Weights", color=C_SUB, fontsize=12, ha='center', va='center')
    
    # Formula Box Banner
    add_rounded_card(ax, 1.2, 5.8, 13.6, 1.5, bg="#0d1f2d", border=C_CYAN, lw=2)
    ax.text(8, 6.75, r"$T = \max\left(0,\, 100 - (\alpha \cdot R_{\mathrm{fake}} + \beta \cdot R_{\mathrm{dup}} + \gamma \cdot R_{\mathrm{contra}})\right)$",
            color=C_CYAN, fontsize=20, fontweight='heavy', ha='center', va='center')
    ax.text(8, 6.15, "Where alpha = 0.50 (Fake Ratio), beta = 0.30 (Duplicate Cluster Ratio), gamma = 0.20 (Rating Contradiction Ratio)",
            color=C_WHITE, fontsize=10.5, ha='center', va='center')
    
    # 4 Trust Tiers Cards
    tiers = [
        ("TIER 1: HIGH TRUST", "Score: 75% - 100%", C_GREEN, "Predominantly organic reviews with authentic linguistic markers. Safe purchase recommendation.", 1.2),
        ("TIER 2: MODERATE TRUST", "Score: 50% - 74%", C_CYAN, "Mild duplication or isolated anomalies. Mostly reliable with minor promotional noise.", 4.7),
        ("TIER 3: LOW TRUST", "Score: 25% - 49%", C_AMBER, "Substantial promotional astroturfing or detected botnet review-bombing clusters.", 8.2),
        ("TIER 4: CRITICAL ANOMALY", "Score: 0% - 24%", C_RED, "Severe coordinated fraud. Extreme duplicate density and ungrounded review manipulation.", 11.7)
    ]
    for ttitle, trange, col, tdesc, x in tiers:
        add_rounded_card(ax, x, 1.2, 3.2, 4.2, bg=C_CARD, border=col, lw=2)
        ax.text(x + 1.6, 5.0, ttitle, color=col, fontsize=10.5, fontweight='heavy', ha='center', va='center')
        ax.text(x + 1.6, 4.5, trange, color=C_WHITE, fontsize=11, fontweight='bold', ha='center', va='center')
        ax.plot([x + 0.3, x + 2.9], [4.1, 4.1], color="#233554", lw=1)
        ax.text(x + 1.6, 3.6, tdesc, color=C_SUB, fontsize=9, ha='center', va='top', wrap=True)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide10_trust_score_formula.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 11: Machine Learning Model Performance
# ==============================================================================
def make_slide11():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "EMPIRICAL MODEL EVALUATION: DECISION TREE VS ADABOOST", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Evaluated on 180 Holdout Test Samples (Stratified 80/20 Partitioning)", color=C_SUB, fontsize=12, ha='center', va='center')
    
    # Left: Comparative Bar Chart
    add_rounded_card(ax, 1.0, 1.2, 8.4, 6.0, bg=C_CARD, border=C_CYAN, lw=2)
    ax.text(5.2, 6.7, "PERFORMANCE METRICS COMPARISON (TEST SPLIT)", color=C_CYAN, fontsize=12, fontweight='bold', ha='center', va='center')
    
    metrics = ["Accuracy", "Precision (Fake)", "Recall (Fake)", "F1-Score (Fake)"]
    dt_vals = [98.89, 100.0, 94.12, 96.97]
    ada_vals = [98.89, 100.0, 94.12, 96.97]
    
    y_indices = np.arange(len(metrics))
    bar_h = 0.28
    
    for i, (m, dt_v, ada_v) in enumerate(zip(metrics, dt_vals, ada_vals)):
        y_pos = 5.6 - i * 1.1
        ax.text(1.4, y_pos + 0.2, m, color=C_WHITE, fontsize=10, fontweight='bold', va='center')
        
        # DT Bar
        add_rounded_card(ax, 3.8, y_pos - 0.05, 5.2 * (dt_v/100), bar_h, bg=C_INDIGO, border=C_INDIGO, radius=0.08)
        ax.text(3.8 + 5.2 * (dt_v/100) + 0.15, y_pos + 0.08, f"DT: {dt_v:.1f}%", color=C_INDIGO, fontsize=9, fontweight='bold', va='center')
        
        # AdaBoost Bar
        add_rounded_card(ax, 3.8, y_pos - 0.40, 5.2 * (ada_v/100), bar_h, bg=C_GREEN, border=C_GREEN, radius=0.08)
        ax.text(3.8 + 5.2 * (ada_v/100) + 0.15, y_pos - 0.26, f"Ada: {ada_v:.1f}%", color=C_GREEN, fontsize=9, fontweight='bold', va='center')

    # Right: Operational Summary Card
    add_rounded_card(ax, 9.8, 1.2, 5.2, 6.0, bg=C_CARD, border=C_GREEN, lw=2)
    ax.text(12.4, 6.7, "OPERATIONAL VERDICT", color=C_GREEN, fontsize=12, fontweight='heavy', ha='center', va='center')
    
    verdicts = [
        ("Zero False Positives:", "Precision is 100%, ensuring no authentic customer review is wrongly marked fake."),
        ("High Detection Sensitivity:", "Recall is 94.12%, capturing subtle astroturfed promotional spam."),
        ("Ultra-Low Latency:", "Decision Tree fit time: 0.038s\nAdaBoost fit time: 0.280s\nInference latency < 2.5ms/review."),
        ("Ensemble Stability:", "AdaBoost (SAMME) iteratively reweights boundary samples for robust generalization.")
    ]
    for idx, (h, d) in enumerate(verdicts):
        y = 5.7 - idx * 1.25
        ax.text(10.2, y, h, color=C_CYAN, fontsize=10, fontweight='bold', va='top')
        ax.text(10.2, y - 0.35, d, color=C_SUB, fontsize=8.8, va='top', wrap=True)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide11_model_performance.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 12: Confusion Matrices
# ==============================================================================
def make_slide12():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "CONFUSION MATRIX & ERROR COST ANALYSIS", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Evaluating Type I vs. Type II Errors on N = 180 Test Review Instances", color=C_SUB, fontsize=12, ha='center', va='center')
    
    # Left Matrix: Decision Tree
    add_rounded_card(ax, 1.0, 1.2, 6.8, 6.0, bg=C_CARD, border=C_INDIGO, lw=2)
    ax.text(4.4, 6.7, "MODEL A: DECISION TREE MATRIX", color=C_INDIGO, fontsize=11.5, fontweight='bold', ha='center', va='center')
    
    # Grid 2x2
    # TN=146, FP=0, FN=2, TP=32
    cells = [
        (1.5, 4.3, "TRUE NEGATIVE (TN)\n146 Reviews\n(Correct Genuine)", C_GREEN),
        (4.5, 4.3, "FALSE POSITIVE (FP)\n0 Reviews\n(Zero False Alarms!)", C_CYAN),
        (1.5, 2.0, "FALSE NEGATIVE (FN)\n2 Reviews\n(Undetected Bot)", C_AMBER),
        (4.5, 2.0, "TRUE POSITIVE (TP)\n32 Reviews\n(Correct Fake Caught)", C_GREEN)
    ]
    for cx, cy, lbl, col in cells:
        add_rounded_card(ax, cx, cy, 2.8, 1.8, bg="#131e33", border=col, lw=1.5)
        ax.text(cx + 1.4, cy + 0.9, lbl, color=C_WHITE, fontsize=9.5, fontweight='bold', ha='center', va='center')
        
    # Right Matrix: AdaBoost Classifier
    add_rounded_card(ax, 8.2, 1.2, 6.8, 6.0, bg=C_CARD, border=C_GREEN, lw=2)
    ax.text(11.6, 6.7, "MODEL B: ADABOOST ENSEMBLE MATRIX", color=C_GREEN, fontsize=11.5, fontweight='bold', ha='center', va='center')
    
    cells_ada = [
        (8.7, 4.3, "TRUE NEGATIVE (TN)\n146 Reviews\n(Correct Genuine)", C_GREEN),
        (11.7, 4.3, "FALSE POSITIVE (FP)\n0 Reviews\n(Zero False Alarms!)", C_CYAN),
        (8.7, 2.0, "FALSE NEGATIVE (FN)\n2 Reviews\n(Borderline Case)", C_AMBER),
        (11.7, 2.0, "TRUE POSITIVE (TP)\n32 Reviews\n(Correct Fake Caught)", C_GREEN)
    ]
    for cx, cy, lbl, col in cells_ada:
        add_rounded_card(ax, cx, cy, 2.8, 1.8, bg="#131e33", border=col, lw=1.5)
        ax.text(cx + 1.4, cy + 0.9, lbl, color=C_WHITE, fontsize=9.5, fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide12_confusion_matrices.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 13: Dashboard UI & Feature Set
# ==============================================================================
def make_slide13():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "INTERACTIVE WEB APPLICATION & OPERATIONAL DASHBOARD", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Designed for Teachers, Project Evaluators, and Commercial Auditing", color=C_SUB, fontsize=12, ha='center', va='center')
    
    # Left: UI Wireframe Simulation
    add_rounded_card(ax, 1.0, 1.2, 8.6, 6.0, bg="#0d1424", border=C_CYAN, lw=2)
    ax.text(1.4, 6.7, "REVIEWGUARD AI LIVE INTERFACE (PORT 5000)", color=C_CYAN, fontsize=11, fontweight='bold', va='center')
    
    # Mini stats row
    m_stats = [("Total Reviews", "899"), ("Genuine", "731"), ("Fake Flagged", "168"), ("Trust Index", "88%")]
    for idx, (st, sv) in enumerate(m_stats):
        add_rounded_card(ax, 1.4 + idx * 1.95, 5.3, 1.8, 0.9, bg=C_CARD, border="#233554", lw=1)
        ax.text(1.4 + idx * 1.95 + 0.9, 5.85, sv, color=C_WHITE, fontsize=12, fontweight='bold', ha='center', va='center')
        ax.text(1.4 + idx * 1.95 + 0.9, 5.5, st, color=C_MUTED, fontsize=8, ha='center', va='center')
        
    # Table mockup
    add_rounded_card(ax, 1.4, 1.6, 7.8, 3.4, bg=C_CARD, border="#233554", lw=1)
    ax.text(1.6, 4.6, "ID   REVIEW EXCERPT                            RATING   VERDICT   CONFIDENCE", color=C_CYAN, fontsize=8.5, fontweight='bold', va='center')
    ax.plot([1.6, 9.0], [4.4, 4.4], color="#233554", lw=1)
    
    rows = [
        ("#1", "Purchased headset 2w ago, battery lasts 18h...", "★ 5.0", "Genuine", "88.1%", C_GREEN),
        ("#2", "BEST PRODUCT IN WORLD FIVE STARS BUY NOW...", "★ 5.0", "Fake", "88.1%", C_RED),
        ("#3", "WORST TRASH BROKE IMMEDIATELY SCAM SELLER...", "★ 1.0", "Fake", "78.0%", C_RED),
        ("#4", "Keyboard keys feel tactile, backlight is soft...", "★ 4.0", "Genuine", "75.4%", C_GREEN)
    ]
    for i, (rid, txt, rat, verd, conf, col) in enumerate(rows):
        y_r = 4.0 - i * 0.65
        ax.text(1.6, y_r, f"{rid:<4} {txt:<38} {rat:<8}", color=C_WHITE, fontsize=8, va='center')
        ax.text(7.2, y_r, verd, color=col, fontsize=8, fontweight='bold', va='center')
        ax.text(8.4, y_r, conf, color=C_SUB, fontsize=8, va='center')

    # Right: Key System Modules
    add_rounded_card(ax, 10.0, 1.2, 5.0, 6.0, bg=C_CARD, border=C_GREEN, lw=2)
    ax.text(12.5, 6.7, "OPERATIONAL MODULES", color=C_GREEN, fontsize=12, fontweight='heavy', ha='center', va='center')
    
    mods = [
        ("Single Review Predictor:", "Instant inference with top TF-IDF keywords & stylometric breakdown."),
        ("Live URL Scanner:", "Scrapes Flipkart, Amazon, and public stores with SSRF security."),
        ("Teacher Viva Presets:", "1-click testing of Astroturfing, Smear attacks, and Genuine nuance."),
        ("Automated PDF Hub:", "Generates formal IEEE certificates and URL audit reports.")
    ]
    for idx, (h, d) in enumerate(mods):
        y = 5.7 - idx * 1.25
        ax.text(10.4, y, f"• {h}", color=C_CYAN, fontsize=9.5, fontweight='bold', va='top')
        ax.text(10.4, y - 0.35, d, color=C_SUB, fontsize=8.8, va='top', wrap=True)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide13_dashboard_ui.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 14: SSRF Security & Testing
# ==============================================================================
def make_slide14():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "SSRF SECURITY GUARDRAILS & ROBUSTNESS TESTING", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "Enterprise-Grade URL Security Shield Protecting Internal Private Subnets", color=C_SUB, fontsize=12, ha='center', va='center')
    
    # Left: SSRF Decision Flow
    add_rounded_card(ax, 1.0, 1.2, 6.8, 6.0, bg=C_CARD, border=C_RED, lw=2)
    ax.text(1.4, 6.7, "SSRF DEFENSE ARCHITECTURE", color=C_RED, fontsize=12, fontweight='bold', va='center')
    
    steps = [
        ("Step 1: URL Parse & Protocol Check", "Only HTTP/HTTPS permitted; rejects file://, gopher://, ftp://"),
        ("Step 2: DNS Hostname Resolution", "Resolves destination domain to underlying IP address."),
        ("Step 3: Private Subnet Rejection", "Strictly BLOCKS 127.0.0.1, 10.0.0.0/8, 192.168.0.0/16, 172.16.0.0/12"),
        ("Step 4: Cloud Metadata Shield", "Blocks AWS/GCP internal metadata IP (169.254.169.254)."),
        ("Step 5: Timeout & Payload Caps", "Capped at 5s timeout & 2MB response to prevent ReDoS / OOM.")
    ]
    for idx, (h, d) in enumerate(steps):
        y = 5.8 - idx * 0.95
        ax.text(1.4, y, f"• {h}", color=C_WHITE, fontsize=9.5, fontweight='bold', va='top')
        ax.text(1.6, y - 0.35, d, color=C_SUB, fontsize=8.5, va='top')
        
    # Right: Testing Strategy & Verification
    add_rounded_card(ax, 8.2, 1.2, 6.8, 6.0, bg=C_CARD, border=C_GREEN, lw=2)
    ax.text(8.6, 6.7, "VERIFICATION & TESTING OUTCOMES", color=C_GREEN, fontsize=12, fontweight='bold', va='center')
    
    t_tests = [
        ("17/17 Automated Unit Tests Passing:", "Covers text normalization, stylometrics, model inference, and routes."),
        ("19/19 End-to-End Verification Checkpoints:", "Tests server liveness, live URL scraping, database persistence, and PDF creation."),
        ("Active Attack Injection Verified:", "Probed with http://127.0.0.1:8080/admin -> Safely blocked with HTTP 200 security alert."),
        ("Stratified Split Validation:", "Guarantees equal class distribution (80% train / 20% test).")
    ]
    for idx, (h, d) in enumerate(t_tests):
        y = 5.8 - idx * 1.2
        ax.text(8.6, y, f"✔ {h}", color=C_CYAN, fontsize=9.5, fontweight='bold', va='top')
        ax.text(8.9, y - 0.35, d, color=C_SUB, fontsize=8.8, va='top', wrap=True)

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide14_security_testing.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


# ==============================================================================
# SLIDE 15: Conclusion & Future Scope
# ==============================================================================
def make_slide15():
    fig, ax = setup_figure()
    
    ax.text(8, 8.2, "CONCLUSION, ACADEMIC CONTRIBUTIONS & FUTURE ROADMAP", color=C_CYAN, fontsize=18, fontweight='heavy', ha='center', va='center')
    ax.text(8, 7.7, "ReviewGuard AI: A Teacher-Ready, Production-Grade Review Trust Framework", color=C_SUB, fontsize=12, ha='center', va='center')
    
    # Left: Key Contributions
    add_rounded_card(ax, 1.0, 1.4, 6.8, 5.8, bg=C_CARD, border=C_CYAN, lw=2)
    ax.text(1.4, 6.7, "CORE ACADEMIC CONTRIBUTIONS", color=C_CYAN, fontsize=12, fontweight='bold', va='center')
    
    contribs = [
        ("Decoupled Multi-Perspective NLP:", "Breaks the flaw in binary detectors by separating review sentiment from review authenticity."),
        ("High-Accuracy Ensemble Classifiers:", "AdaBoost & Decision Tree pipelines achieving 98.89% test accuracy with zero data leakage."),
        ("Mathematical Review-Set Trust Scoring:", "Formulates a transparent, reproducible index balancing fake reviews, bot duplicates, and rating contradictions."),
        ("Open-Access IEEE Architecture:", "Complete teacher-ready web platform with interactive Chart.js graphs, SSRF protection, and ReportLab PDF reports.")
    ]
    for idx, (h, d) in enumerate(contribs):
        y = 5.9 - idx * 1.25
        ax.text(1.4, y, f"✔ {h}", color=C_GREEN, fontsize=10, fontweight='bold', va='top')
        ax.text(1.6, y - 0.35, d, color=C_SUB, fontsize=8.8, va='top', wrap=True)

    # Right: Future Scope & Roadmap
    add_rounded_card(ax, 8.2, 1.4, 6.8, 5.8, bg=C_CARD, border=C_INDIGO, lw=2)
    ax.text(8.6, 6.7, "TARGETED FUTURE IMPROVEMENTS", color=C_INDIGO, fontsize=12, fontweight='bold', va='center')
    
    future = [
        ("DistilBERT Transformer Fine-Tuning:", "Integrate lightweight transformer attention heads for subtle semantic context understanding."),
        ("Multi-Modal Image Review Verification:", "Cross-reference customer photo uploads against merchant product catalogs using computer vision."),
        ("Graph-Based Reviewer Syndicate Mining:", "Deploy Graph Neural Networks (GNNs) across user IDs and IP addresses to dismantle organized review fraud rings."),
        ("Browser Extension Integration:", "Deploy ReviewGuard AI as a Chrome extension for real-time browsing trust analysis on Amazon and Flipkart.")
    ]
    for idx, (h, d) in enumerate(future):
        y = 5.9 - idx * 1.25
        ax.text(8.6, y, f"🚀 {h}", color=C_CYAN, fontsize=10, fontweight='bold', va='top')
        ax.text(8.9, y - 0.35, d, color=C_SUB, fontsize=8.8, va='top', wrap=True)

    # Bottom Quote
    ax.text(8, 0.8, "“The goal of AI in e-commerce is not to silence criticism, but to protect marketplace truth.”",
            color=C_GREEN, fontsize=11, fontweight='bold', style='italic', ha='center', va='center')

    plt.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "slide15_conclusion_roadmap.png"), facecolor=C_BG, edgecolor='none')
    plt.close(fig)


def generate_all_presentation_images():
    print("Generating 15 high-definition visual diagrams for ReviewGuard AI presentation...")
    make_slide1()
    print("[OK] Slide 1 image generated")
    make_slide2()
    print("[OK] Slide 2 image generated")
    make_slide3()
    print("[OK] Slide 3 image generated")
    make_slide4()
    print("[OK] Slide 4 image generated")
    make_slide5()
    print("[OK] Slide 5 image generated")
    make_slide6()
    print("[OK] Slide 6 image generated")
    make_slide7()
    print("[OK] Slide 7 image generated")
    make_slide8()
    print("[OK] Slide 8 image generated")
    make_slide9()
    print("[OK] Slide 9 image generated")
    make_slide10()
    print("[OK] Slide 10 image generated")
    make_slide11()
    print("[OK] Slide 11 image generated")
    make_slide12()
    print("[OK] Slide 12 image generated")
    make_slide13()
    print("[OK] Slide 13 image generated")
    make_slide14()
    print("[OK] Slide 14 image generated")
    make_slide15()
    print("[OK] Slide 15 image generated")
    print(f"\nAll 15 slide diagram images successfully saved in: {OUT_DIR}")


if __name__ == "__main__":
    generate_all_presentation_images()
