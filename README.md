# Advanced Fake Product Review Detection Using Machine Learning
### ReviewGuard AI — IEEE-Style Final Year Academic Project

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.0-green.svg)](https://flask.palletsprojects.com/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%2F%20SQLAlchemy-blueviolet.svg)](https://www.sqlite.org/)
[![Reports](https://img.shields.io/badge/PDF%20Engine-ReportLab-red.svg)](https://www.reportlab.com/)
[![Security](https://img.shields.io/badge/Security-SSRF%20%2B%20CSRF%20Protected-brightgreen.svg)]()

> **ReviewGuard AI** is an intelligent web-based machine learning application engineered to distinguish between authentic consumer feedback and deceptive computer-generated/manipulated product reviews. The system fundamentally decouples **customer sentiment** from **review authenticity**, ensuring positive feedback is not blindly assumed genuine and negative criticism is not automatically dismissed as fraud.

---

## 📋 Table of Contents

1. [Project Overview & Key Highlights](#-project-overview--key-highlights)
2. [System Architecture & Data Flow](#-system-architecture--data-flow)
3. [Machine Learning Algorithms & Mathematical Foundations](#-machine-learning-algorithms--mathematical-foundations)
4. [Technology Stack](#-technology-stack)
5. [Project Directory Layout](#-project-directory-layout)
6. [Installation & Setup Instructions](#-installation--setup-instructions)
7. [Running the Application](#-running-the-application)
8. [Teacher & Evaluator Demonstration Guide](#-teacher--evaluator-demonstration-guide)
9. [Modules & Feature Walkthrough](#-modules--feature-walkthrough)
10. [REST API Documentation](#-rest-api-documentation)
11. [Security Architecture (SSRF & CSRF Guardrails)](#-security-architecture)
12. [Automated Testing Suite](#-automated-testing-suite)
13. [Academic Deliverables & Viva Voce Q&A](#-academic-deliverables--viva-voce-qa)

---

## 🌟 Project Overview & Key Highlights

* **Decoupled Sentiment & Authenticity**: A positive review is not automatically genuine, and a negative review is not automatically fake. An authentic product can suffer coordinated fake negative smear campaigns from competitors, while poor products can receive artificially purchased 5-star praise.
* **Supervised Machine Learning Pipeline**: Evaluates and compares two primary classifiers:
  1. **Decision Tree Classifier (CART)** — Highly interpretable rule-based splitting utilizing Gini Impurity.
  2. **AdaBoost Classifier (SAMME)** — Iterative ensemble boosting focusing sequential weak learners on deceptive linguistic nuances.
* **Zero Data Leakage**: Standardized `TfidfVectorizer` and classifiers are bundled inside scikit-learn `Pipeline` objects fitted strictly on the 80% training split.
* **Stylometric & Linguistic Feature Engineering**: Computes vocabulary richness (Type-Token Ratio), average sentence length, punctuation densities (exclamation and question marks), and n-gram lexical diversity.
* **Policy-Compliant Live URL Analysis**: Safely extracts customer reviews from live public pages and demo e-commerce mock stores with strict **Server-Side Request Forgery (SSRF)** prevention blocking loopback and private subnets.
* **Automated PDF Report Generation**: Generates formal, IEEE-style downloadable PDF certificates for individual predictions, comparative model benchmarks, and URL audit sessions using ReportLab.
* **Role-Based Authentication**: Secure session authentication featuring salted password hashing via Werkzeug, protected routes, and CSRF token verification on all mutation endpoints.

---

## 🏗️ System Architecture & Data Flow

```
                                [ User / Web Browser ]
                                          │
                        HTTP(S) Requests  │  CSRF Token Protected
                                          ▼
                      ┌─────────────────────────────────────────┐
                      │            Flask Web Server             │
                      │  - Session Authentication & RBAC        │
                      │  - Route Dispatcher & Error Handlers    │
                      └───────────────────┬─────────────────────┘
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            ▼                             ▼                             ▼
   [ Dataset Ingestion ]         [ Single / Batch ML ]        [ Safe URL Scraper ]
    - CSV Upload & Validation     - Pipeline Inference         - SSRF IP Verification
    - Schema Normalization        - Calibrated Probabilities   - 2MB / 5s Timeout Cap
    - Deduplication (0 Leakage)   - Salient N-Gram Extraction  - DOM Review Parsing
            │                             │                             │
            ▼                             ▼                             ▼
  ┌───────────────────┐         ┌───────────────────┐         ┌───────────────────┐
  │  SQLite Database  │         │  Model Artifacts  │         │ ReportLab Engine  │
  │ - Users & Roles   │         │ - Decision Tree   │         │ - NumberedCanvas  │
  │ - Audit History   │         │ - AdaBoost Model  │         │ - Dynamic Charts  │
  │ - Dataset Meta    │         │ - JSON Metadata   │         │ - PDF Certificate │
  └───────────────────┘         └───────────────────┘         └───────────────────┘
```

---

## 📐 Machine Learning Algorithms & Mathematical Foundations

### 1. TF-IDF Vectorization (Term Frequency - Inverse Document Frequency)
Text reviews are converted into numerical feature vectors using sublinear term-frequency scaling and n-gram tokenization ($1 \le n \le 2$):

$$\text{TF}(t, d) = 1 + \log(f_{t, d}) \quad \text{for } f_{t, d} > 0$$

$$\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

Vectors are subsequently normalized to unit Euclidean length ($\ell_2$-norm) to eliminate text length bias.

### 2. Decision Tree Classifier (CART)
The Decision Tree builds an interpretable binary tree using **Gini Impurity** to measure node purity:

$$I_G(p) = 1 - \sum_{i=0}^{1} p_i^2 = 1 - (p_{\text{genuine}}^2 + p_{\text{fake}}^2)$$

At each internal node, the feature and split threshold that maximize Information Gain are chosen:

$$\Delta I_G = I_G(D) - \frac{|D_{\text{left}}|}{|D|} I_G(D_{\text{left}}) - \frac{|D_{\text{right}}|}{|D|} I_G(D_{\text{right}})$$

### 3. AdaBoost Classifier (Adaptive Boosting)
AdaBoost sequentially combines $M$ weak decision tree estimators $h_m(x)$ into an ensemble hypothesis $H(x)$:

$$H(x) = \text{sign}\left(\sum_{m=1}^{M} \alpha_m h_m(x)\right)$$

Where estimator weight $\alpha_m$ is determined by its weighted error rate $\epsilon_m$:

$$\alpha_m = \frac{1}{2} \ln\left(\frac{1 - \epsilon_m}{\epsilon_m}\right)$$

Sample weights $w_i$ are updated adaptively after each round, exponentially penalizing misclassifications:

$$w_i^{(m+1)} = w_i^{(m)} \exp\left(-\alpha_m y_i h_m(x_i)\right)$$

This forces subsequent estimators to concentrate specifically on subtle linguistic deception patterns that simpler classifiers fail to discern.

---

## 💻 Technology Stack

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Language** | Python | 3.10+ | Core programming and data pipelines |
| **Framework** | Flask | 3.0+ | WSGI web application server & REST routing |
| **Machine Learning** | Scikit-learn | 1.4+ | Vectorization, pipelines, DT, and AdaBoost |
| **Data Processing** | Pandas & NumPy | Latest | Tabular data manipulation and array math |
| **Database** | SQLite & SQLAlchemy | Latest | Relational audit log, user auth, dataset metadata |
| **Form & CSRF Security**| Flask-WTF / WTForms | Latest | CSRF token protection and secure inputs |
| **PDF Generation** | ReportLab | 4.0+ | Multi-page academic reports with headers/footers |
| **Visualization** | Chart.js & Matplotlib | Latest | Dynamic dashboard charts & headless static figures |
| **Web Scraping** | Requests & BeautifulSoup4 | Latest | Policy-compliant live DOM parsing with SSRF defense |
| **Model Persistence** | Joblib | Latest | Fast serialized pipeline caching and retrieval |

---

## 📂 Project Directory Layout

```text
fake-review-detector/
│
├── dataset/
│   ├── sample_reviews.csv         # Standardized 1,600-sample balanced benchmark dataset
│   └── README.md                  # Dataset schema documentation & label mappings
│
├── instance/
│   └── reviewguard.db             # Local SQLite database (Users, Predictions, Metadata)
│
├── models/
│   ├── decision_tree_model.joblib # Serialized Decision Tree ML pipeline
│   ├── adaboost_model.joblib      # Serialized AdaBoost ML pipeline
│   └── training_metadata.json     # Empirical metrics, latencies, and confusion matrices
│
├── reports/
│   ├── charts/                    # Generated headless Matplotlib figures
│   └── *.pdf                      # Exported PDF evaluation & audit certificates
│
├── src/
│   ├── __init__.py                # Package initialization
│   ├── preprocessing.py           # Text cleaning, stylometrics, label standardization
│   ├── model_training.py          # Decision Tree & AdaBoost training pipelines
│   ├── prediction.py              # Probabilistic inference & keyword signal extraction
│   ├── evaluation.py              # Comparative metric calculations & CM interpretation
│   ├── visualization.py           # Chart.js JSON payloads & Matplotlib figure rendering
│   ├── review_extraction.py       # SSRF-protected URL scraping & demo mock engine
│   └── pdf_reports.py             # ReportLab PDF report generation with NumberedCanvas
│
├── static/
│   ├── css/
│   │   └── style.css              # Custom dark-mode design system with glassmorphism
│   └── js/
│       └── main.js                # Frontend AJAX handlers and CSRF injection
│
├── templates/
│   ├── base.html                  # Master layout with responsive sidebar and topbar
│   ├── index.html                 # IEEE-style landing page and project introduction
│   ├── login.html                 # Authentication form with evaluator demo credentials
│   ├── dashboard.html             # Operational metrics, Chart.js graphs, and recent audit
│   ├── upload.html                # CSV drag-and-drop upload and schema validator
│   ├── preview.html               # Statistical dataset audit and 50-row preview table
│   ├── train.html                 # Supervised training trigger with spinner animation
│   ├── performance.html           # Side-by-side metric comparison and confusion matrices
│   ├── predict.html               # Single review prediction form with sample buttons
│   ├── result.html                # Detailed verdict, confidence meter, and PDF export
│   ├── history.html               # Paginated immutable prediction audit history
│   ├── live_prediction.html       # E-commerce URL review scanner with SSRF defense
│   ├── live_result.html           # Product trust score gauge and batch breakdown
│   ├── reports.html               # Central PDF download hub
│   └── errors/
│       ├── 400.html               # Bad Request handler
│       ├── 403.html               # Access Forbidden handler
│       ├── 404.html               # Not Found handler
│       └── 500.html               # Internal Server Error handler
│
├── tests/
│   ├── test_preprocessing.py      # Unit tests for text cleaning and feature extraction
│   ├── test_prediction.py         # Unit tests for ML inference and probability sums
│   └── test_routes.py             # Integration tests for routes, auth, and SSRF blocking
│
├── app.py                         # Application factory, DB models, and route definitions
├── config.py                      # Environment configuration and security whitelists
├── requirements.txt               # Complete Python package dependency manifest
└── README.md                      # Comprehensive academic and technical documentation
```

---

## 🚀 Installation & Setup Instructions

### Prerequisites
* **Python 3.10** or higher installed on your system.
* **Git** installed (optional, for cloning).

### 1. Clone or Open the Workspace
```powershell
# Windows PowerShell
cd "c:\Shivam\Coding\ML PROJECT\fake review detector"
```

```bash
# Linux / macOS
cd ~/projects/fake-review-detector
```

### 2. Create and Activate a Virtual Environment
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏃 Running the Application

### Launch the Flask Web Server
```powershell
# Windows PowerShell
python app.py
```

```bash
# Linux / macOS
python3 app.py
```

Open your browser and navigate to:
👉 **`http://127.0.0.1:5000`**

---

## 👨‍🏫 Teacher & Evaluator Demonstration Guide

### Default Administrative Credentials
The application automatically provisions an initial evaluation account out-of-the-box:

* **Username:** `admin`
* **Password:** `Admin@12345`

### Recommended 5-Minute Demonstration Walkthrough:

1. **Home Page (`/`)**: Walk through the IEEE-style introduction, emphasizing that review sentiment is decoupled from authenticity.
2. **Sign In (`/login`)**: Log in using `admin` / `Admin@12345` to unlock the operational dashboard.
3. **Operational Intelligence Dashboard (`/dashboard`)**: Show live metrics, the active dataset counter, and dynamic Chart.js comparative performance visualizations.
4. **Active Dataset Preview (`/preview`)**: Inspect the 1,600 pre-loaded balanced benchmark records, column distributions, missing value counts, and vocabulary richness metrics.
5. **Model Training Hub (`/train`)**: Click "Execute Model Training Pipeline" to demonstrate live stratified 80/20 partitioning, TF-IDF vectorization, and classifier fitting.
6. **Performance Evaluation (`/performance`)**: Review the empirical comparison table (Decision Tree vs AdaBoost), latency metrics, confusion matrices, and the cost-matrix analysis of Type I vs Type II errors.
7. **Single Review Prediction (`/predict`)**: 
   * Click **"Genuine Review"** demo chip $\to$ observe predicted *Genuine* verdict with confidence gauge and extracted stylometric features.
   * Click **"Fake Positive"** demo chip $\to$ observe predicted *Fake* verdict, high deception probability, and influential TF-IDF terms.
   * Click **"Download PDF Certificate"** to showcase ReportLab report generation.
8. **Live URL Review Scanner (`/live_prediction`)**:
   * Click **"Demo Electronics Store (Offline Engine)"** $\to$ observe batch review extraction, overall product trust score (e.g. 78% Trust), and security SSRF guardrails.
9. **PDF Reports Center (`/reports`)**: Download the formal multi-page IEEE Benchmark Report with embedded Matplotlib figures.

---

## 📡 REST API Documentation

### 1. Predict Single Review
* **Endpoint:** `POST /api/predict`
* **Headers:** `Content-Type: application/json`
* **Request Payload:**
```json
{
  "text": "I bought this wireless keyboard for my office. Keys are responsive and battery lasts 3 weeks.",
  "model": "adaboost",
  "category": "Electronics",
  "rating": 5
}
```
* **Response Payload (HTTP 200):**
```json
{
  "badge_class": "success",
  "cleaned_text": "i bought this wireless keyboard for my office...",
  "confidence_percentage": 94.2,
  "confidence_score": 0.942,
  "fake_probability": 0.058,
  "genuine_probability": 0.942,
  "model_name": "adaboost",
  "model_used": "AdaBoost Classifier",
  "prediction_binary": 0,
  "prediction_label": "Genuine",
  "top_keywords": ["keyboard", "battery", "office", "wireless"]
}
```

### 2. Fetch Chart.js Benchmark Data
* **Endpoint:** `GET /api/charts/performance`
* **Response:** JSON payload with labels and accuracy, precision, recall, and F1 arrays.

---

## 🔒 Security Architecture

ReviewGuard AI implements multi-layered enterprise application security:

1. **SSRF Guardrail (Server-Side Request Forgery Prevention)**:
   * Rejects loopback addresses (`127.0.0.1`, `localhost`).
   * Blocks RFC 1918 private subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`).
   * Blocks cloud metadata endpoints (`169.254.169.254`).
   * Enforces a strict domain whitelist (`books.toscrape.com`, `demo-ecommerce-reviews.local`, etc.).
   * Caps maximum response payload size to **2 MB** with a **5.0-second** timeout.
2. **CSRF Defense**: All POST/PUT mutations are validated via `Flask-WTF` CSRF tokens embedded in hidden form inputs and meta headers.
3. **Credential Security**: Passwords are never stored in plaintext; salted password hashes are computed using Werkzeug's `pbkdf2:sha256` standard.
4. **Data Leakage Prevention**: Feature scaling and vectorizer vocabularies are fitted exclusively on training splits to prevent holdout contamination.

---

## 🧪 Automated Testing Suite

The repository contains an automated test suite verifying preprocessing, model inference, authentication, routes, and security defenses:

```powershell
# Run all unit and integration tests
python -m unittest discover tests
```

### Test Coverage Highlights:
* `test_clean_text`: HTML strip, URL tokenization, whitespace normalization.
* `test_extract_stylometric_features`: Verification of word count, sentence count, and Type-Token Ratio.
* `test_model_status`: Validates presence of serialized `.joblib` model artifacts.
* `test_adaboost_prediction` & `test_decision_tree_prediction`: Calibrated probabilities sum to $1.0$.
* `test_unauthenticated_dashboard_redirects`: Route protection verification.
* `test_login_success` & `test_login_failure`: Authentication state verification.
* `test_ssrf_protection_blocked`: Verifies that internal network probes are rejected before dispatch.
* `test_api_predict_endpoint`: Validates REST API JSON inputs and responses.

---

## 🎓 Academic Deliverables & Viva Voce Q&A

### Top 5 Viva Voce Questions & Answers:

**Q1: Why do you decouple sentiment analysis from review authenticity?**  
*Answer:* A positive review is not automatically genuine, and a negative review is not automatically fake. In commercial e-commerce, competitors launch coordinated negative smear attacks against high-quality products to depress their ratings, while unscrupulous merchants buy glowing 5-star reviews for inferior products. Conflating sentiment with veracity creates severe blind spots.

**Q2: What is the primary advantage of AdaBoost over a single Decision Tree?**  
*Answer:* A single Decision Tree has high variance and is prone to overfitting on idiosyncratic training words. AdaBoost is an adaptive ensemble boosting algorithm that iteratively trains weak learners, adaptively increasing the weights of misclassified samples in each round. This forces the ensemble to learn subtle, multi-term linguistic deception patterns and produces calibrated probability outputs.

**Q3: How do you prevent data leakage during TF-IDF vectorization?**  
*Answer:* If a vectorizer is fitted on the entire dataset prior to splitting, terms and document frequencies from the test set contaminate the vocabulary, artificially inflating test scores. We encapsulate `TfidfVectorizer` and classifiers inside scikit-learn `Pipeline` objects and execute `.fit()` solely on the 80% training partition.

**Q4: What is the real-world consequence of a False Positive versus a False Negative in fake review detection?**  
*Answer:* A False Positive (Type I Error) wrongly flags an authentic customer review as fake, silencing genuine consumer feedback and unfairly penalizing the reviewer. A False Negative (Type II Error) allows deceptive promotional text to pass undetected, misleading prospective buyers. AdaBoost minimizes False Positives while maintaining high detection sensitivity.

**Q5: How does the system defend against Server-Side Request Forgery (SSRF) when scanning product URLs?**  
*Answer:* The URL analyzer inspects the target hostname before dispatching requests. It resolves DNS records and checks destination IP addresses against RFC 1918 private subnets, loopback addresses (`127.0.0.1`), and cloud metadata services (`169.254.169.254`). Unsafe or unapproved domains are rejected immediately.

---

## 📜 License & Academic Integrity

This project is developed for final-year engineering degree requirements adhering to IEEE academic standards. Code is open for academic review, grading, and demonstration purposes.
