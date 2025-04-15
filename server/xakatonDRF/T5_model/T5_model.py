import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

MODEL_NAME = 'cointegrated/rut5-base-multitask'
MODEL_PATH = 'agriculture_text_transform_model'


def load_model_and_tokenizer(model_path=MODEL_PATH):
    tokenizer = T5Tokenizer.from_pretrained(model_path)

    model = T5ForConditionalGeneration.from_pretrained(model_path).to(torch.device('cpu'))
    return model, tokenizer


def save_model_and_tokenizer(model, tokenizer, model_path=MODEL_PATH):
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)


def transform_text(model, tokenizer, text, **kwargs):
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
