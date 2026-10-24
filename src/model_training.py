"""
Machine Learning Model Training & Pipeline Serialization Module
==============================================================
Trains, tunes, evaluates, and serializes two core classifiers:
- Model A: Decision Tree Classifier
- Model B: AdaBoost Classifier

Strictly prevents data leakage by bundling the TF-IDF vectorizer and 
classifier inside scikit-learn Pipelines fitted solely on training splits.
"""

import os
import time
import json
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

from src.preprocessing import (
    standardize_dataset, prepare_train_test_split, get_tfidf_vectorizer
)

def evaluate_pipeline(pipeline, X_train, y_train, X_test, y_test, model_name: str) -> dict:
    """
    Fits a pipeline on X_train/y_train, measures training & testing latencies,
    and computes full classification metrics on the holdout test set.
    """
    # 1. Measure Training Time
    start_train = time.perf_counter()
    pipeline.fit(X_train, y_train)
    train_time = round(time.perf_counter() - start_train, 4)
    
    # 2. Measure Inference / Testing Time
    start_test = time.perf_counter()
    y_pred = pipeline.predict(X_test)
    test_time = round(time.perf_counter() - start_test, 4)
    inference_latency_ms = round((test_time / max(len(X_test), 1)) * 1000, 2)
    
    # 3. Compute Metrics (Class 1 = Fake/Computer-Generated, Class 0 = Genuine)
    acc = round(float(accuracy_score(y_test, y_pred)), 4)
    prec = round(float(precision_score(y_test, y_pred, pos_label=1, zero_division=0)), 4)
    rec = round(float(recall_score(y_test, y_pred, pos_label=1, zero_division=0)), 4)
    f1 = round(float(f1_score(y_test, y_pred, pos_label=1, zero_division=0)), 4)
    
    # Macro metrics
    prec_macro = round(float(precision_score(y_test, y_pred, average='macro', zero_division=0)), 4)
    rec_macro = round(float(recall_score(y_test, y_pred, average='macro', zero_division=0)), 4)
    f1_macro = round(float(f1_score(y_test, y_pred, average='macro', zero_division=0)), 4)
    
    # Confusion Matrix: [[TN, FP], [FN, TP]]
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    # Classification Report
    clf_report = classification_report(y_test, y_pred, target_names=['Genuine', 'Fake'], output_dict=True)
    
    return {
        "model_name": model_name,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "precision_macro": prec_macro,
        "recall_macro": rec_macro,
        "f1_macro": f1_macro,
        "train_time_sec": train_time,
        "training_time_seconds": train_time,
        "test_time_sec": test_time,
        "inference_latency_ms": inference_latency_ms,
        "confusion_matrix": {
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
            "matrix": [[int(tn), int(fp)], [int(fn), int(tp)]]
        },
        "classification_report": clf_report
    }

