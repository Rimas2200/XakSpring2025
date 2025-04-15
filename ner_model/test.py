import torch
from transformers import BertTokenizerFast, BertForTokenClassification


model_path = "./ner-model"
tokenizer = BertTokenizerFast.from_pretrained(model_path)
model = BertForTokenClassification.from_pretrained(model_path)

label_list = ['B-CROP', 'B-DATE', 'B-DEPARTMENT', 'B-HECTARE', 'B-OPERATION', 'B-SUBUNIT', 'B-YIELD_TOTAL', 'I-CROP', 'I-DEPARTMENT', 'I-HECTARE', 'I-OPERATION', 'I-SUBUNIT', 'I-YIELD_TOTAL', 'O']


def remove_duplicate_words(text):
    seen = set()
    result = []
    for word in text.split():
        if word not in seen:
            seen.add(word)
            result.append(word)
    return " ".join(result)


def predict_entities(text):
    words = text.split()

    inputs = tokenizer(
        words,
        is_split_into_words=True,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predictions = torch.argmax(outputs.logits, dim=2)[0].tolist()

    word_ids = inputs.word_ids()
    entities = []
    current_entity = None
    current_entity_words = []
    current_entity_start = None
    last_word_idx = None

    for word_idx, label_id in zip(word_ids, predictions):
        if word_idx is None:
            continue

        last_word_idx = word_idx

        label = label_list[label_id]
        word = words[word_idx]

        if label.startswith("B-"):
            if current_entity:
                entities.append({
                    "entity": current_entity,
                    "text": " ".join(current_entity_words),
                    "start": current_entity_start,
                    "end": word_idx
                })
            current_entity = label[2:]
            current_entity_words = [word]
            current_entity_start = word_idx

        elif label.startswith("I-") and current_entity and label[2:] == current_entity:
            current_entity_words.append(word)

        else:
            if current_entity:
                entities.append({
                    "entity": current_entity,
                    "text": " ".join(current_entity_words),
                    "start": current_entity_start,
                    "end": word_idx
                })
                current_entity = None
                current_entity_words = []
                current_entity_start = None

    if current_entity and last_word_idx is not None:
        entities.append({
            "entity": current_entity,
            "text": " ".join(current_entity_words),
            "start": current_entity_start,
            "end": last_word_idx + 1
        })

    merged_entities = []
    for entity in entities:
        if not merged_entities:
            merged_entities.append(entity)
        else:
            last_entity = merged_entities[-1]
            if (last_entity['entity'] == entity['entity'] and
                    last_entity['end'] == entity['start']):
                last_entity['text'] += " " + entity['text']
                last_entity['end'] = entity['end']
            else:
                merged_entities.append(entity)

    for entity in merged_entities:
        entity['text'] = remove_duplicate_words(entity['text'])

    return merged_entities

if __name__ == "__main__":
    example_text = "Пахота под Соя товарная: День - 295 га От начала - 6804 га (79%) Остаток- 1774 га"
    # example_text = "Пахота под Соя товарная: День - 295 га От начала - 6804 га (79%) Остаток- 1774 га"
    # example_text = "16.11 Мир Пахота под Кукуруза товарная 30 га, 599 га, 89%, 73 га остаток. Пахота под Соя товарная 30 га, 879 га, 77%, 260 га остаток. Работало 2 агрегата."
    entities = predict_entities(example_text)

    print("Текст:", example_text)
    print("Извлеченные сущности:")
    for entity in entities:
        print(f"- {entity['entity']}: '{entity['text']}'")