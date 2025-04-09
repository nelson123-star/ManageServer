from pydantic import BaseModel
from typing import Dict

class SystemMetrics(BaseModel):
    cpu_percent: float
    ram_percent: float
    processes: Dict[str, float]

class Service (BaseModel):
    service_name: str

    class Config:
        schema_extra = {
            "example": {
                "service_name": "askb_rp111"
            }
        }