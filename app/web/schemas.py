from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    api: bool
    database: bool
