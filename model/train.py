import pandas as pd
import numpy as np
import torch
import random
from tqdm.auto import trange
from sklearn.model_selection import train_test_split
from model import load_model_and_tokenizer, save_model_and_tokenizer, MODEL_NAME

df = pd.read_excel('train.xlsx', header=None, names=['input', 'output'])
df_train, df_test = train_test_split(df.dropna(), test_size=0.2, random_state=42)
pairs = df_train[['input', 'output']].values.tolist()

# Загрузка модели и токенизатора
tokenizer = torch.hub.load('huggingface/pytorch-transformers', 'tokenizer', MODEL_NAME)
model = torch.hub.load('huggingface/pytorch-transformers', 'modelForConditionalGeneration', MODEL_NAME).cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

batch_size = 16
report_steps = 100
epochs = 95

model.train()
losses = []

for epoch in range(epochs):
    print(f'\nEPOCH {epoch + 1}/{epochs}')
    random.shuffle(pairs)

    for i in trange(0, int(len(pairs) / batch_size)):
        batch = pairs[i * batch_size: (i + 1) * batch_size]

        x = tokenizer(
            [p[0] for p in batch],
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=128
        ).to(model.device)

        y = tokenizer(
            [p[1] for p in batch],
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=128
        ).to(model.device)

        y.input_ids[y.input_ids == tokenizer.pad_token_id] = -100

        outputs = model(
            input_ids=x.input_ids,
            attention_mask=x.attention_mask,
            labels=y.input_ids,
            decoder_attention_mask=y.attention_mask,
            return_dict=True
        )

        loss = outputs.loss
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        optimizer.zero_grad()

        losses.append(loss.item())

        if i % report_steps == 0:
            print(f'Step {i}, Loss: {np.mean(losses[-report_steps:]):.4f}')

model.eval()
save_model_and_tokenizer(model, tokenizer)
