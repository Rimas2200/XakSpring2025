# model_loader.py
import os
from transformers import AutoModelForSeq2SeqLM, AutoModelForTokenClassification, AutoTokenizer

def load_models():
    # Пути к папкам с моделями
    t5_model_path = "T5_model/agriculture_text_transform_model"
    ner_model_path = "ner_model/ner-model"

    # Загрузка T5 модели, если её нет
    if not os.path.exists(t5_model_path):
        print("Скачивание файлов")
        os.makedirs(t5_model_path, exist_ok=True)
        model = AutoModelForSeq2SeqLM.from_pretrained("RimasZzz/agriculture_text_transform_model")
        tokenizer = AutoTokenizer.from_pretrained("RimasZzz/agriculture_text_transform_model")
        model.save_pretrained(t5_model_path)
        tokenizer.save_pretrained(t5_model_path)

    # Загрузка NER модели, если её нет
    if not os.path.exists(ner_model_path):
        print("Скачивание файлов ")
        os.makedirs(ner_model_path, exist_ok=True)
        model = AutoModelForTokenClassification.from_pretrained("RimasZzz/agriculture_bert-base-multilingual-cased")
        tokenizer = AutoTokenizer.from_pretrained("RimasZzz/agriculture_bert-base-multilingual-cased")
        model.save_pretrained(ner_model_path)
        tokenizer.save_pretrained(ner_model_path)