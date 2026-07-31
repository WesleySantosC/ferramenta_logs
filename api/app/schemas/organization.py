from pydantic import BaseModel


class OrganizationCreateSchema(BaseModel):
    name: str
    slug: str


class OrganizationUpdateSchema(BaseModel):
    name: str
    slug: str


class OrganizationResponseSchema(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True