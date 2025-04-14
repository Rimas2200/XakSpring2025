from transformers import BertTokenizerFast, BertForTokenClassification, Trainer, TrainingArguments
from transformers import logging as hf_logging
from datasets import Dataset
import torch

label_list = [
    "O", "B-OPERATION", "I-OPERATION", "B-CROP", "I-CROP", "B-DATE", "B-DEPARTMENT", "I-DEPARTMENT", "B-YIELD_TOTAL"
]
label_to_id = {label: i for i, label in enumerate(label_list)}
id_to_label = {i: label for label, i in label_to_id.items()}


train_data = []

tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased")
model = BertForTokenClassification.from_pretrained("bert-base-multilingual-cased", num_labels=len(label_list))

def tokenize_and_align_labels(example):
    tokenized = tokenizer(example["tokens"], is_split_into_words=True, truncation=True, padding="max_length", max_length=64)
    word_ids = tokenized.word_ids()
    labels = [-100] * len(tokenized["input_ids"])
    for i, word_idx in enumerate(word_ids):
        if word_idx is not None:
            labels[i] = example["ner_tags"][word_idx]
    tokenized["labels"] = labels
    return tokenized

dataset = Dataset.from_list(train_data).map(tokenize_and_align_labels)

hf_logging.set_verbosity_info()

args = TrainingArguments(
    output_dir="./ner-model",
    per_device_train_batch_size=2,
    num_train_epochs=10,
    logging_steps=1,
    save_steps=1000,
    save_total_limit=1,
    evaluation_strategy="no",
    logging_dir="./logs",
    logging_first_step=True,
    logging_strategy="steps",
    disable_tqdm=False,
    report_to="none",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

trainer.train()

model.save_pretrained("./ner-model")
tokenizer.save_pretrained("./ner-model")

print("Модель сохранена в ./ner-model")
