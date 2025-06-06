from datetime import date, datetime

import httpx
import streamlit as st

st.set_page_config(page_title="FinWidget | Дашборд", layout="wide")

# 👇 Интерфейс выбора даты и времени
st.title("📊 Анализ транзакций FinWidget")
date_input = st.date_input("Выберите дату", value=datetime.today().date())
time_input = st.time_input("Выберите время", value=datetime.now().time())

dt = datetime.combine(date_input, time_input)
dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")

# 📡 Получаем данные с /home
with st.spinner("Загружаем данные..."):
    try:
        response = httpx.get("http://127.0.0.1:8000/home", params={"date": dt_str})
        data = response.json()
    except Exception as e:
        st.error(f"Ошибка при подключении к API: {e}")
        st.stop()

# 👋 Приветствие
st.header(data["greeting"])

# 💳 Карты
st.subheader("💳 Расходы по картам")
for card in data["cards"]:
    st.metric(
        label=f"Карта *{card['last_digits']}", value=f"{card['total_spent']} ₽", delta=f"{card['cashback']} ₽ кэшбэк"
    )

# 📌 Топ-5 транзакций
st.subheader("🔥 Топ-5 транзакций")
st.table(data["top_transactions"])

# 💱 Курсы валют
st.subheader("💱 Курсы валют")
st.json(data["currency_rates"])

# 📈 Котировки акций
st.subheader("📈 Акции")
st.json(data["stock_prices"])

# 🧾 Отчёт
st.divider()
st.subheader("📥 Сформировать Excel-отчёт")

# Выбор фильтров
status = st.selectbox("Статус операции", ["", "OK", "ERROR"])
currency = st.selectbox("Валюта операции", ["", "RUB", "USD", "EUR"])
start_date = st.date_input("Дата начала", value=date.today().replace(day=1))
end_date = st.date_input("Дата окончания", value=date.today())

# Кнопка генерации отчёта
if st.button("📊 Сформировать отчёт"):
    try:
        params = {}
        if status:
            params["status"] = status
        if currency:
            params["currency"] = currency
        if start_date:
            params["start"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end"] = end_date.strftime("%Y-%m-%d")

        report_resp = httpx.get("http://127.0.0.1:8000/report", params=params)
        result = report_resp.json()
        file_path = result["message"].split("в ")[-1]

        st.success("Отчёт успешно создан.")
        st.download_button(
            label="📎 Скачать отчёт",
            data=open(file_path, "rb").read(),
            file_name="report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    except Exception as e:
        st.error(f"Ошибка при создании отчёта: {e}")
