from pydantic import BaseModel
from typing import Optional


class ProjectCreateSchema(BaseModel):

    name: str
    description: Optional[str] = None


class ProjectUpdateSchema(BaseModel):

    name: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None


class ProjectResponseSchema(BaseModel):

    id: int
    name: str
    description: Optional[str]
    active: bool
    organization_id: int

    class Config:
        from_attributes = True