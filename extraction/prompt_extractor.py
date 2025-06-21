import os
import json
import openai
from .base_extractor import BaseExtractor

class PromptExtractor(BaseExtractor):
    def __init__(self):
        # Require the API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        # Instantiate the v1 client
        self.client = openai.OpenAI(api_key=self.api_key)

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
            resp = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in psychometrics."},
                    {"role": "user",   "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150,
            )
            # Use attribute access for the v1 response object
            content = resp.choices[0].message.content.strip()
            start = content.find("{")
            end   = content.rfind("}") + 1
            return json.loads(content[start:end])

        except Exception as e:
            scores = {
                "awareness": 0,
                "conscientiousness": 0,
                "stress": 0,
                "neuroticism": 0,
                "risk_tolerance": 0
            }
            print(f"Error during OpenAI API call: {e}")
        return scores


