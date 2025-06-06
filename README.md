# FinWidget

Анализ банковских транзакций: веб-интерфейс, REST API и отчёты из Excel-файлов.  
Проект реализован в рамках курсовой работы.

---

## 📂 Описание

**FinWidget** — это аналитическая система для работы с банковскими транзакциями:

- Загрузка Excel-файла
- REST API на FastAPI
- Генерация отчётов по фильтрам
- Визуализация в Streamlit-интерфейсе

---

## 🚀 Реализованные возможности

### 🌐 API-эндпоинты

| Метод | Путь              | Описание                                    |
|-------|-------------------|---------------------------------------------|
| GET   | `/home`           | Главная аналитика: приветствие, карты, топ |
| GET   | `/operations`     | Фильтрация транзакций по статусу/валюте    |
| GET   | `/categories`     | Список уникальных категорий                 |
| GET   | `/summary`        | Статистика по статусам операций            |
| GET   | `/top-categories` | Топ N категорий по расходам                |
| GET   | `/report`         | Генерация Excel-отчёта по фильтрам         |

---

## 🖥 Веб-интерфейс (Streamlit)

Реализован дашборд `/home`:

- 👋 Приветствие по времени
- 💳 Траты по картам и кэшбэк
- 🔝 Топ-5 транзакций
- 💱 Курсы валют (фиктивно)
- 📈 Котировки акций
- 📥 Генерация и скачивание Excel-отчёта по дате, валюте и статусу
- 📊 Диаграмма расходов по категориям

---

## ⚙️ Сервисы

- 📤 Конвертация валют (USD, EUR → RUB)
- 📁 Загрузка Excel-файла `operations3.xlsx`
- 📎 Загрузка настроек из `user_settings.json`
- 📆 Работа с диапазоном дат, форматами
- 🧾 Генерация отчёта `report.xlsx`

---

## 🧪 Тестирование

- `pytest`
- `mock`, `patch`, `parametrize`, `fixtures`
- Команда:

```bash
poetry run pytest --cov=src --cov-report=term-missing
✅ Покрытие: 88%+

🧰 Pre-commit хуки
В проект настроены хуки:

✅ black

✅ isort

✅ flake8

✅ mypy

🧭 Установка и запуск проекта
1. Установка Poetry и зависимостей

pip install poetry
poetry install
2. Настройка .env
Создай .env по шаблону:


CURRENCY_API_KEY=your_api_key_here
3. Запуск FastAPI

poetry run uvicorn src.main:app --reload
📄 Swagger UI: http://127.0.0.1:8000/docs

4. Запуск Streamlit-интерфейса

poetry run streamlit run src/streamlit_app.py
🌐 Откроется по адресу: http://localhost:8501

🧾 Исходные данные
data/operations3.xlsx — транзакции

user_settings.json — список валют и тикеров

data/report.xlsx — отчёт, генерируемый из фильтров

🧠 Автор
Artem Kabritskii
📧 artemkabr7@gmail.com
💻 GitHub: https://github.com/ArtemKabr/FinWidget