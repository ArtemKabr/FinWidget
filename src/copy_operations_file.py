import shutil
from pathlib import Path


def copy_operations_file() -> None:
    """
    Копирует файл `operations.xls` с рабочего стола в папку `data/` проекта.
    """
    source = Path("C:/Users/HP/Desktop/operations3.xlsx")
    destination_dir = Path("data")
    destination = destination_dir / source.name

    destination_dir.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy(source, destination)
        print(f"✅ Файл скопирован в: {destination}")
    except FileNotFoundError:
        print(f"❌ Файл не найден: {source}")


if __name__ == "__main__":
    copy_operations_file()
