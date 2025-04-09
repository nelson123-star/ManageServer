import os, subprocess
from fastapi import APIRouter
from model import Service

service_router = APIRouter(prefix="/service", tags=["Service"])

# Эндпоинт для остановки службы
@service_router.post("/stop")
async def stop_service(service: Service):
    os.system(f"sc stop {service.service_name}")
    return {"message": f"Остановка службы: {service.service_name}"}

# Эндпоинт для запуска службы
@service_router.post("/start")
async def start_service(service: Service):
    os.system(f"sc start {service.service_name}")
    return {"message": f"Запуск службы: {service.service_name}"}

# Эндпоинт для получения службы
@service_router.post("/state")
async def get_state_service(service: Service):
    conf_list = subprocess.check_output(f"sc query {service.service_name}", shell=True)
    # conf_list = conf_list.decode('Windows-1251')
    conf_list = conf_list.decode('CP866')
    # conf_list = conf_list.decode('utf-8')
    conf_list = str(conf_list)
    result = conf_list.split("\r\n")
    state_service = ''
    for iter in result:
        if (iter.find('STATE') != -1 or iter.find('Состояние') != -1):
            state_service = iter
            break
    state_service = state_service.strip().split(":")
    state_list = []
    for iter in state_service:
        iter = iter.strip()
        state_list.append(iter)

    # Если состояние строка
    state_service = ":".join(state_list)

    state_service = state_service.split(" ")[-1]

    return {"Состояние службы":state_service}

