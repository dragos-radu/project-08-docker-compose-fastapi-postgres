from fastapi import FastAPI, HTTPException, status

from app.database import Base, engine

from app.models import Project, ProjectCreate, ProjectUpdate
from app.store import (
    create_project,
    delete_project,
    get_project,
    list_projects,
    update_project,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevOps Projects API",
    description=(
        "A local-first FastAPI CRUD API for managing DevOps portfolio projects. "
        "The API uses in-memory storage, includes automated tests and is prepared "
        "for future Docker and cloud deployment scenarios."
    ),
    version="1.0.0",
    contact={
        "name": "Dragos Radu",
        "url": "https://github.com/dragos-radu",
    },
    license_info={
        "name": "MIT",
    },
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/projects", response_model=list[Project])
def get_projects():
    return list_projects()


@app.get("/projects/{project_id}", response_model=Project)
def get_project_by_id(project_id: int):
    project = get_project(project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return project


@app.post("/projects", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project_endpoint(project: ProjectCreate):
    return create_project(project)


@app.put("/projects/{project_id}", response_model=Project)
def replace_project(project_id: int, project_data: ProjectUpdate):
    project = update_project(project_id, project_data)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return project


@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_project(project_id: int):
    deleted = delete_project(project_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return None
