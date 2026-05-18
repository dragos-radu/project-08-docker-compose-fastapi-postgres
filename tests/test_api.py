from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_project():
    response = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "description": "This is a test project created with pytest.",
            "status": "planned",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["name"] == "Test Project"
    assert data["description"] == "This is a test project created with pytest."
    assert data["status"] == "planned"


def test_list_projects():
    response = client.get("/projects")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_project_by_id():
    create_response = client.post(
        "/projects",
        json={
            "name": "Read Test Project",
            "description": "This project is created before reading it by id.",
            "status": "in-progress",
        },
    )

    project_id = create_response.json()["id"]

    response = client.get(f"/projects/{project_id}")

    assert response.status_code == 200
    assert response.json()["id"] == project_id
    assert response.json()["name"] == "Read Test Project"


def test_update_project():
    create_response = client.post(
        "/projects",
        json={
            "name": "Old Project Name",
            "description": "This project will be updated by the test.",
            "status": "planned",
        },
    )

    project_id = create_response.json()["id"]

    response = client.put(
        f"/projects/{project_id}",
        json={
            "name": "Updated Project Name",
            "description": "This project was updated by the test.",
            "status": "done",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == project_id
    assert response.json()["name"] == "Updated Project Name"
    assert response.json()["status"] == "done"


def test_delete_project():
    create_response = client.post(
        "/projects",
        json={
            "name": "Delete Test Project",
            "description": "This project will be deleted by the test.",
            "status": "planned",
        },
    )

    project_id = create_response.json()["id"]

    delete_response = client.delete(f"/projects/{project_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/projects/{project_id}")

    assert get_response.status_code == 404
