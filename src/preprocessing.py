"""
Data Preprocessing & Linguistic Feature Extraction Module
=========================================================
Handles text sanitization, column normalization, label standardisation,
linguistic feature engineering, and stratified data partitioning.
Prevents data leakage by ensuring all feature transformations fit only on training folds.
"""

import re
import os
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

# Standard accepted column names across various public datasets
CANDIDATE_TEXT_COLUMNS = [
    'text', 'review', 'review_text', 'review_body', 
    'content', 'comments', 'review_comment', 'clean_text',
    'review text', 'review content'
]

CANDIDATE_LABEL_COLUMNS = [
    'label', 'label_binary', 'target', 'class', 
    'deceptive', 'is_fake', 'feedback', 'target label'
]

COLUMN_ALIAS_MAP = {
    'review text': 'text',
    'review_text': 'text',
    'review_body': 'text',
    'review body': 'text',
    'content': 'text',
    'comments': 'text',
    'clean_text': 'text',
    'target label': 'label',
    'target_label': 'label',
    'target': 'label',
    'class': 'label',
    'deceptive': 'label',
    'is_fake': 'label',
    'rating score': 'rating',
    'rating_score': 'rating',
    'product category': 'category',
    'product_category': 'category'
}

def clean_text(text: str) -> str:
    """
    Sanitizes raw review text for machine learning.
    - Strips HTML tags
    - Replaces URLs with a generic token
    - Normalizes multiple spaces and newlines
    - Preserves sentence-ending punctuation for stylometric extraction
    """
    if not isinstance(text, str):
        return ""
    
    # Remove HTML tags
    cleaned = re.sub(r'<[^>]+>', ' ', text)
    # Mask URLs
    cleaned = re.sub(r'https?://\S+|www\.\S+', '[URL]', cleaned)
    # Normalize whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def compute_linguistic_features(text: str) -> dict:
    """
    Computes stylometric and structural linguistic statistics from review text.
    These features represent stylistic markers without requiring external network calls.
    """
    if not text:
        return {
            "text_length": 0,
            "word_count": 0,
            "average_word_length": 0.0,
            "vocabulary_richness": 0.0,
            "sentence_count": 0,
            "exclamation_count": 0,
            "question_count": 0
        }
    
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    char_count = len(text)
    
    # Vocabulary Richness (Type-Token Ratio)
    unique_words = len(set(words))
    vocab_richness = round(unique_words / max(word_count, 1), 4)
    
    # Average word length
    avg_word_len = round(sum(len(w) for w in words) / max(word_count, 1), 2)
    
    # Sentence count estimation
    sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
    sentence_count = max(len(sentences), 1 if word_count > 0 else 0)
    
    exclamation_count = text.count('!')
    question_count = text.count('?')
    
    return {
        "text_length": char_count,
        "word_count": word_count,
        "average_word_length": avg_word_len,
        "vocabulary_richness": vocab_richness,
        "sentence_count": sentence_count,
        "exclamation_count": exclamation_count,
        "question_count": question_count
    }

# Alias for stylometric extraction
extract_stylometric_features = compute_linguistic_features

def map_label_to_binary(val) -> int:
    """
    Maps heterogeneous label conventions to standard binary classification:
    - 0 = Genuine / Original Review ('OR', 'genuine', 'real', '0', 0)
    - 1 = Fake / Computer-Generated Review ('CG', 'fake', 'deceptive', '1', 1)
    """
    if pd.isna(val):
        raise ValueError("Missing label value encountered.")
    
    s = str(val).strip().lower()
    
    # Genuine representations
    if s in ['genuine', 'or', 'real', 'truthful', 'authentic', '0', '0.0', 'false']:
        return 0
    # Fake representations
    elif s in ['fake', 'cg', 'deceptive', 'spam', 'fraud', '1', '1.0', 'true']:
        return 1
    else:
        try:
            num = int(float(s))
            if num in [0, 1]:
                return num
        except ValueError:
            pass
        raise ValueError(f"Ambiguous or unrecognized label value: '{val}'. Expected 'genuine'/'fake', 'OR'/'CG', or '0'/'1'.")

def standardize_labels(series: pd.Series) -> pd.Series:
    """Standardizes an entire Series of labels to binary integers (0 or 1)."""
    return series.apply(map_label_to_binary)

