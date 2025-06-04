from pathlib import Path

import pandas as pd

file_path = Path("data/operations3.xlsx")  # путь к файлу

try:
    df = pd.read_excel(file_path, dtype=str).fillna("")
    preview = df.head(2).to_dict(orient="records")
    print("Первые 2 строки Excel-файла:")
    for row in preview:
        print(row)
except Exception as e:
    print(f"Ошибка при чтении Excel-файла: {e}")
