# app.py

from flask import Flask, request, jsonify
from extraction.model_extractor import ModelExtractor
from extraction.prompt_extractor import PromptExtractor
from extraction.azure_extractor import AzureExtractor  # Optional
from dotenv import load_dotenv
import os
from flask_cors import CORS  # Import CORS
load_dotenv() 
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

model_path = os.path.join(os.getcwd(), "models", "psychometric_model")

# Initialize your extractors
model_extractor = ModelExtractor(model_path)
prompt_extractor = PromptExtractor()
azure_extractor = AzureExtractor()  # Uncomment if using Azure

@app.route('/api/psychometrics', methods=['POST'])
def extract_psychometrics():
    data = request.get_json()
    text = data.get("text", "")
    method = data.get("method", "model").lower()
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    print ("Method:", method)
    print ("Text:", text)

    try: 
        if method == "prompt":
            result = prompt_extractor.extract(text)
        elif method == "model":
            result = model_extractor.extract(text)
        elif method == "azure":
            result = azure_extractor.extract(text)
        else:
            return jsonify({"error": "Invalid method. Use 'prompt', 'model', or 'azure'."}), 400
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

    print("Extraction result:", result)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
