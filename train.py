"""
Fake Review Detection - Machine Learning Training Script
========================================================
This script loads the review dataset, validates and cleans the text data,
fits candidate classification models using TF-IDF feature extraction inside
a scikit-learn Pipeline (preventing data leakage), evaluates accuracy,
precision, recall, and F1-score, selects the best model based on F1-score,
and saves the trained model pipeline to 'model/review_model.pkl'.
"""

import os
import re
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def clean_text(text):
    """Simple, transparent text cleaning function."""
    if not isinstance(text, str):
        return ""
    # Convert to lowercase
    text = text.lower()
    # Normalize URLs
    text = re.sub(r'http\S+|www\S+|https\S+', ' [URL] ', text)
    # Normalize excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def main():
    print("=" * 60)
    print("      Fake Review Detection - Model Training & Pipeline      ")
    print("=" * 60)

    dataset_path = os.path.join("data", "reviews.csv")
    if not os.path.exists(dataset_path):
        print(f"[ERROR] Dataset file not found at: {dataset_path}")
        print("Please ensure 'data/reviews.csv' exists before training.")
        return

    print("\n1. Loading dataset...")
    df = pd.read_csv(dataset_path)
    initial_count = len(df)
    print(f"   Initial rows loaded: {initial_count}")

    # Validate column presence
    if 'review' not in df.columns or 'label' not in df.columns:
        print("[ERROR] Dataset must contain 'review' and 'label' columns.")
        return

    # Clean missing rows
    df = df.dropna(subset=['review', 'label'])
    missing_removed = initial_count - len(df)

    # Normalize labels (e.g. 'real' -> 'genuine', 0/1, case insensitive)
    label_map = {
        'genuine': 'genuine', 'real': 'genuine', '1': 'genuine', 1: 'genuine',
        'fake': 'fake', '0': 'fake', 0: 'fake'
    }
    df['label'] = df['label'].astype(str).str.strip().str.lower()
    df['label'] = df['label'].map(lambda x: label_map.get(x, x))
    
    # Keep only valid labels
    df = df[df['label'].isin(['genuine', 'fake'])]

    # Remove exact duplicates
    dup_before = len(df)
    df = df.drop_duplicates(subset=['review'])
    duplicates_removed = dup_before - len(df)

    # Clean text reviews
    df['clean_review'] = df['review'].apply(clean_text)
    df = df[df['clean_review'].str.strip() != ""]

    total_reviews = len(df)
    genuine_count = (df['label'] == 'genuine').sum()
    fake_count = (df['label'] == 'fake').sum()

    print("\n2. Dataset Statistics:")
    print(f"   Total valid reviews: {total_reviews}")
    print(f"   Genuine reviews    : {genuine_count}")
    print(f"   Fake reviews       : {fake_count}")
    print(f"   Missing rows dropped: {missing_removed}")
    print(f"   Duplicates removed : {duplicates_removed}")

    if total_reviews < 10:
        print("[ERROR] Dataset too small for training.")
        return

    # Prepare features and target
    X = df['clean_review']
    y = df['label']

    print("\n3. Splitting dataset (80% Train, 20% Test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Candidate models dictionary
    candidate_models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Linear SVM (Calibrated)": CalibratedClassifierCV(LinearSVC(random_state=42, max_iter=2000)),
        "Multinomial Naive Bayes": MultinomialNB()
    }

    print("\n4. Training & Evaluating Candidate Models:")
    print("-" * 60)

    best_name = None
    best_f1 = -1.0
    best_pipeline = None
    results = {}

    for name, clf in candidate_models.items():
        # Create pipeline: TF-IDF vectorizer + Classifier
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
            ('classifier', clf)
        ])

        # Fit strictly on training data (no data leakage)
        pipeline.fit(X_train, y_train)

        # Predict on test set
        y_pred = pipeline.predict(X_test)

        # Calculate metrics ('fake' treated as positive class for precision/recall calculation)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, pos_label='fake', zero_division=0)
        rec = recall_score(y_test, y_pred, pos_label='fake', zero_division=0)
        f1 = f1_score(y_test, y_pred, pos_label='fake', zero_division=0)

        results[name] = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'pipeline': pipeline
        }

        print(f"   Model: {name}")
        print(f"     Accuracy : {acc * 100:.2f}%")
        print(f"     Precision: {prec * 100:.2f}%")
        print(f"     Recall   : {rec * 100:.2f}%")
        print(f"     F1-score : {f1 * 100:.2f}%")
        print("-" * 60)

        # Selection based on F1-score
        if f1 > best_f1:
            best_f1 = f1
            best_name = name
            best_pipeline = pipeline

    print(f"\n5. Best Model Selected: {best_name} (F1-score: {best_f1 * 100:.2f}%)")

    # Save complete pipeline
    model_dir = "model"
    os.makedirs(model_dir, exist_ok=True)
    model_file = os.path.join(model_dir, "review_model.pkl")

    # Attach model metadata for downstream evaluation and explainability
    best_pipeline.model_name_ = best_name
    best_pipeline.evaluation_results_ = {
        k: {m: round(v[m] * 100, 2) for m in ['accuracy', 'precision', 'recall', 'f1']}
        for k, v in results.items()
    }
    
    joblib.dump(best_pipeline, model_file)
    print(f"   Pipeline successfully saved to '{model_file}'")

    print("\n" + "=" * 60)
    print("               Training Completed Successfully!               ")
    print("=" * 60)


if __name__ == "__main__":
    main()
