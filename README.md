# 📊 Прогнозирование оттока клиентов телеком-оператора (Telco Churn)

Учебный проект **Case 02 — Telco Churn** посвящён анализу клиентской базы телеком-оператора и прогнозированию оттока клиентов (`Churn`) методами машинного обучения.

В проекте предусмотрены разведочный анализ данных (EDA), подготовка признаков, построение и сравнение моделей, анализ качества классификации и интерпретация факторов риска. Цель — определить клиентов с повышенной вероятностью оттока и сформировать основу для решений по их удержанию.

## 🔗 Ссылки

- **Репозиторий:** https://github.com/zenith305/Case_02_Telco_Churn
- **Предзащита — открыть в Google Colab:** https://colab.research.google.com/github/zenith305/Case_02_Telco_Churn/blob/main/notebooks/01_predefense.ipynb
- **Исходный CSV на GitHub:** https://github.com/zenith305/Case_02_Telco_Churn/blob/main/data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv
- **Прямая ссылка на CSV (Raw):** https://raw.githubusercontent.com/zenith305/Case_02_Telco_Churn/main/data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv

> Ссылки на Colab открывают опубликованные в ветке `main` версии ноутбуков. Изменения, сделанные только в личной копии Colab, не попадают на GitHub автоматически.

## 📁 Структура проекта

```text
Case_02_Telco_Churn/
├── archive/                   # Архивные версии ноутбуков
├── data/
│   └── raw/
│       └── WA_Fn-UseC_-Telco-Customer-Churn.csv
├── notebooks/
│   ├── 01_predefense.ipynb    # Предзащита: анализ данных и базовые модели
│   └── 02_defense.ipynb       # Защита: модели, оценка и интерпретация
├── reports/                   # Отчёты и результаты анализа
├── src/
│   └── data_utils.py         # Загрузка и подготовка данных
├── .gitignore
├── README.md
└── requirements.txt
```

Структура показывает основные файлы; дополнительные скрипты и отчёты могут присутствовать в репозитории. Обученные модели и архивы ZIP исключены правилами `.gitignore` и не требуются для загрузки исходного CSV.

## 📦 Данные

Используется учебный набор **Telco Customer Churn**: 7 043 строки и 21 исходный столбец. Целевая переменная — `Churn` (факт ухода клиента). Данные включают характеристики клиента, подключённые услуги, параметры договора и платежей.

Проверка прямой загрузки в Python / Google Colab:

```python
import pandas as pd

CSV_URL = (
    "https://raw.githubusercontent.com/"
    "zenith305/Case_02_Telco_Churn/main/"
    "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
)

df = pd.read_csv(CSV_URL)
print(df.shape)  # Ожидается: (7043, 21)
```

Это проверка **исходного** CSV. Для основного анализа используйте подготовку данных, реализованную в `src/data_utils.py`, чтобы сохранить согласованность признаков и типов.

## ☁️ Запуск в Google Colab

1. Откройте ноутбук по ссылке из раздела «Ссылки».
2. Подключите среду выполнения Colab.
3. Если ноутбук требует файлов из `src/` и `data/`, сначала выполните ячейку подготовки проекта. Для неё можно использовать следующий код:

```python
from pathlib import Path
import os
import subprocess
import sys

REPO_URL = "https://github.com/zenith305/Case_02_Telco_Churn.git"
PROJECT_ROOT = Path("/content/Case_02_Telco_Churn")

if not (PROJECT_ROOT / ".git").is_dir():
    subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, str(PROJECT_ROOT)],
        check=True,
    )
else:
    subprocess.run(
        ["git", "-C", str(PROJECT_ROOT), "pull", "--ff-only"],
        check=True,
    )

for relative_path in (
    "src/data_utils.py",
    "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv",
):
    if not (PROJECT_ROOT / relative_path).is_file():
        raise FileNotFoundError(f"Не найден файл: {relative_path}")

os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

print("Проект готов к выполнению:", PROJECT_ROOT)
```

4. Запустите остальные ячейки по порядку или выберите **«Среда выполнения → Выполнить все»**, если подготовительная ячейка уже встроена в ноутбук.

Для запуска требуется интернет. При изменении файлов внутри клонированной папки `git pull --ff-only` может потребовать отдельного разрешения локальных изменений.

## 💻 Запуск локально в VS Code

Требуются **Python 3** и **Git**. Рекомендуется отдельное виртуальное окружение.

```powershell
git clone https://github.com/zenith305/Case_02_Telco_Churn.git
cd Case_02_Telco_Churn
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Откройте папку проекта в VS Code, выберите интерпретатор `.venv` и запустите нужный ноутбук из `notebooks/`. В Linux/macOS команда активации окружения: `source .venv/bin/activate`.

## 🧪 Этапы анализа

1. Загрузка и проверка исходных данных.
2. Очистка и подготовка признаков.
3. Разведочный анализ данных (EDA).
4. Построение базовой модели и сравнение подходов к классификации.
5. Оценка метрик, настройка порога классификации и интерпретация результатов.
6. Формирование выводов для задачи удержания клиентов.

Конкретные результаты, метрики и графики приведены в соответствующих ноутбуках; README не фиксирует значения метрик, которые могут измениться при повторном обучении.

## 🔒 Публикация и воспроизводимость

- Исходный CSV хранится в `data/raw/` и доступен по прямой ссылке.
- Файлы `.pkl`, `.joblib`, ZIP-архивы, виртуальные окружения и локальные секреты не следует публиковать.
- Перед публикацией отчётов из `reports/` убедитесь, что они не содержат конфиденциальной информации.
- Для воспроизводимости используйте версии библиотек из `requirements.txt` и выполняйте ячейки последовательно.

## 📌 Назначение

Проект подготовлен для учебной предзащиты и защиты по задаче прогнозирования оттока клиентов. Результаты являются аналитическими и не должны использоваться как единственное основание для решений в отношении реальных клиентов.
