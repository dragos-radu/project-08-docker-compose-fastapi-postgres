from app.database import SessionLocal
from app.db_models import ProjectDB
from app.models import Project, ProjectCreate, ProjectUpdate


def db_project_to_project(db_project: ProjectDB) -> Project:
    return Project(
        id=db_project.id,
        name=db_project.name,
        description=db_project.description,
        status=db_project.status,
    )


def list_projects() -> list[Project]:
    with SessionLocal() as db:
        projects = db.query(ProjectDB).order_by(ProjectDB.id).all()
        return [db_project_to_project(project) for project in projects]


def get_project(project_id: int) -> Project | None:
    with SessionLocal() as db:
        project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()

        if project is None:
            return None

        return db_project_to_project(project)


def create_project(project_data: ProjectCreate) -> Project:
    with SessionLocal() as db:
        project = ProjectDB(
            name=project_data.name,
            description=project_data.description,
            status=project_data.status,
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        return db_project_to_project(project)


def update_project(project_id: int, project_data: ProjectUpdate) -> Project | None:
    with SessionLocal() as db:
        project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()

        if project is None:
            return None

        project.name = project_data.name
        project.description = project_data.description
        project.status = project_data.status

        db.commit()
        db.refresh(project)

        return db_project_to_project(project)


def delete_project(project_id: int) -> bool:
    with SessionLocal() as db:
        project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()

        if project is None:
            return False

        db.delete(project)
        db.commit()

        return True