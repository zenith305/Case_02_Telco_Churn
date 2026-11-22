📊 Прогнозирование оттока клиентов телеком-оператора (Telco Churn)

Case_02_Telco_Churn/
├── models/
│   └── final_churn_model.pkl # Обученная модель (Pipeline)
├── notebooks/
│   ├── 01_predzashita.ipynb  # EDA и Baseline (LogReg)
│   └── 02_zashita.ipynb      # Сравнение моделей, Threshold, SHAP и бизнес-выводы
├── reports/
│   └── shap_summary_final.png # Итоговый график факторов риска
├── src/
│   ├── data_utils.py         # Скрипт загрузки и очистки данных
│   └── preprocess.py         # Вспомогательный скрипт
├── .gitignore                # Исключения для Git
├── README.md                 # Описание проекта
└── requirements.txt          # Зависимости
```
