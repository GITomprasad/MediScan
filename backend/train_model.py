"""
MediScan AI - Medical Report Classification Model Trainer
Trains a TF-IDF + Calibrated Logistic Regression model on labeled medical reports.
Saves model, vectorizer, and evaluation metrics for the backend.
"""

import json
import os
import re
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "medical_reports_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "trained_models")
os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODEL_DIR, "classifier.joblib")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "model_metrics.json")

def preprocess_text(text: str) -> str:
    """Preprocess medical text: lowercase, remove special noise, normalize whitespace."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Replace non-word chars (keeping hyphens and spaces)
    text = re.sub(r'[^a-z0-9\s\-_]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train_and_evaluate():
    print(f"Loading dataset from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset loaded: {len(df)} samples across {df['category'].nunique()} categories.")
    print("Class distribution:")
    print(df['category'].value_counts())

    # Preprocess text
    df['clean_text'] = df['text'].apply(preprocess_text)

    X = df['clean_text']
    y = df['category']

    # Stratified train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    print(f"\nTraining set size: {len(X_train)}, Test set size: {len(X_test)}")

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print(f"TF-IDF Vocabulary size: {len(vectorizer.vocabulary_)} features.")

    # Train Classifier (Logistic Regression with multi_class='multinomial')
    model = LogisticRegression(
        C=2.0,
        max_iter=1000,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_train_vec, y_train)

    # Predictions & Probabilities
    y_pred = model.predict(X_test_vec)
    y_prob = model.predict_proba(X_test_vec)

    # Metrics calculation
    acc = accuracy_score(y_test, y_pred)
    prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(y_test, y_pred, average='macro')
    prec_weighted, rec_weighted, f1_weighted, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
    
    classes = list(model.classes_)
    cm = confusion_matrix(y_test, y_pred, labels=classes)
    cls_report = classification_report(y_test, y_pred, target_names=classes, output_dict=True)

    print("\n" + "="*50)
    print("MODEL EVALUATION RESULTS (Test Set)")
    print("="*50)
    print(f"Accuracy:  {acc * 100:.2f}%")
    print(f"Precision: {prec_macro * 100:.2f}% (Macro)")
    print(f"Recall:    {rec_macro * 100:.2f}% (Macro)")
    print(f"F1-Score:  {f1_macro * 100:.2f}% (Macro)")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred, target_names=classes))

    # Save artifacts
    print(f"\nSaving model to: {MODEL_PATH}")
    joblib.dump(model, MODEL_PATH)

    print(f"Saving vectorizer to: {VECTORIZER_PATH}")
    joblib.dump(vectorizer, VECTORIZER_PATH)

    metrics_data = {
        "accuracy": round(float(acc), 4),
        "precision_macro": round(float(prec_macro), 4),
        "recall_macro": round(float(rec_macro), 4),
        "f1_macro": round(float(f1_macro), 4),
        "precision_weighted": round(float(prec_weighted), 4),
        "recall_weighted": round(float(rec_weighted), 4),
        "f1_weighted": round(float(f1_weighted), 4),
        "classes": classes,
        "confusion_matrix": cm.tolist(),
        "classification_report": cls_report,
        "total_samples": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test)
    }

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=2)

    print(f"Saving metrics to: {METRICS_PATH}")
    print("Training and evaluation completed successfully!")

if __name__ == "__main__":
    train_and_evaluate()
