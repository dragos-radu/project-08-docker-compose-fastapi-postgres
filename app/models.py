from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    status: str = Field(default="planned", max_length=50)


class ProjectUpdate(BaseModel):
    name: str = Field(None, min_length=3, max_length=100)
    description: str = Field(None, min_length=10, max_length=500)
    status: str = Field(None, max_length=50)


class Project(ProjectCreate):
    id: int
