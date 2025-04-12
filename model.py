import pandas as pd
import numpy as np
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import random
from tqdm.auto import tqdm, trange
from sklearn.model_selection import train_test_split

df = pd.read_excel('нормализованный_output_paragraphs.xlsx', header=None, names=['input', 'output'])

pd.options.display.max_colwidth = 500
print("Примеры данных:")
print(df.sample(5))

# Разделение на обучающую и тестовую выборки
df_train, df_test = train_test_split(df.dropna(), test_size=0.2, random_state=42)

# Подготовка пар для обучения
pairs = df_train[['input', 'output']].values.tolist()

# Инициализация модели и токенизатора
model_name = 'cointegrated/rut5-base-multitask'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name).cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

batch_size = 8
report_steps = 100
epochs = 70

model.train()
losses = []

for epoch in range(epochs):
    print(f'\nEPOCH {epoch + 1}/{epochs}')
    random.shuffle(pairs)

    for i in trange(0, int(len(pairs) / batch_size)):
        batch = pairs[i * batch_size: (i + 1) * batch_size]

        # Токенизация входных и целевых текстов
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

        # Замена pad токенов на -100 для игнорирования в функции потерь
        y.input_ids[y.input_ids == tokenizer.pad_token_id] = -100

        # Вычисление потерь
        outputs = model(
            input_ids=x.input_ids,
            attention_mask=x.attention_mask,
            labels=y.input_ids,
            decoder_attention_mask=y.attention_mask,
            return_dict=True
        )

        loss = outputs.loss
        loss.backward()

        # Оптимизация
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        optimizer.zero_grad()

        losses.append(loss.item())

        if i % report_steps == 0:
            print(f'Step {i}, Loss: {np.mean(losses[-report_steps:]):.4f}')

model.eval()


# Функция для генерации ответов
def transform_text(text, **kwargs):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=128).to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=128,
            num_beams=5,
            repetition_penalty=2.5,
            **kwargs
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

model.save_pretrained("agriculture_text_transform_model")
tokenizer.save_pretrained("agriculture_text_transform_model")