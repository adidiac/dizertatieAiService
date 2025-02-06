import pandas as pd
import numpy as np
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import evaluate

# Load your CSV data
data = pd.read_csv("psychometric_data.csv")

def preprocess_data(df):
    return {
        "text": df["text"].tolist(),
        "labels": df[["awareness", "conscientiousness", "stress", "neuroticism", "risk_tolerance"]].values.tolist()
    }

data_dict = preprocess_data(data)
dataset = Dataset.from_dict(data_dict)

# Split dataset
split = dataset.train_test_split(test_size=0.2)
train_dataset = split["train"]
eval_dataset = split["test"]

model_name = "bert-base-uncased"
# Load the pretrained tokenizer and model from the official checkpoint.
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=5, problem_type="regression")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

train_dataset = train_dataset.map(tokenize_function, batched=True)
eval_dataset = eval_dataset.map(tokenize_function, batched=True)

train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
eval_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# Load MSE metric using evaluate
mse_metric = evaluate.load("mse")

def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    mse = ((predictions - labels) ** 2).mean()
    return {"mse": mse}

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    evaluation_strategy="epoch",
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.save_model("./psychometric_model")

# Add this line to also save the tokenizer in the same folder.
tokenizer.save_pretrained("./psychometric_model")
