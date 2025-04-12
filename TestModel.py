import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


model_path = "agriculture_text_transform_model"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path).cuda()
model.eval()


def transform_text(text):
    inputs = tokenizer(
        text,
        return_tensors='pt',
        truncation=True,
        max_length=128
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=128,
            num_beams=5,
            repetition_penalty=2.5,
            early_stopping=True
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


while True:
    user_input = input("\nтекст: ").strip()

    if user_input.lower() in ['q']:
        break

    transformed_text = transform_text(user_input)
    print(f"Исходный текст: {user_input}")
    print(f"Преобразованный текст: {transformed_text}")
