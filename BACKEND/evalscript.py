import torch
import pandas as pd
from transformers import BertTokenizerFast, BertForSequenceClassification
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from datasets import Dataset
from tqdm import tqdm

# 1. Load model and tokenizer
# Correct absolute path to your trained model
model_path = "D:/02_TAMUCC SPRING 2025/HCI/TERM-PROJECT/BACKEND/trained_emotion_model"

model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizerFast.from_pretrained(model_path)
model.eval()

# 2. Load test data
df_test = pd.read_csv("DATASETS/goemotions_only.csv")
df_test = df_test[["text", "label"]].dropna()

# Mapping labels to IDs
unique_labels = sorted(df_test["label"].unique())
label2id = {label: i for i, label in enumerate(unique_labels)}
id2label = {i: label for label, i in label2id.items()}

# Encode text
test_dataset = Dataset.from_pandas(df_test)
encoded_test = test_dataset.map(lambda e: tokenizer(e['text'], truncation=True, padding='max_length'), batched=True)
encoded_test.set_format(type='torch', columns=['input_ids', 'attention_mask'])

# 3. Run evaluation manually
all_preds = []
all_labels = []

for i in tqdm(range(len(encoded_test))):
    input_ids = encoded_test[i]['input_ids'].unsqueeze(0)
    attention_mask = encoded_test[i]['attention_mask'].unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
    
    logits = outputs.logits
    pred = torch.argmax(logits, dim=1).item()
    all_preds.append(pred)
    true_label = label2id[df_test.iloc[i]["label"]]
    all_labels.append(true_label)

# 4. Calculate Metrics
accuracy = accuracy_score(all_labels, all_preds)
precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='weighted')

print("\n✅ EVALUATION METRICS:")
print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")
print("\n✅ Evaluation completed successfully!")