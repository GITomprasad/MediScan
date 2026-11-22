"""
MediScan AI - Classification Service
Loads trained TF-IDF vectorizer and model, handles text inference,
and returns category, confidence score, and top class probabilities.
"""

import os
import re
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "trained_models", "classifier.joblib")
VECTORIZER_PATH = os.path.join(BASE_DIR, "trained_models", "tfidf_vectorizer.joblib")
METRICS_PATH = os.path.join(BASE_DIR, "trained_models", "model_metrics.json")

class MedicalDocumentClassifier:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MedicalDocumentClassifier, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.vectorizer = None
            cls._instance.classes = []
            cls._instance.load_model()
        return cls._instance

    def load_model(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.vectorizer = joblib.load(VECTORIZER_PATH)
            self.classes = list(self.model.classes_)
            print(f"[MediScan AI ML] Loaded classifier model with classes: {self.classes}")
        else:
            print(f"[MediScan AI ML] Model files not found at {MODEL_PATH}. Please run train_model.py first.")

    @staticmethod
    def preprocess(text: str) -> str:
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s\-_]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def classify(self, raw_text: str):
        if not self.model or not self.vectorizer:
            self.load_model()
            if not self.model:
                raise RuntimeError("ML model is not loaded. Train the model before classifying.")

        clean_text = self.preprocess(raw_text)
        if len(clean_text) < 15:
            raise ValueError("Insufficient text content to classify.")

        vec = self.vectorizer.transform([clean_text])
        probabilities = self.model.predict_proba(vec)[0]
        
        # Build category probability dictionary
        prob_dict = {}
        for category, prob in zip(self.classes, probabilities):
            prob_dict[category] = round(float(prob), 4)

        # Get highest probability category
        best_category = max(prob_dict, key=prob_dict.get)
        confidence = prob_dict[best_category]

        return {
            "predicted_category": best_category,
            "confidence_score": confidence,
            "all_probabilities": prob_dict
        }

classifier_service = MedicalDocumentClassifier()
