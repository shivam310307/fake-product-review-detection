"""
Model Performance Evaluation & Metric Interpretation Module
===========================================================
Calculates and formats academic performance metrics:
- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix interpretation (TP, TN, FP, FN)
- Training & testing execution latency
- Domain-specific explanation of False Positives vs False Negatives
"""

import os
import json

def load_training_metadata(metadata_path: str = "models/training_metadata.json") -> dict:
    """Loads saved experiment evaluation metadata from disk."""
    if not os.path.exists(metadata_path):
        return None
    with open(metadata_path, "r") as f:
        return json.load(f)

def explain_evaluation_concepts() -> dict:
    """
    Returns formal academic definitions and interpretations of ML metrics
    tailored specifically to the fake review detection problem domain.
    """
    return {
        "positive_class": "Class 1: Fake / Computer-Generated Review",
        "negative_class": "Class 0: Genuine / Original Review",
        "definitions": {
            "True Positive (TP)": (
                "A fake or computer-generated review is correctly identified and flagged by the model."
            ),
            "True Negative (TN)": (
                "An authentic customer review is correctly classified as genuine."
            ),
            "False Positive (FP)": (
                "Type I Error: An authentic customer review is mistakenly flagged as fake. "
                "In e-commerce, high FP rates unfairly silence legitimate customer opinions."
            ),
            "False Negative (FN)": (
                "Type II Error: A deceptive fake review slips through unnoticed. "
                "In e-commerce, high FN rates expose consumers to astroturfed hype or unmitigated attack campaigns."
            ),
            "Precision": (
                "TP / (TP + FP): When the model predicts a review is fake, how often is it actually fake? "
                "High precision prevents falsely accusing genuine buyers."
            ),
            "Recall (Sensitivity)": (
                "TP / (TP + FN): What percentage of all actual fake reviews did the model successfully catch? "
                "High recall ensures comprehensive fraud coverage."
            ),
            "F1-Score": (
                "Harmonic mean of Precision and Recall: 2 * (Precision * Recall) / (Precision + Recall). "
                "The most reliable single metric when evaluating imbalanced review datasets."
            )
        }
    }

class ConfusionMatrixData:
    """Provides dual attribute and dictionary item access to confusion matrix counts."""
    def __init__(self, tn: int, fp: int, fn: int, tp: int):
        self.true_negative = int(tn)
        self.false_positive = int(fp)
        self.false_negative = int(fn)
        self.true_positive = int(tp)
        self.tn = self.true_negative
        self.fp = self.false_positive
        self.fn = self.false_negative
        self.tp = self.true_positive

    def __getitem__(self, item):
        return getattr(self, item)

    def to_dict(self):
        return {
            "true_negative": self.true_negative,
            "false_positive": self.false_positive,
            "false_negative": self.false_negative,
            "true_positive": self.true_positive
        }

def get_confusion_matrix_interpretation(cm) -> ConfusionMatrixData:
    """Interprets a confusion matrix input into a ConfusionMatrixData object."""
    if isinstance(cm, dict):
        tn = cm.get('tn', cm.get('true_negative', 0))
        fp = cm.get('fp', cm.get('false_positive', 0))
        fn = cm.get('fn', cm.get('false_negative', 0))
        tp = cm.get('tp', cm.get('true_positive', 0))
    elif isinstance(cm, (list, tuple)):
        if len(cm) == 2 and isinstance(cm[0], (list, tuple)):
            tn, fp = cm[0][0], cm[0][1]
            fn, tp = cm[1][0], cm[1][1]
        elif len(cm) == 4:
            tn, fp, fn, tp = cm
        else:
            tn, fp, fn, tp = 0, 0, 0, 0
    else:
        tn, fp, fn, tp = 0, 0, 0, 0

    return ConfusionMatrixData(tn, fp, fn, tp)

def get_comparative_table(metadata: dict) -> list[dict]:
    """Formats comparison between Decision Tree and AdaBoost for HTML table rendering."""
    if not metadata or "models" not in metadata:
        return []
        
    rows = []
    models_dict = metadata["models"]
    
    for m_key, m_val in models_dict.items():
        cm = m_val["confusion_matrix"]
        rows.append({
            "name": m_val["model_name"],
            "accuracy": f"{m_val['accuracy'] * 100:.2f}%",
            "precision": f"{m_val['precision'] * 100:.2f}%",
            "recall": f"{m_val['recall'] * 100:.2f}%",
            "f1_score": f"{m_val['f1_score'] * 100:.2f}%",
            "train_time": f"{m_val.get('train_time_sec', m_val.get('training_time_seconds', 0)):.4f} s",
            "test_time": f"{m_val.get('test_time_sec', 0):.4f} s",
            "tp": cm["tp"],
            "tn": cm["tn"],
            "fp": cm["fp"],
            "fn": cm["fn"]
        })
    return rows

def compare_models(metadata_path: str = "models/training_metadata.json") -> dict:
    """Loads metadata and computes comparison between Decision Tree and AdaBoost."""
    meta = load_training_metadata(metadata_path)
    if not meta:
        return {
            "has_data": False,
            "rows": [],
            "concepts": explain_evaluation_concepts()
        }
        
    rows = get_comparative_table(meta)
    return {
        "has_data": True,
        "metadata": meta,
        "rows": rows,
        "concepts": explain_evaluation_concepts(),
        "best_model": meta.get("best_model_by_f1", "AdaBoost")
    }
