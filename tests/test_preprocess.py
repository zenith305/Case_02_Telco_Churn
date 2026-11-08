import pandas as pd
import os

def test_cleaned_data_exists():
    """Проверяем, что файл с очищенными данными существует"""
    path = 'data/processed/cleaned_data.csv'
    assert os.path.exists(path), f"Файл {path} не найден!"

def test_total_charges_has_no_nan():
    """Проверяем, что в колонке TotalCharges нет пустых значений (NaN)"""
    df = pd.read_csv('data/processed/cleaned_data.csv')
    
    # В исходном датасете были пробелы, из-за которых pandas читал колонку как строку.
    # После нашей очистки там должны быть только числа.
    assert pd.api.types.is_numeric_dtype(df['TotalCharges']), "Колонка TotalCharges должна быть числовой!"
    assert df['TotalCharges'].isna().sum() == 0, "В колонке TotalCharges остались пропуски!"

def test_no_customer_id():
    """Проверяем, что мы удалили ненужный customerID"""
    df = pd.read_csv('data/processed/cleaned_data.csv')
    assert 'customerID' not in df.columns, "Колонка customerID должна быть удалена!"