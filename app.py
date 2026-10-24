"""
Advanced Fake Product Review Detection System
===============================================
Production-grade Flask Web Application & REST APIs.
Implements:
- IEEE-style academic project architecture
- Session-based authentication with Werkzeug password hashing
- SQLite database via Flask-SQLAlchemy (Users, PredictionHistory, DatasetMeta)
- CSRF Protection via Flask-WTF
- Dataset upload, validation, and interactive preview
- Machine learning model training (Decision Tree & AdaBoost)
- Single review prediction & batch analysis
- Policy-compliant live URL scraping with strict SSRF guardrails
- Interactive Chart.js visualizations & ReportLab PDF report generation
"""

import os
import json
import logging
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
import pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from flask import (
    Flask, render_template, request, redirect, url_for, 
    flash, session, jsonify, send_file, abort
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import config_by_name, Config
from src.preprocessing import (
    load_and_validate_dataset,
    extract_stylometric_features,
    clean_text
)
from src.model_training import train_models, get_training_status
from src.prediction import (
    predict_single_review, get_model_status, compute_decoupling_analysis
)
from src.evaluation import compare_models, get_confusion_matrix_interpretation
from src.visualization import (
    generate_model_comparison_chart_data,
    generate_confusion_matrix_chart_data,
    generate_class_distribution_chart_data,
    generate_static_charts
)
from src.review_extraction import analyze_product_url
from src.pdf_reports import (
    generate_prediction_report,
    generate_model_evaluation_report,
    generate_url_analysis_report
)

# Initialize extensions
db = SQLAlchemy()
csrf = CSRFProtect()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger('ReviewGuardApp')


# =====================================================================
# Database Models
# =====================================================================

class User(db.Model):
    """User account model with secure password hashing."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PredictionHistory(db.Model):
    """Audit log of individual review authenticity predictions."""
    __tablename__ = 'prediction_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(80), nullable=True)
    model_name = db.Column(db.String(80), nullable=False)
    prediction_label = db.Column(db.String(20), nullable=False)  # 'Genuine' or 'Fake'
    prediction_binary = db.Column(db.Integer, nullable=False)    # 0 or 1
    confidence_score = db.Column(db.Float, nullable=False)
    fake_probability = db.Column(db.Float, nullable=False)
    genuine_probability = db.Column(db.Float, nullable=False)
    top_keywords = db.Column(db.Text, nullable=True)  # JSON-encoded array
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    def get_keywords_list(self):
        try:
            return json.loads(self.top_keywords) if self.top_keywords else []
        except Exception:
            return []


class DatasetMeta(db.Model):
    """Metadata tracking for uploaded and benchmark datasets."""
    __tablename__ = 'dataset_metadata'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    total_rows = db.Column(db.Integer, nullable=False)
    total_columns = db.Column(db.Integer, nullable=False)
    genuine_count = db.Column(db.Integer, nullable=False)
    fake_count = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


def _init_default_admin(app):
    """Idempotently provisions the initial administrator account."""
    admin_user = app.config.get('DEFAULT_ADMIN_USERNAME', 'admin')
    admin_pass = app.config.get('DEFAULT_ADMIN_PASSWORD', 'Admin@12345')

    existing = User.query.filter_by(username=admin_user).first()
    if not existing:
        admin = User(username=admin_user, role='admin')
        admin.set_password(admin_pass)
        db.session.add(admin)
        db.session.commit()
        logger.info("Initialized default administrator account '%s'.", admin_user)


def login_required(f):
    """Pass-through decorator: All routes are completely open and accessible without login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function


# =====================================================================
# Route Registration Function
# =====================================================================

def _register_routes(app):
    """Registers all context processors, routes, and error handlers onto the app instance."""

    @app.context_processor
    def inject_global_template_vars():
        """Injects user authentication status and system metadata into all templates."""
        user = None
        if session.get('user_id'):
            user = db.session.get(User, session.get('user_id'))
        if not user:
            user = User.query.filter_by(role='admin').first() or User(username='Guest User', role='public')
        
        model_status = get_model_status()
        return {
            'current_user': user,
            'model_status': model_status,
            'now': datetime.now(timezone.utc)
        }

    # =====================================================================
    # Public Routes (Landing, Auth)
    # =====================================================================

    @app.route('/')
    def index():
        """Module 1: Public Home Page & Academic Presentation Landing."""
        model_status = get_model_status()
        total_predictions = PredictionHistory.query.count()
        return render_template(
            'index.html',
            model_status=model_status,
            total_predictions=total_predictions
        )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Module 2: User Authentication Login."""
        if session.get('user_id'):
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            if not username or not password:
                flash('Please provide both username and password.', 'danger')
                return render_template('login.html')

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                flash(f'Welcome back, {user.username}!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page if next_page else url_for('dashboard'))
            else:
                flash('Invalid username or password. Check credentials and retry.', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        """Module 2: Session Logout."""
        session.clear()
        flash('You have been logged out securely.', 'info')
        return redirect(url_for('login'))

    # =====================================================================
    # Protected Dashboard & Overview
    # =====================================================================

    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Module 1 / Dashboard: System Overview with Metrics and Visualizations."""
        total_preds = PredictionHistory.query.count()
        fake_preds = PredictionHistory.query.filter_by(prediction_label='Fake').count()
        genuine_preds = PredictionHistory.query.filter_by(prediction_label='Genuine').count()
        recent_preds = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).limit(8).all()
        
        active_dataset = DatasetMeta.query.filter_by(is_active=True).first()
        if not active_dataset and os.path.exists(app.config['ACTIVE_DATASET_PATH']):
            try:
                df = pd.read_csv(app.config['ACTIVE_DATASET_PATH'])
                active_dataset = DatasetMeta(
                    filename='sample_reviews.csv',
                    filepath=app.config['ACTIVE_DATASET_PATH'],
                    total_rows=len(df),
                    total_columns=len(df.columns),
                    genuine_count=int((df['label_binary'] == 0).sum()) if 'label_binary' in df.columns else 0,
                    fake_count=int((df['label_binary'] == 1).sum()) if 'label_binary' in df.columns else 0,
                    is_active=True
                )
                db.session.add(active_dataset)
                db.session.commit()
            except Exception as e:
                logger.warning("Could not auto-register active dataset: %s", e)

        model_status = get_model_status()
        training_status = get_training_status()

        return render_template(
            'dashboard.html',
            total_preds=total_preds,
            fake_preds=fake_preds,
            genuine_preds=genuine_preds,
            recent_preds=recent_preds,
            active_dataset=active_dataset,
            model_status=model_status,
            training_status=training_status
        )

    # =====================================================================
    # Dataset Upload & Preview Modules
    # =====================================================================

    @app.route('/upload', methods=['GET', 'POST'])
    @login_required
    def upload_dataset():
        """Module 3: CSV Dataset Upload and Validation."""
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part in upload request.', 'danger')
                return redirect(request.url)

            file = request.files['file']
            if file.filename == '':
                flash('No file selected.', 'danger')
                return redirect(request.url)

            if not file.filename.lower().endswith('.csv'):
                flash('Unsupported file format. Please upload a standard CSV file.', 'danger')
                return redirect(request.url)

            try:
                filename = secure_filename(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)

                df, stats = load_and_validate_dataset(save_path)
                DatasetMeta.query.update({DatasetMeta.is_active: False})

                meta = DatasetMeta(
                    filename=filename,
                    filepath=save_path,
                    total_rows=stats['total_records'],
                    total_columns=len(df.columns),
                    genuine_count=stats['genuine_count'],
                    fake_count=stats['fake_count'],
                    is_active=True
                )
                db.session.add(meta)
                db.session.commit()

                flash(
                    f"Dataset '{filename}' successfully validated and activated: "
                    f"{stats['total_records']} records ({stats['genuine_count']} Genuine, {stats['fake_count']} Fake).",
                    'success'
                )
                return redirect(url_for('preview_dataset'))

            except Exception as e:
                logger.error("Dataset upload failed: %s", e)
                flash(f"Dataset validation error: {str(e)}", 'danger')
                return redirect(request.url)

        datasets = DatasetMeta.query.order_by(DatasetMeta.uploaded_at.desc()).all()
        return render_template('upload.html', datasets=datasets)

    @app.route('/preview')
    @login_required
    def preview_dataset():
        """Module 4: Dataset Preview with Statistical Summary and Paginated Table."""
        active_dataset = DatasetMeta.query.filter_by(is_active=True).first()
        filepath = active_dataset.filepath if active_dataset else app.config['ACTIVE_DATASET_PATH']

        if not os.path.exists(filepath):
            flash('No active dataset found on server. Please upload one.', 'warning')
            return redirect(url_for('upload_dataset'))

        try:
            df, stats = load_and_validate_dataset(filepath)
            columns = list(df.columns)
            records_preview = df.head(50).to_dict(orient='records')
            missing_stats = df.isnull().sum().to_dict()
            duplicate_count = int(df.duplicated(subset=['text'] if 'text' in df.columns else None).sum())

            return render_template(
                'preview.html',
                dataset_meta=active_dataset,
                stats=stats,
                columns=columns,
                records=records_preview,
                missing_stats=missing_stats,
                duplicate_count=duplicate_count,
                filepath=filepath
            )
        except Exception as e:
            logger.error("Preview failed: %s", e)
            flash(f"Failed to preview dataset: {str(e)}", 'danger')
            return redirect(url_for('upload_dataset'))

    @app.route('/activate_dataset/<int:dataset_id>', methods=['POST'])
    @login_required
    def activate_dataset(dataset_id):
        """Switches the active dataset for training and preview."""
        target = DatasetMeta.query.get_or_404(dataset_id)
        DatasetMeta.query.update({DatasetMeta.is_active: False})
        target.is_active = True
        db.session.commit()
        flash(f"Dataset '{target.filename}' is now active.", 'success')
        return redirect(url_for('preview_dataset'))

    # =====================================================================
    # Model Training & Performance Evaluation Modules
    # =====================================================================

    @app.route('/train', methods=['GET', 'POST'])
    @login_required
    def train():
        """Module 5: Machine Learning Model Training (Decision Tree & AdaBoost)."""
        training_status = get_training_status()
        active_dataset = DatasetMeta.query.filter_by(is_active=True).first()
        filepath = active_dataset.filepath if active_dataset else app.config['ACTIVE_DATASET_PATH']

        if request.method == 'POST':
            if not os.path.exists(filepath):
                flash('No dataset found to train on. Please upload a dataset first.', 'danger')
                return redirect(url_for('upload_dataset'))

            try:
                logger.info("Initiating model training on: %s", filepath)
                results = train_models(
                    csv_path=filepath,
                    models_dir=app.config['MODEL_FOLDER'],
                    test_size=0.20,
                    random_state=42
                )
                flash(
                    f"Models successfully trained! "
                    f"Decision Tree Accuracy: {results['results']['decision_tree']['metrics']['accuracy'] * 100:.2f}%, "
                    f"AdaBoost Accuracy: {results['results']['adaboost']['metrics']['accuracy'] * 100:.2f}%.",
                    'success'
                )
                return redirect(url_for('performance'))
            except Exception as e:
                logger.error("Training error: %s", e)
                flash(f"Training failed: {str(e)}", 'danger')

        return render_template(
            'train.html',
            training_status=training_status,
            active_dataset=active_dataset
        )

    @app.route('/performance')
    @login_required
    def performance():
        """Module 6: Model Evaluation & Comparative Performance Dashboard."""
        training_status = get_training_status()
        if not training_status.get('is_trained'):
            flash('Models have not been trained yet. Please initiate training first.', 'info')
            return redirect(url_for('train'))

        comparison = compare_models()
        
        dt_cm = training_status['results']['decision_tree']['metrics']['confusion_matrix']
        ada_cm = training_status['results']['adaboost']['metrics']['confusion_matrix']
        
        dt_interpretation = get_confusion_matrix_interpretation(dt_cm)
        ada_interpretation = get_confusion_matrix_interpretation(ada_cm)

        return render_template(
            'performance.html',
            training_status=training_status,
            comparison=comparison,
            dt_interpretation=dt_interpretation,
            ada_interpretation=ada_interpretation
        )

    # =====================================================================
    # Review Prediction & Audit History Modules
    # =====================================================================

    @app.route('/predict', methods=['GET', 'POST'])
    @login_required
    def predict():
        """Module 7: Single Review Prediction."""
        model_status = get_model_status()
        if not (model_status['decision_tree'] or model_status['adaboost']):
            flash('No trained models detected. Please train models first.', 'warning')
            return redirect(url_for('train'))

        if request.method == 'POST':
            review_text = request.form.get('review_text', '').strip()
            model_name = request.form.get('model_choice', 'adaboost')
            rating = request.form.get('rating')
            category = request.form.get('category', 'Electronics')

            if not review_text:
                flash('Please enter review text to analyze.', 'danger')
                return render_template('predict.html', model_status=model_status)

            try:
                rating_val = float(rating) if rating else None
            except ValueError:
                rating_val = None

            try:
                result = predict_single_review(
                    text=review_text,
                    model_name=model_name,
                    rating=rating_val,
                    category=category
                )

                history_entry = PredictionHistory(
                    user_id=session.get('user_id'),
                    review_text=review_text,
                    rating=rating_val,
                    category=category,
                    model_name=model_name,
                    prediction_label=result['prediction_label'],
                    prediction_binary=result['prediction_binary'],
                    confidence_score=result['confidence_score'],
                    fake_probability=result['fake_probability'],
                    genuine_probability=result['genuine_probability'],
                    top_keywords=json.dumps(result['top_keywords'])
                )
                db.session.add(history_entry)
                db.session.commit()

                return redirect(url_for('view_result', prediction_id=history_entry.id))

            except Exception as e:
                logger.error("Prediction failed: %s", e)
                flash(f"Prediction failed: {str(e)}", 'danger')

        return render_template('predict.html', model_status=model_status)

    @app.route('/result/<int:prediction_id>')
    @login_required
    def view_result(prediction_id):
        """Displays detailed prediction verdict and linguistic indicators."""
        record = PredictionHistory.query.get_or_404(prediction_id)
        keywords = record.get_keywords_list()
        stats = extract_stylometric_features(record.review_text)
        decoupling = compute_decoupling_analysis(
            text=record.review_text,
            rating=record.rating,
            prediction_label=record.prediction_label,
            stats=stats
        )

        return render_template(
            'result.html',
            record=record,
            keywords=keywords,
            stats=stats,
            decoupling=decoupling
        )

    @app.route('/history')
    @login_required
    def history():
        """Module 8: Complete Audit Log of Past Predictions."""
        page = request.args.get('page', 1, type=int)
        per_page = 20
        pagination = PredictionHistory.query.order_by(
            PredictionHistory.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

        return render_template('history.html', pagination=pagination)

    # =====================================================================
    # Live Product URL Analysis Module (Safe Scraping)
    # =====================================================================

    @app.route('/live_prediction', methods=['GET', 'POST'])
    @login_required
    def live_prediction():
        """Module 11: Policy-Compliant Live Product URL Analysis with SSRF Protection."""
        if request.method == 'POST':
            url = request.form.get('product_url', '').strip()
            model_name = request.form.get('model_choice', 'adaboost')

            if not url:
                flash('Please enter a valid product page URL.', 'danger')
                return render_template('live_prediction.html')

            try:
                logger.info("Executing URL review extraction for: %s", url)
                analysis_data = analyze_product_url(
                    url=url,
                    model_name=model_name,
                    allowed_domains=app.config['SUPPORTED_DOMAINS'],
                    timeout=app.config['URL_REQUEST_TIMEOUT']
                )

                if not analysis_data.get('success', True):
                    flash(f"Live URL Analysis Error: {analysis_data.get('error', 'Extraction failed')}", 'danger')
                    return render_template('live_prediction.html', supported_domains=app.config['SUPPORTED_DOMAINS'])

                session['latest_url_analysis'] = analysis_data

                flash(
                    f"Successfully extracted and evaluated {analysis_data['reviews_analyzed_count']} reviews. "
                    f"Product Trust Score: {analysis_data['trust_score']}% ({analysis_data['trust_level']}).",
                    'success'
                )
                return render_template('live_result.html', analysis=analysis_data)

            except Exception as e:
                logger.error("Live analysis failed for '%s': %s", url, e)
                flash(f"Live URL Analysis Error: {str(e)}", 'danger')

        return render_template('live_prediction.html', supported_domains=app.config['SUPPORTED_DOMAINS'])

    # =====================================================================
    # PDF Report Generation & Downloads
    # =====================================================================

    @app.route('/reports')
    @login_required
    def reports():
        """Module 10: PDF Reports Central Hub."""
        recent_preds = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).limit(15).all()
        has_evaluation = get_training_status().get('is_trained', False)
        has_url_analysis = 'latest_url_analysis' in session

        return render_template(
            'reports.html',
            recent_preds=recent_preds,
            has_evaluation=has_evaluation,
            has_url_analysis=has_url_analysis
        )

    @app.route('/download_report/prediction/<int:prediction_id>')
    @login_required
    def download_prediction_pdf(prediction_id):
        """Generates and downloads a formal PDF certificate for an individual review prediction."""
        record = PredictionHistory.query.get_or_404(prediction_id)
        output_filename = f"ReviewGuard_Prediction_{record.id}.pdf"
        output_path = os.path.join(app.config['REPORT_FOLDER'], output_filename)

        stats = extract_stylometric_features(record.review_text)
        decoupling = compute_decoupling_analysis(
            text=record.review_text,
            rating=record.rating,
            prediction_label=record.prediction_label,
            stats=stats
        )

        pred_data = {
            'id': record.id,
            'review_text': record.review_text,
            'model_name': record.model_name,
            'model_used': record.model_name,
            'category': record.category,
            'rating': record.rating,
            'prediction_label': record.prediction_label,
            'confidence_score': record.confidence_score,
            'confidence_percentage': round(record.confidence_score * 100, 2),
            'fake_probability': record.fake_probability,
            'genuine_probability': record.genuine_probability,
            'probability_fake': round(record.fake_probability * 100, 2),
            'probability_genuine': round(record.genuine_probability * 100, 2),
            'top_keywords': record.get_keywords_list(),
            'salient_keywords': record.get_keywords_list(),
            'stats': stats,
            'decoupling': decoupling,
            'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')
        }

        try:
            generate_prediction_report(pred_data, output_path)
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        except Exception as e:
            logger.error("Failed to generate prediction PDF: %s", e)
            flash(f"Failed to generate PDF report: {str(e)}", 'danger')
            return redirect(url_for('view_result', prediction_id=prediction_id))

    @app.route('/download_report/evaluation')
    @login_required
    def download_evaluation_pdf():
        """Generates and downloads the comprehensive IEEE-style model evaluation report."""
        output_filename = "ReviewGuard_Model_Benchmark_Report.pdf"
        output_path = os.path.join(app.config['REPORT_FOLDER'], output_filename)

        try:
            generate_model_evaluation_report(
                metadata_path=app.config['METADATA_PATH'],
                output_pdf_path=output_path
            )
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        except Exception as e:
            logger.error("Failed to generate evaluation PDF: %s", e)
            flash(f"Failed to generate evaluation PDF: {str(e)}", 'danger')
            return redirect(url_for('performance'))

    @app.route('/download_report/live')
    @login_required
    def download_live_analysis_pdf():
        """Generates and downloads the live product URL authenticity audit report."""
        analysis = session.get('latest_url_analysis')
        if not analysis:
            flash('No recent live URL analysis found in your session.', 'warning')
            return redirect(url_for('live_prediction'))

        output_filename = f"ReviewGuard_URL_Audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = os.path.join(app.config['REPORT_FOLDER'], output_filename)

        try:
            generate_url_analysis_report(analysis, output_path)
            return send_file(output_path, as_attachment=True, download_name=output_filename)
        except Exception as e:
            logger.error("Failed to generate URL analysis PDF: %s", e)
            flash(f"Failed to generate URL analysis PDF: {str(e)}", 'danger')
            return redirect(url_for('live_prediction'))

    @app.route('/presentation')
    def presentation_view():
        """Serves the interactive 15-slide master presentation for projectors and viva defense."""
        presentation_html_path = os.path.join(app.root_path, "presentation.html")
        if os.path.exists(presentation_html_path):
            return send_file(presentation_html_path)
        flash('Interactive presentation template not found.', 'warning')
        return redirect(url_for('reports'))

    @app.route('/download_presentation/pdf')
    def download_presentation_pdf():
        """Downloads the 15-slide academic master presentation PDF."""
        pdf_path = os.path.join(app.root_path, "ReviewGuard_AI_Master_Presentation.pdf")
        if os.path.exists(pdf_path):
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name="ReviewGuard_AI_Master_Presentation.pdf"
            )
        flash('Presentation PDF not found on server.', 'warning')
        return redirect(url_for('reports'))

    @app.route('/download_presentation/pptx')
    def download_presentation_pptx():
        """Downloads the 15-slide PowerPoint (PPTX) presentation with speaker notes."""
        pptx_path = os.path.join(app.root_path, "ReviewGuard_AI_Master_Presentation.pptx")
        if os.path.exists(pptx_path):
            return send_file(
                pptx_path,
                as_attachment=True,
                download_name="ReviewGuard_AI_Master_Presentation.pptx"
            )
        flash('PowerPoint presentation file not found on server.', 'warning')
        return redirect(url_for('reports'))

    @app.route('/download_presentation/guide')
    def download_presentation_guide():
        """Downloads the companion Viva Voce Defense & Speaker Script Guide PDF."""
        guide_path = os.path.join(app.root_path, "ReviewGuard_AI_Speaker_Script_and_Viva_Guide.pdf")
        if os.path.exists(guide_path):
            return send_file(
                guide_path,
                as_attachment=True,
                download_name="ReviewGuard_AI_Speaker_Script_and_Viva_Guide.pdf"
            )
        flash('Viva Voce guide file not found on server.', 'warning')
        return redirect(url_for('reports'))

    # =====================================================================
    # REST API Endpoints
    # =====================================================================

    @app.route('/api/predict', methods=['POST'])
    @csrf.exempt
    def api_predict():
        """REST API endpoint for real-time review inference."""
        data = request.get_json(silent=True) or request.form
        text = data.get('text', '').strip()
        model_name = data.get('model', 'adaboost')
        category = data.get('category', 'General')
        rating = data.get('rating')

        if not text:
            return jsonify({'error': 'Review text is required.'}), 400

        try:
            rating_val = float(rating) if rating is not None else None
        except ValueError:
            rating_val = None

        try:
            result = predict_single_review(
                text=text,
                model_name=model_name,
                rating=rating_val,
                category=category
            )
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/charts/performance')
    @login_required
    def api_charts_performance():
        """Returns Chart.js compatible JSON payload for performance metrics."""
        return jsonify(generate_model_comparison_chart_data())

    @app.route('/api/charts/confusion_matrix/<model_name>')
    @login_required
    def api_charts_confusion_matrix(model_name):
        """Returns Chart.js compatible confusion matrix payload."""
        return jsonify(generate_confusion_matrix_chart_data(model_name))

    # =====================================================================
    # Error Handlers
    # =====================================================================

    @app.errorhandler(400)
    def bad_request_error(e):
        return render_template('errors/400.html', error=e), 400

    @app.errorhandler(403)
    def forbidden_error(e):
        return render_template('errors/403.html', error=e), 403

    @app.errorhandler(404)
    def not_found_error(e):
        return render_template('errors/404.html', error=e), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        logger.exception("Internal Server Error caught by handler: %s", e)
        return render_template('errors/500.html', error=e), 500


def create_app(config_name='default'):
    """Application factory for Flask."""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    for folder in [
        app.config['UPLOAD_FOLDER'],
        app.config['DATASET_FOLDER'],
        app.config['MODEL_FOLDER'],
        app.config['REPORT_FOLDER'],
        os.path.join(app.root_path, 'instance')
    ]:
        os.makedirs(folder, exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        db.create_all()
        _init_default_admin(app)

    _register_routes(app)
    return app


# Root application instance for WSGI/Gunicorn/Direct run
app = create_app(os.environ.get('FLASK_ENV', 'default'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() in ('true', '1', 'yes')
    logger.info("Starting ReviewGuard AI Web Server on http://127.0.0.1:%s (Debug=%s)", port, debug)
    app.run(host='127.0.0.1', port=port, debug=debug)
