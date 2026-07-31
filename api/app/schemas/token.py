from pydantic import BaseModel


class TokenCreateSchema(BaseModel):

    name: str

    project_id: int