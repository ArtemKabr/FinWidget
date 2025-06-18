import shutil
from pathlib import Path


def copy_operations_file() -> None:
    source = Path("C:/Users/HP/Desktop/operations3.xlsx")
    destination_dir = Path("data")
    destination = destination_dir / source.name

    destination_dir.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy(source, destination)
        normalized = str(destination).replace("\\", "/")
        print(f"✅ Файл скопирован в: {normalized}")

    except FileNotFoundError:
        normalized = str(source).replace("\\", "/")
        print(f"❌ Файл не найден: {normalized}")


if __name__ == "__main__":
    copy_operations_file()