def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalizes column names in a DataFrame based on standard aliases."""
    renamed = {}
    for col in df.columns:
        norm_key = str(col).strip().lower()
        if norm_key in COLUMN_ALIAS_MAP:
            renamed[col] = COLUMN_ALIAS_MAP[norm_key]
    return df.rename(columns=renamed)

def standardize_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Standardizes an uploaded dataframe into the canonical ReviewGuard schema:
    - Identifies text and label columns
    - Drops empty/null rows and duplicates
    - Computes missing linguistic features
    - Returns standardized DataFrame and diagnostic summary
    """
    initial_rows = len(df)
    
    # Normalize column names first
    df = normalize_column_names(df)
    columns_lower = {str(col).lower().strip(): col for col in df.columns}
    
    # 1. Identify text column
    text_col = None
    for cand in CANDIDATE_TEXT_COLUMNS:
        if cand in columns_lower:
            text_col = columns_lower[cand]
            break
            
    if not text_col:
        raise ValueError(
            f"Could not identify a valid review text column. Found columns: {list(df.columns)}. "
            f"Expected one of: {CANDIDATE_TEXT_COLUMNS}."
        )
        
    # 2. Identify label column
    label_col = None
    for cand in CANDIDATE_LABEL_COLUMNS:
        if cand in columns_lower:
            label_col = columns_lower[cand]
            break
            
    if not label_col:
        raise ValueError(
            f"Could not identify a valid label column. Found columns: {list(df.columns)}. "
            f"Expected one of: {CANDIDATE_LABEL_COLUMNS}."
        )
        
    # 3. Clean and map data
    processed_df = df.copy()
    processed_df['text'] = processed_df[text_col].astype(str).apply(clean_text)
    
    # Drop empty texts (< 3 characters)
    processed_df = processed_df[processed_df['text'].str.len() >= 3]
    
    # Map labels
    processed_df['label_binary'] = processed_df[label_col].apply(map_label_to_binary)
    processed_df['label'] = processed_df['label_binary'].map({0: 'genuine', 1: 'fake'})
    
    # Deduplicate on review text to prevent train/test leakage
    pre_dedup = len(processed_df)
    processed_df = processed_df.drop_duplicates(subset=['text']).reset_index(drop=True)
    duplicates_removed = pre_dedup - len(processed_df)
    
    # 4. Ensure linguistic features exist
    if 'vocabulary_richness' not in processed_df.columns or 'sentence_count' not in processed_df.columns:
        stats_list = [compute_linguistic_features(t) for t in processed_df['text']]
        stats_df = pd.DataFrame(stats_list)
        for c in stats_df.columns:
            if c not in processed_df.columns:
                processed_df[c] = stats_df[c]
                
    summary = {
        "initial_rows": initial_rows,
        "valid_rows": len(processed_df),
        "total_records": len(processed_df),
        "duplicates_removed": duplicates_removed,
        "genuine_count": int(sum(processed_df['label_binary'] == 0)),
        "fake_count": int(sum(processed_df['label_binary'] == 1)),
        "text_column_detected": text_col,
        "label_column_detected": label_col
    }
    
    return processed_df, summary

def load_and_validate_dataset(csv_path_or_df) -> tuple[pd.DataFrame, dict]:
    """Loads a CSV dataset (or accepts a DataFrame) and validates schema."""
    if isinstance(csv_path_or_df, (str, Path)):
        if not os.path.exists(csv_path_or_df):
            raise FileNotFoundError(f"Dataset file not found at: {csv_path_or_df}")
        df = pd.read_csv(csv_path_or_df)
    else:
        df = csv_path_or_df
    return standardize_dataset(df)

def prepare_train_test_split(df: pd.DataFrame, test_size: float = 0.20, random_state: int = 42):
    """
    Splits the standardized dataset into stratified train and test partitions.
    Ensures class distribution balance across both sets.
    """
    # Ensure label column exists
    if 'label_binary' not in df.columns:
        df, _ = standardize_dataset(df)
        
    if len(df) < 20:
        raise ValueError("Dataset is too small for meaningful training and evaluation (minimum 20 records required).")
        
    genuine_count = sum(df['label_binary'] == 0)
    fake_count = sum(df['label_binary'] == 1)
    
    if genuine_count < 5 or fake_count < 5:
        raise ValueError(
            f"Insufficient class diversity: Found {genuine_count} genuine and {fake_count} fake reviews. "
            "At least 5 samples of each class are required for stratified splitting."
        )
        
    X = df['text']
    y = df['label_binary']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state, 
        stratify=y
    )
    
    return X_train, X_test, y_train, y_test

# Alias for prepare_train_test_split
prepare_data_splits = prepare_train_test_split

def get_tfidf_vectorizer():
    """Returns standardized TF-IDF Vectorizer configuration."""
    return TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words='english',
        sublinear_tf=True
    )
