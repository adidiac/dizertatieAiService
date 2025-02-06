import os
import json
import openai
from .base_extractor import BaseExtractor

class PromptExtractor(BaseExtractor):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = self.api_key

    def _generate_prompt(self, text: str) -> str:
        return f"""
Analyze the following text and provide scores between 0 and 1 for the following dimensions:
- Awareness (knowledge of cybersecurity best practices)
- Conscientiousness (attention to detail, adherence to guidelines)
- Stress (current level of stress, where 0 means no stress and 1 means extremely stressed)
- Neuroticism (tendency to experience negative emotions)
- Risk Tolerance (willingness to take risks, where 0 is very risk averse and 1 is highly risk tolerant)

Text: "{text}"

Respond with a JSON object in the following format:
{{"awareness": <score>, "conscientiousness": <score>, "stress": <score>, "neuroticism": <score>, "risk_tolerance": <score>}}
"""

    def extract(self, text: str) -> dict:
        prompt = self._generate_prompt(text)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # or use another available model
                messages=[
                    {"role": "system", "content": "You are an expert in psychometrics."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150,
            )
            # Get the message content from the response
            output_text = response["choices"][0]["message"]["content"].strip()
            # Try to extract the JSON from the output text
            json_start = output_text.find("{")
            json_end = output_text.rfind("}") + 1
            json_str = output_text[json_start:json_end]
            scores = json.loads(json_str)
        except Exception as e:
            scores = {"error": "Failed to parse prompt response", "details": str(e)}
        return scores
