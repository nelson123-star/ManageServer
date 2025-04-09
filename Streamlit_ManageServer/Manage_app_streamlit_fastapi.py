# ВАЖНО!!! ЗАПУСКАТЬ ЧЕРЕЗ ТЕРМИНАЛ. команда: streamlit run Manage_app_streamlit_fastapi.py

import psutil
import streamlit as st
import requests
import time
import pandas as pd

# URL FastAPI-приложения
API_URL = "http://localhost:8082"


# Функция для получения данных CPU и RAM и списка запущенных процессов
def get_metrics():
    # CPU и RAM
    cpu_percent = psutil.cpu_percent(interval=1)
    ram_percent = psutil.virtual_memory().percent

    # Список процессов
    processes = {}
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes[proc.info['name']] = {
            "cpu_percent": proc.info['cpu_percent'],
            "memory_percent": proc.info['memory_percent']
        }

    return {
        "cpu_percent": cpu_percent,
        "ram_percent": ram_percent,
        "processes": processes
    }


# Функция для управления службами на Windows
def manage_service(service_name, action):
    try:
        response = requests.post(f"{API_URL}/service/{action}", json={"service_name": service_name})
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to service")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the server: {e}")
        return None


# Основная функция для отображения веб-интерфейса
def main():
    st.set_page_config(page_title="Server Monitor", page_icon="🖥️", layout="wide")
    st.title("🖥️ Server Monitoring")
    st.markdown("---")

    # Управление службами
    st.subheader("Управление службами")
    service_name = st.text_input("Ввод названия службы:")
    action = st.selectbox("Выберете действие для службы", ["start", "stop", "state"])
    if st.button(f"{action} service"):
        result = manage_service(service_name, action)
        st.success(result)

    st.markdown("---")

    # Контейнеры для обновления значений
    cpu_metric = st.empty()
    ram_metric = st.empty()
    task_table = st.empty()

    st.markdown("---")

    # Цикл для обновления данных
    while True:
        # Получаем данные с сервера
        metrics = get_metrics()
        if metrics:
            # Обновление CPU
            with cpu_metric:
                st.subheader("CPU Usage")
                st.metric(label="CPU", value=f"{metrics['cpu_percent']}%")

            # Обновление RAM
            with ram_metric:
                st.subheader("RAM Usage")
                st.metric(label="RAM", value=f"{metrics['ram_percent']}%")

            # Преобразуем процессы в DataFrame
            processes = []
            for name, info in metrics['processes'].items():
                processes.append({
                    "Name": name,
                    "CPU (%)": info['cpu_percent'],
                    "RAM (%)": info['memory_percent']
                })
            task_df = pd.DataFrame(processes)

            # Таблица процессов
            with task_table:
                st.subheader("Running Processes")
                st.dataframe(task_df, use_container_width=True)

        # Обновление данных (каждые 2 секунды для корректности)
        time.sleep(2)


if __name__ == "__main__":
    main()