def train_all_models(
    dataset_path: str,
    output_dir: str,
    test_size: float = 0.20,
    random_state: int = 42
) -> dict:
    """
    Executes the complete academic training workflow:
    1. Loads and standardizes dataset from dataset_path
    2. Performs stratified train/test split
    3. Trains Decision Tree Classifier pipeline
    4. Trains AdaBoost Classifier pipeline
    5. Serializes trained pipelines to output_dir
    6. Saves comparative training metadata as JSON
    """
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset file not found at: {dataset_path}")
        
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Standardize dataset
    raw_df = pd.read_csv(dataset_path)
    clean_df, data_summary = standardize_dataset(raw_df)
    
    # Step 2: Stratified Partitioning
    X_train, X_test, y_train, y_test = prepare_train_test_split(
        clean_df, test_size=test_size, random_state=random_state
    )
    
    # -------------------------------------------------------------
    # Model A: Decision Tree Classifier Pipeline
    # -------------------------------------------------------------
    dt_classifier = DecisionTreeClassifier(
        criterion="gini",
        max_depth=30,
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=random_state
    )
    dt_pipeline = Pipeline([
        ('tfidf', get_tfidf_vectorizer()),
        ('clf', dt_classifier)
    ])
    
    dt_metrics = evaluate_pipeline(
        dt_pipeline, X_train, y_train, X_test, y_test, 
        model_name="Decision Tree Classifier"
    )
    dt_model_path = os.path.join(output_dir, "decision_tree_model.joblib")
    joblib.dump(dt_pipeline, dt_model_path)
    
    # -------------------------------------------------------------
    # Model B: AdaBoost Classifier Pipeline
    # -------------------------------------------------------------
    base_estimator = DecisionTreeClassifier(
        max_depth=3, 
        class_weight="balanced", 
        random_state=random_state
    )
    
    try:
        ada_classifier = AdaBoostClassifier(
            estimator=base_estimator,
            n_estimators=60,
            learning_rate=0.8,
            random_state=random_state
        )
    except TypeError:
        ada_classifier = AdaBoostClassifier(
            base_estimator=base_estimator,
            n_estimators=60,
            learning_rate=0.8,
            random_state=random_state
        )
        
    ada_pipeline = Pipeline([
        ('tfidf', get_tfidf_vectorizer()),
        ('clf', ada_classifier)
    ])
    
    ada_metrics = evaluate_pipeline(
        ada_pipeline, X_train, y_train, X_test, y_test, 
        model_name="AdaBoost Classifier"
    )
    ada_model_path = os.path.join(output_dir, "adaboost_model.joblib")
    joblib.dump(ada_pipeline, ada_model_path)
    
    # Step 3: Record Comprehensive Experiment Metadata
    trained_at = time.strftime("%Y-%m-%d %H:%M:%S")
    best_model_key = "adaboost" if ada_metrics["f1_score"] >= dt_metrics["f1_score"] else "decision_tree"
    
    metadata = {
        "dataset_path": dataset_path,
        "total_records": len(clean_df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "genuine_count": data_summary["genuine_count"],
        "fake_count": data_summary["fake_count"],
        "trained_at": trained_at,
        "timestamp": trained_at,
        "is_trained": True,
        "best_model": best_model_key,
        "best_model_by_f1": "AdaBoost" if ada_metrics["f1_score"] >= dt_metrics["f1_score"] else "Decision Tree",
        "best_model_by_accuracy": "AdaBoost" if ada_metrics["accuracy"] >= dt_metrics["accuracy"] else "Decision Tree",
        "models": {
            "Decision Tree": dt_metrics,
            "AdaBoost": ada_metrics
        },
        "results": {
            "decision_tree": {
                "model_name": "Decision Tree Classifier",
                "training_time_seconds": dt_metrics["train_time_sec"],
                "inference_latency_ms": dt_metrics["inference_latency_ms"],
                "metrics": dt_metrics
            },
            "adaboost": {
                "model_name": "AdaBoost Classifier",
                "training_time_seconds": ada_metrics["train_time_sec"],
                "inference_latency_ms": ada_metrics["inference_latency_ms"],
                "metrics": ada_metrics
            }
        }
    }
    
    meta_path = os.path.join(output_dir, "training_metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=4)
        
    return metadata

def train_models(csv_path: str, models_dir: str = "models", test_size: float = 0.20, random_state: int = 42) -> dict:
    """Wrapper conforming to app.py calling convention."""
    return train_all_models(
        dataset_path=csv_path,
        output_dir=models_dir,
        test_size=test_size,
        random_state=random_state
    )

def get_training_status(models_dir: str = "models") -> dict:
    """Retrieves current model training status from metadata file with safe defaults."""
    meta_path = os.path.join(models_dir, "training_metadata.json")
    dt_exists = os.path.exists(os.path.join(models_dir, "decision_tree_model.joblib"))
    ada_exists = os.path.exists(os.path.join(models_dir, "adaboost_model.joblib"))
    
    data = {
        "is_trained": dt_exists and ada_exists,
        "trained_at": "Recently trained",
        "timestamp": "Recently trained",
        "best_model": "adaboost",
        "models": {},
        "results": {}
    }

    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r") as f:
                loaded = json.load(f)
                data.update(loaded)
                data["is_trained"] = True

                if not data.get("trained_at"):
                    data["trained_at"] = data.get("timestamp", "Recently trained")

                # Synthesize results mapping if models dict is present
                if "models" in data and not data.get("results"):
                    dt = data["models"].get("Decision Tree", {})
                    ada = data["models"].get("AdaBoost", {})
                    data["results"] = {
                        "decision_tree": {
                            "model_name": "Decision Tree Classifier",
                            "training_time_seconds": dt.get("train_time_sec", 0.0),
                            "inference_latency_ms": dt.get("inference_latency_ms", 0.0),
                            "metrics": dt
                        },
                        "adaboost": {
                            "model_name": "AdaBoost Classifier",
                            "training_time_seconds": ada.get("train_time_sec", 0.0),
                            "inference_latency_ms": ada.get("inference_latency_ms", 0.0),
                            "metrics": ada
                        }
                    }
                
                if not data.get("best_model"):
                    best_hint = data.get("best_model_by_f1", "AdaBoost").lower()
                    data["best_model"] = "decision_tree" if "tree" in best_hint else "adaboost"

                return data
        except Exception:
            pass

    return data
