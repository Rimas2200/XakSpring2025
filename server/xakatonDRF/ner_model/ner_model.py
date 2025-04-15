import json
from transformers import BertTokenizerFast, BertForTokenClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch
from pathlib import Path

def load_data_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

train_data = load_data_from_json("processed_data.json")

unique_labels = set(tag for example in train_data for tag in example["ner_tags"])
label_list = sorted(unique_labels)
label_to_id = {label: i for i, label in enumerate(label_list)}
print(label_list)

tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased")
model = BertForTokenClassification.from_pretrained(
    "bert-base-multilingual-cased", num_labels=len(label_list)
)

# Функция для токенизации и выравнивания меток
def tokenize_and_align_labels(example):
    tokenized = tokenizer(
        example["tokens"],
        is_split_into_words=True,
        truncation=True,
        padding="max_length",
        max_length=64,
    )
    word_ids = tokenized.word_ids()
    labels = [-100] * len(tokenized["input_ids"])
    for i, word_idx in enumerate(word_ids):
        if word_idx is not None:
            labels[i] = label_to_id[example["ner_tags"][word_idx]]
    tokenized["labels"] = labels
    return tokenized

dataset = Dataset.from_list(train_data).map(tokenize_and_align_labels)

training_args = TrainingArguments(
    output_dir="./ner-model",
    per_device_train_batch_size=2,
    num_train_epochs=50,
    logging_steps=1,
    save_steps=10000,
    save_total_limit=1,
    evaluation_strategy="no",
    logging_dir="./logs",
    logging_first_step=True,
    logging_strategy="steps",
    disable_tqdm=True,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

trainer.train()

model.save_pretrained("./ner-model")

print("Модель сохранена в ./ner-model")