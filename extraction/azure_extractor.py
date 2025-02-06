# extraction/azure_extractor.py

import os
import requests
from .base_extractor import BaseExtractor

class AzureExtractor(BaseExtractor):
    def __init__(self):
        # Set these environment variables or configure as needed
        self.endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
        self.subscription_key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
        if not self.endpoint or not self.subscription_key:
            raise ValueError("Azure endpoint or subscription key not set")

    def extract(self, text: str) -> dict:
        headers = {
            "Ocp-Apim-Subscription-Key": self.subscription_key,
            "Content-Type": "application/json"
        }
        body = {
            "documents": [
                {"id": "1", "language": "en", "text": text}
            ]
        }
        # Call Azure Text Analytics sentiment endpoint with opinion mining enabled
        url = f"{self.endpoint}/text/analytics/v3.2-preview.1/sentiment?opinionMining=true"
        response = requests.post(url, headers=headers, json=body)
        result = response.json()
        
        try:
            document = result["documents"][0]
            # Document-level sentiment
            overall_sentiment = document.get("sentiment", "neutral")
            
            # Default scores (0 to 1 scale)
            awareness = 0.5
            conscientiousness = 0.5
            stress = 0.5
            neuroticism = 0.5
            risk_tolerance = 0.5
            
            # Map overall sentiment to stress and neuroticism (simplified mapping)
            if overall_sentiment == "negative":
                stress = 0.8
                neuroticism = 0.7
            elif overall_sentiment == "positive":
                stress = 0.3
                neuroticism = 0.3
            else:
                stress = 0.5
                neuroticism = 0.5
            
            # Process sentence-level opinions for more granular mapping
            for sentence in document.get("sentences", []):
                # Each sentence may have a list of opinions with targets and assessments.
                opinions = sentence.get("opinions", [])
                for opinion in opinions:
                    target_text = opinion.get("target", {}).get("text", "").lower()
                    # Get the assessment(s) which include sentiment and confidence score
                    assessments = opinion.get("assessments", [])
                    for assessment in assessments:
                        aspect_sentiment = assessment.get("sentiment", "neutral")
                        # We use confidence scores as a proxy for intensity
                        confidence = assessment.get("confidenceScore", 0.5)
                        
                        # Map aspects based on keywords
                        if "security" in target_text or "best practice" in target_text:
                            # If positive, higher awareness
                            if aspect_sentiment == "positive":
                                awareness = max(awareness, confidence)
                        if "guideline" in target_text or "procedure" in target_text or "detail" in target_text:
                            if aspect_sentiment == "positive":
                                conscientiousness = max(conscientiousness, confidence)
                        if "overwhelmed" in target_text or "stress" in target_text or "pressure" in target_text:
                            if aspect_sentiment == "negative":
                                stress = max(stress, confidence)
                        if "anxious" in target_text or "worried" in target_text or "nervous" in target_text:
                            if aspect_sentiment == "negative":
                                neuroticism = max(neuroticism, confidence)
                        if "shortcut" in target_text or "risk" in target_text:
                            if aspect_sentiment == "positive":
                                risk_tolerance = max(risk_tolerance, confidence)
            
            # Return the mapped scores
            return {
                "awareness": round(awareness, 2),
                "conscientiousness": round(conscientiousness, 2),
                "stress": round(stress, 2),
                "neuroticism": round(neuroticism, 2),
                "risk_tolerance": round(risk_tolerance, 2)
            }
        except Exception as e:
            return {"error": "Failed to parse Azure response", "details": str(e)}
