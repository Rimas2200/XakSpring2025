import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


file_path = "Таблица (полевые работы).xlsx"
df = pd.read_excel(file_path)

df = df.dropna(subset=["За день, га", "С начала операции, га"])

df["За день, га"] = pd.to_numeric(df["За день, га"], errors="coerce")
df["С начала операции, га"] = pd.to_numeric(df["С начала операции, га"], errors="coerce")

def predict_completion(row, total_area):
    """
    Рассчитывает оставшиеся дни для завершения операции.

    :param row: строка DataFrame с данными по операции
    :param total_area: общая площадь для выполнения операции (га)
    :return: количество дней до завершения или сообщение об ошибке
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

df["Дата"] = pd.to_datetime(df["Дата"], format="%d.%m", errors="coerce")
df = df.dropna(subset=["Дата"])

plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
sns.barplot(data=df, x="Операция", y="Прогноз (дней)", hue="Подразделение", errorbar=None)
plt.title("Прогноз завершения операций (дни)")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Оставшиеся дни")
plt.xlabel("Операция")

lagging_units = df[df["Прогноз (дней)"] > 10]
plt.subplot(2, 2, 3)
sns.barplot(data=lagging_units, x="Подразделение", y="Прогноз (дней)", hue="Операция", errorbar=None)
plt.title("Отстающие подразделения")
plt.xticks(rotation=45, ha="right")
plt.ylabel("Оставшиеся дни")
plt.xlabel("Подразделение")

plt.subplot(2, 2, 4)
operation_counts = df["Операция"].value_counts()
plt.pie(operation_counts, labels=operation_counts.index, autopct="%1.1f%%", startangle=90)
plt.title("Распределение операций")

plt.tight_layout()
plt.show()