import json

import numpy as np
import pandas as pd

file_path = "Таблица (полевые работы).xlsx"
df = pd.read_excel(file_path)

df = df.dropna(subset=["За день, га", "С начала операции, га"], how="all")

df["За день, га"] = pd.to_numeric(df["За день, га"], errors="coerce")
df["С начала операции, га"] = pd.to_numeric(df["С начала операции, га"], errors="coerce")
df["Вал за день, ц"] = pd.to_numeric(df["Вал за день, ц"], errors="coerce")
df["Вал с начала, ц"] = pd.to_numeric(df["Вал с начала, ц"], errors="coerce")

def predict_completion(row, total_area):
    """
    Рассчитывает оставшиеся дни для завершения операции.

    :param row: строка DataFrame с данными по операции
    :param total_area: общая площадь для выполнения операции (га)
    :return: количество дней до завершения или None
    """
    processed_area = row["С начала операции, га"]
    daily_rate = row["За день, га"]

    if pd.isna(daily_rate) or daily_rate == 0:
        return None

    if total_area is None:
        return None

    remaining_area = total_area - processed_area
    if remaining_area <= 0:
        return 0

    days_remaining = remaining_area / daily_rate
    return round(days_remaining, 1)

total_areas = {
    "Выравнивание зяби": 6000,
    "Предпосевная культивация": 5000,
    "Сев": 3000,
    "Пахота": 4000,
    "Чизлевание": 2000,
    "Дискование": 10000,
}

df["Прогноз (дней)"] = df.apply(
    lambda row: predict_completion(row, total_areas.get(row["Операция"], None)), axis=1
)

df = df.dropna(subset=["Прогноз (дней)"])

df = df.replace({np.nan: None})

output_data = df.to_dict(orient="records")
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print("Данные успешно сохранены в data.json")