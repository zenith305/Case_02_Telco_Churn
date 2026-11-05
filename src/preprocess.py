import os
import pandas as pd


# 1. Загрузка данных
raw_path = 'data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv'
df = pd.read_csv(raw_path)

print("Исходный размер данных:", df.shape)

# 2. Очистка TotalCharges
# В этом датасете там есть пустые строки (пробелы). Превращаем их в NaN (пустоту).
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Заполняем пропуски нулем. Так как это новые клиенты (tenure=0), ставим 0.
df['TotalCharges'] = df['TotalCharges'].fillna(0)

# 3. Удаление ненужных колонок
# customerID не несет смысла для модели
df = df.drop(columns=['customerID'])

print("Размер после очистки:", df.shape)

# 4. Сохранение очищенных данных
os.makedirs('data/processed', exist_ok=True)
processed_path = 'data/processed/cleaned_data.csv'
df.to_csv(processed_path, index=False)

print(f"Очищенные данные сохранены в {processed_path}")