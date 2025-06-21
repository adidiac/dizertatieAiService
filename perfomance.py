import time, pandas as pd, numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Încarcă datele de test
test_df = pd.read_csv("models/mbti_psychometrics.csv").sample(n=20, random_state=42)

# 2. Instanţiere extractoare
from extraction.model_extractor import ModelExtractor
from extraction.prompt_extractor import PromptExtractor
from extraction.azure_extractor  import AzureExtractor

model_ext  = ModelExtractor("models/psychometric_model")
prompt_ext = PromptExtractor()
azure_ext  = AzureExtractor()

print("Model extractor loaded")

methods = {
    "model":  model_ext.extract,
    "prompt": prompt_ext.extract,
    "azure":  azure_ext.extract
}

dims = ["awareness","conscientiousness","stress","neuroticism","risk_tolerance"]
errors   = {m:{d:[] for d in dims} for m in methods}
latency  = {m:[] for m in methods}
print("Extractors loaded")
# 3. Colectează MSE și latențe
for m, fn in methods.items():
    for i, row in test_df.iterrows():
        text = row["text"]
        gt   = {d: row[d] for d in dims}

        # predict
        t0   = time.perf_counter()
        pred = fn(text)
        t1   = time.perf_counter()
        latency[m].append(t1 - t0)

        # normalize keys
        pred = {k.lower(): v for k, v in pred.items()}

        # compute squared errors
        for d in dims:
            if d not in pred:
                print(f"[{m}] missing '{d}' for sample {i}; pred keys:", pred.keys())
                # you can choose to skip or assume pred[d]=0
                continue
            errors[m][d].append((pred[d] - gt[d])**2)

# 4. Calculează MSE
mse = {m:{d: np.mean(errors[m][d]) for d in dims} for m in methods}

# 5. Plot MSE
import matplotlib.pyplot as plt
plt.figure()
for m in methods:
    vals = [mse[m][d] for d in dims]
    plt.plot(dims, vals, marker='o', label=m)
plt.title("MSE per psychometric dimension")
plt.ylabel("MSE")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 6. Plot latenţe
plt.figure()
df_lat = pd.DataFrame({m: latency[m] for m in methods})
df_lat.boxplot()
plt.title("Latency per extraction method")
plt.ylabel("Time (s)")
plt.tight_layout()
plt.show()
