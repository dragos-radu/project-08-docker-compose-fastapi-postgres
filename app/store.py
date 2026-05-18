from app.models import Project, ProjectCreate, ProjectUpdate

projects_store: dict[int, Project] = {}
next_project_id = 1


def list_projects() -> list[Project]:
    return list(projects_store.values())


def get_project(project_id: int) -> Project | None:
    return projects_store.get(project_id)


def create_project(project_data: ProjectCreate) -> Project:
    global next_project_id

    project = Project(
        id=next_project_id,
        name=project_data.name,
        description=project_data.description,
        status=project_data.status,
    )

    projects_store[next_project_id] = project
    next_project_id += 1

    return project


def update_project(project_id: int, project_data: ProjectUpdate) -> Project | None:
    if project_id not in projects_store:
        return None

    update_project = Project(
        id=project_id,
        name=project_data.name,
        description=project_data.description,
        status=project_data.status,
    )

    projects_store[project_id] = update_project

    return update_project


def delete_project(project_id: int) -> bool:
    if project_id not in projects_store:
        return False

    del projects_store[project_id]

    return True
