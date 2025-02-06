# extraction/model_extractor.py

import torch
from transformers import BertTokenizer, BertForSequenceClassification
from .base_extractor import BaseExtractor

class ModelExtractor(BaseExtractor):
    def __init__(self, model_path: str):
        try:
            self.tokenizer = BertTokenizer.from_pretrained(model_path)
            self.model = BertForSequenceClassification.from_pretrained(model_path, num_labels=5)
            self.model.eval()
        except Exception as e:
            raise RuntimeError("Failed to load model") from e

    def extract(self, text: str) -> dict:
        inputs = self.tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=128)
        with torch.no_grad():
            outputs = self.model(**inputs)
        scores = outputs.logits.squeeze().tolist()
        if not isinstance(scores, list):
            scores = [scores]
        return {
            "awareness": scores[0],
            "conscientiousness": scores[1],
            "stress": scores[2],
            "neuroticism": scores[3],
            "risk_tolerance": scores[4]
        }
