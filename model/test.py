from model import load_model_and_tokenizer, transform_text
import pandas as pd

# Загрузка модели и токенизатора
model, tokenizer = load_model_and_tokenizer()

df_test = pd.read_excel('train.xlsx', header=None, names=['input', 'output']).dropna()
df_test = df_test.sample(10, random_state=42)

for idx, row in df_test.iterrows():
    input_text = row['input']
    true_output = row['output']
    generated = transform_text(model, tokenizer, input_text)

    print(f'Input:\n{input_text}')
    print(f'Expected Output:\n{true_output}')
    print(f'Generated Output:\n{generated}')
    print('-' * 60)
