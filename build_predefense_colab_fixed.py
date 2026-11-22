#!/usr/bin/env python3
"""Собирает автономный пакет предзащиты для Google Colab, не меняя исходники."""
import ast
import copy
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTEBOOK_CANDIDATES = ("01_predefense.ipynb", "Предзащита.ipynb", "01_predefense_colab.ipynb")
CSV_NAME = "WA_Fn-UseC_-Telco-Customer-Churn.csv"
CSV_PATH = Path("data/raw") / CSV_NAME
ARCHIVE_NAME = "Предзащита_Colab.zip"
REQUIRED_COLUMNS = {"customerID", "TotalCharges", "Churn", "SeniorCitizen", "tenure", "MonthlyCharges"}
REQUIREMENTS = "numpy\npandas\nmatplotlib\nseaborn\nscikit-learn\n"

SETUP = '''from pathlib import Path
import os
import sys
import zipfile

# В Colab сначала откройте этот ноутбук, затем запустите эту ячейку.
# При необходимости появится окно выбора ZIP-файла.
ARCHIVE_NAME = "Предзащита_Colab.zip"
CSV_REL = Path("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
PROJECT_ROOT = Path.cwd().resolve()
if not (PROJECT_ROOT / "src/data_utils.py").is_file() or not (PROJECT_ROOT / CSV_REL).is_file():
    if "google.colab" in sys.modules:
        archive_path = Path("/content") / ARCHIVE_NAME
        if not archive_path.is_file():
            from google.colab import files
            print("Загрузите файл Предзащита_Colab.zip")
            uploaded = files.upload()
            if ARCHIVE_NAME not in uploaded:
                raise FileNotFoundError("Не загружен файл " + ARCHIVE_NAME)
        PROJECT_ROOT = Path("/content/Предзащита_проект")
        PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive_path) as archive:
            expected = {
                "01_predefense_colab.ipynb", "requirements.txt",
                "src/data_utils.py", str(CSV_REL).replace("\\\\", "/")
            }
            if not expected.issubset(set(archive.namelist())):
                raise FileNotFoundError("В ZIP отсутствуют необходимые файлы")
            for name in expected:
                target = PROJECT_ROOT / name
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(name) as source, target.open("wb") as dest:
                    import shutil
                    shutil.copyfileobj(source, dest)
    else:
        raise FileNotFoundError("Откройте ноутбук из корня проекта, где есть src/ и data/raw/")
if not (PROJECT_ROOT / CSV_REL).is_file():
    raise FileNotFoundError("CSV отсутствует: " + str(PROJECT_ROOT / CSV_REL))
os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
print("Папка проекта:", PROJECT_ROOT)
print("CSV найден:", PROJECT_ROOT / CSV_REL)
'''

def find_source(name):
    direct = ROOT / name
    nested = ROOT / "src" / name
    for path in (nested, direct):
        if path.is_file():
            return path
    raise FileNotFoundError(f"Не найден {name} (ожидается в src/ или корне проекта)")


def notebook_source():
    for folder in (ROOT / "notebooks", ROOT):
        for name in NOTEBOOK_CANDIDATES:
            path = folder / name
            if path.is_file():
                return path
    raise FileNotFoundError("Нет исходного ноутбука в notebooks/ или корне проекта: " + ", ".join(NOTEBOOK_CANDIDATES))


def patch_loader(source):
    if 'def load_and_clean' not in source:
        raise ValueError("В data_utils.py отсутствует load_and_clean()")
    if 'pd.read_csv(URL)' in source:
        source = source.replace('pd.read_csv(URL)', 'pd.read_csv(DATA_FILE)', 1)
    elif 'pd.read_csv(DATA_FILE)' not in source:
        raise ValueError("Неизвестный способ чтения CSV; автоматическое изменение остановлено")
    if 'DATA_FILE = ' not in source:
        source = 'from pathlib import Path\nDATA_FILE = Path(__file__).resolve().parent.parent / "data" / "raw" / "' + CSV_NAME + '"\n\n' + source
    ast.parse(source)
    return source


def patch_notebook(raw):
    notebook = copy.deepcopy(raw)
    cells = notebook.get('cells', [])
    setup_index = next((i for i, c in enumerate(cells) if c.get('cell_type') == 'code' and
                        ('PROJECT_ROOT =' in ''.join(c.get('source', [])) or
                         'ARCHIVE_NAME = "Предзащита_Colab.zip"' in ''.join(c.get('source', [])))), None)
    if setup_index is None:
        raise ValueError("Не найдена ячейка настройки PROJECT_ROOT: изменение остановлено")
    cells[setup_index]['source'] = SETUP.splitlines(keepends=True)
    for cell in cells:
        if cell.get('cell_type') == 'code':
            code = ''.join(cell.get('source', []))
            ast.parse(code)
            cell['execution_count'] = None
            cell['outputs'] = []
    return notebook


def main():
    source_nb = notebook_source()
    loader_path = find_source('data_utils.py')
    csv_path = ROOT / CSV_PATH
    if not csv_path.is_file():
        raise FileNotFoundError(f"Поместите CSV сюда: {csv_path}")
    import csv
    with csv_path.open('r', encoding='utf-8-sig', newline='') as file:
        reader = csv.reader(file)
        headers = set(next(reader))
    missing = REQUIRED_COLUMNS - headers
    if missing:
        raise ValueError(f"В CSV нет обязательных столбцов: {sorted(missing)}")
    notebook = patch_notebook(json.loads(source_nb.read_text(encoding='utf-8-sig')))
    loader = patch_loader(loader_path.read_text(encoding='utf-8-sig'))
    archive_path = ROOT / ARCHIVE_NAME
    if archive_path.exists():
        raise FileExistsError(f"Архив уже существует: {archive_path}. Переименуйте его для сохранения предыдущей версии")
    with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        z.writestr('01_predefense_colab.ipynb', json.dumps(notebook, ensure_ascii=False, indent=1))
        z.writestr('src/data_utils.py', loader)
        z.writestr('requirements.txt', REQUIREMENTS)
        z.write(csv_path, str(CSV_PATH).replace('\\', '/'))
    with zipfile.ZipFile(archive_path) as z:
        if z.testzip() is not None:
            raise RuntimeError("ZIP повреждён")
        print('ZIP создан:', archive_path)
        for item in z.infolist():
            print(f'  {item.filename} ({item.file_size} байт)')
    print('Исходные файлы не изменены. Для проверки загрузите ZIP в чат.')

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, SyntaxError, KeyError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        print(f'ОШИБКА: {exc}', file=sys.stderr)
        sys.exit(1)
