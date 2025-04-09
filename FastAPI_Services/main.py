from fastapi import FastAPI
import uvicorn
from serivces import service_router

fastapi = FastAPI()

fastapi.include_router(service_router)

if __name__ == '__main__':
    uvicorn.run(app="main:fastapi", host="localhost", port=8082, reload=True)


