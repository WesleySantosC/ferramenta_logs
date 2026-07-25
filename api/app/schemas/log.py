from pydantic import BaseModel
from datetime import datetime
from typing import List


class LogSchema(BaseModel):

    application: str
    service: str
    level: str
    message: str
    environment: str
    request_id: str | None = None
    context: dict | None = None


class LogResponse(BaseModel):

    id: int
    application: str
    service: str
    level: str
    message: str
    environment: str
    request_id: str | None
    context: dict | None
    created_at: datetime

    class Config:
        from_attributes = True

class LogListResponse(BaseModel):

    total: int
    page: int
    limit: int
    data: list[LogResponse]

class LogsBulkSchema(BaseModel):

    logs: list[LogSchema]