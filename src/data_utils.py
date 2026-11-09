# src/data_utils.py
import pandas as pd

URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"

COLS_RU = {"gender": "Пол", "SeniorCitizen": "Пенсионер", "Partner": "Есть партнёр",
           "Dependents": "Есть иждивенцы", "tenure": "Стаж", "PhoneService": "Телефония",
           "MultipleLines": "Несколько линий", "InternetService": "Интернет",
           "OnlineSecurity": "Онлайн-защита", "OnlineBackup": "Облачный бэкап",
           "DeviceProtection": "Защита устройства", "TechSupport": "Техподдержка",
           "StreamingTV": "Стриминг ТВ", "StreamingMovies": "Стриминг кино",
           "Contract": "Контракт", "PaperlessBilling": "Электронный счёт",
           "PaymentMethod": "Способ оплаты", "MonthlyCharges": "Платёж в месяц",
           "TotalCharges": "Всего оплачено", "Churn": "Отток"}

VALUES_RU = {"Yes": "Да", "No": "Нет", "No internet service": "Нет интернета",
             "No phone service": "Нет телефонии", "Female": "Женский", "Male": "Мужской",
             "Fiber optic": "Оптоволокно", "Month-to-month": "Помесячный",
             "One year": "Годовой", "Two year": "Двухлетний",
             "Electronic check": "Электронный чек", "Mailed check": "Чек по почте",
             "Bank transfer (automatic)": "Банковский перевод (авто)",
             "Credit card (automatic)": "Кредитная карта (авто)"}

def load_and_clean() -> pd.DataFrame:
    """Загружает данные, очищает типы и переводит на русский."""
    df = pd.read_csv(URL).set_index("customerID")
    
    # Очистка TotalCharges
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)
    
    # Перевод таргета и бинарных
    df["Churn"] = (df["Churn"] == "Yes").astype("int8")
    df["SeniorCitizen"] = df["SeniorCitizen"].astype("int8")
    
    # Перевод столбцов и значений
    df = df.rename(columns=COLS_RU)
    for c in df.select_dtypes(exclude="number").columns:
        df[c] = df[c].replace(VALUES_RU).astype("category")
        
    # Оптимизация памяти
    df["Стаж"] = df["Стаж"].astype("int8")
    df[["Платёж в месяц", "Всего оплачено"]] = df[["Платёж в месяц", "Всего оплачено"]].astype("float32")
    
    return df