import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict
from transformers import BertTokenizerFast, BertForSequenceClassification, Trainer, TrainingArguments
import torch

# Load GoEmotions only dataset
df = pd.read_csv("DATASETS/goemotions_only.csv")
df = df[["text", "label"]].dropna()

# Split
train_df, test_df = train_test_split(df, test_size=0.1, stratify=df["label"], random_state=42)

# Convert to Hugging Face Datasets
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# Load tokenizer
tokenizer =BertTokenizerFast.from_pretrained('bert-base-uncased')

# Label encoding
label_list = list(set(train_dataset["label"]))
label2id = {label: i for i, label in enumerate(sorted(label_list))}
id2label = {i: label for label, i in label2id.items()}

# Preprocessing function
def preprocess_function(examples):
    return {
        **tokenizer(examples["text"], truncation=True, padding=True),
        "label": [label2id[label] for label in examples["label"]],
    }

# Combine into DatasetDict
dataset = DatasetDict({
    "train": train_dataset,
    "test": test_dataset
})

# Tokenize
encoded_dataset = dataset.map(preprocess_function, batched=True)

# Optional: set format for PyTorch
encoded_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# Load model
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=len(label2id),
    id2label=id2label,
    label2id=label2id
)

# Training arguments


training_args = TrainingArguments(
    output_dir="./results",          # output directory
    num_train_epochs=3,              # total number of training epochs
    per_device_train_batch_size=16,  # batch size per device during training
    per_device_eval_batch_size=64,   # batch size for evaluation
    logging_dir="./logs",            # directory for storing logs
    logging_steps=200,
    save_steps=500,
    save_total_limit=2
)


# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset["train"],
    eval_dataset=encoded_dataset["test"],
    tokenizer=tokenizer
)

# Train!
trainer.train()

# Save the model

model.save_pretrained("trained_emotion_model")
tokenizer.save_pretrained("trained_emotion_model")

print("✅ Training complete and model saved!")

