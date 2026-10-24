"""
Automated Unit Tests for Preprocessing and Feature Extraction Modules
====================================================================
"""

import unittest
import pandas as pd
from src.preprocessing import (
    clean_text,
    extract_stylometric_features,
    normalize_column_names,
    standardize_labels,
    prepare_data_splits
)

class TestPreprocessing(unittest.TestCase):
    
    def test_clean_text(self):
        dirty = "<p>This is an <b>AWESOME</b> product!!! Check it out at https://example.com</p>"
        cleaned = clean_text(dirty)
        self.assertNotIn("<p>", cleaned)
        self.assertNotIn("<b>", cleaned)
        self.assertNotIn("https://", cleaned)
        self.assertIn("awesome", cleaned.lower())
        self.assertIn("product", cleaned)

    def test_extract_stylometric_features(self):
        text = "Super fast delivery! Works completely as expected. Would buy again."
        feats = extract_stylometric_features(text)
        self.assertGreater(feats['word_count'], 0)
        self.assertGreater(feats['sentence_count'], 0)
        self.assertGreater(feats['average_word_length'], 0)
        self.assertGreater(feats['vocabulary_richness'], 0.0)
        self.assertEqual(feats['exclamation_count'], 1)
        self.assertEqual(feats['question_count'], 0)

    def test_normalize_column_names(self):
        df = pd.DataFrame({
            'Review Text': ['Great phone'],
            'Rating Score': [5],
            'Target Label': [0]
        })
        norm_df = normalize_column_names(df)
        self.assertIn('text', norm_df.columns)
        self.assertIn('rating', norm_df.columns)
        self.assertIn('label', norm_df.columns)

    def test_standardize_labels(self):
        # Numeric labels
        self.assertEqual(standardize_labels(pd.Series([0, 1])).tolist(), [0, 1])
        # Text labels
        self.assertEqual(standardize_labels(pd.Series(['genuine', 'fake'])).tolist(), [0, 1])
        self.assertEqual(standardize_labels(pd.Series(['OR', 'CG'])).tolist(), [0, 1])
        self.assertEqual(standardize_labels(pd.Series(['real', 'fake'])).tolist(), [0, 1])

    def test_prepare_data_splits(self):
        df = pd.DataFrame({
            'text': [f"Review number {i}" for i in range(100)],
            'label': [0 if i % 2 == 0 else 1 for i in range(100)]
        })
        X_train, X_test, y_train, y_test = prepare_data_splits(df, test_size=0.2, random_state=42)
        self.assertEqual(len(X_train), 80)
        self.assertEqual(len(X_test), 20)
        self.assertEqual(len(y_train), 80)
        self.assertEqual(len(y_test), 20)

if __name__ == '__main__':
    unittest.main()
