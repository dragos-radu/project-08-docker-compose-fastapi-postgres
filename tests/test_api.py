from fastapi.testclient import TestClient

from app.store import projects_store
from app.main import app

client = TestClient(app)


def setup_function():
    projects_store.clear()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_projects_empty():
    response = client.get("/projects")
    assert response.status_code == 200
    assert response.json() == []


def test_create_project():
    project_payload = {
        "name": "Nginx Static Site",
        "description": "Deploy a static website using Nginx on a Linux environment.",
        "status": "completed",
    }

    response = client.post("/projects", json=project_payload)
    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == project_payload["name"]
    assert data["description"] == project_payload["description"]
    assert data["status"] == project_payload["status"]


def test_get_project_by_id():
    project_payload = {
        "name": "Nginx Load Balancer",
        "description": "Configure Nginx as a load balancer for backend servers.",
        "status": "completed",
    }

    create_response = client.post("/projects", json=project_payload)
    project_id = create_response.json()["id"]

    response = client.get(f"/projects/{project_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == project_id
    assert data["name"] == project_payload["name"]


def test_get_project_by_id_not_found():
    response = client.get("/projects/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_update_project():
    project_payload = {
        "name": "Consul Service Discovery",
        "description": "Configure service discovery using Consul and Nginx.",
        "status": "in-progress",
    }

    create_response = client.post("/projects", json=project_payload)
    project_id = create_response.json()["id"]

    update_payload = {
        "name": "Consul Service Discovery",
        "description": "Configure dynamic service discovery using Consul, Consul Template and Nginx.",
        "status": "completed",
    }

    response = client.put(f"/projects/{project_id}", json=update_payload)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == project_id
    assert data["description"] == update_payload["description"]
    assert data["status"] == "completed"


def test_update_project_not_found():
    update_payload = {
        "name": "Missing Project",
        "description": "This project does not exist.",
        "status": "planned",
    }

    response = client.put("/projects/999", json=update_payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}


def test_delete_project():
    project_payload = {
        "name": "FastAPI CRUD API",
        "description": "Build a local-first API with FastAPI.",
        "status": "in-progress",
    }

    create_response = client.post("/projects", json=project_payload)
    project_id = create_response.json()["id"]

    response = client.delete(f"/projects/{project_id}")

    assert response.status_code == 204

    get_response = client.get(f"/projects/{project_id}")

    assert get_response.status_code == 404


def test_delete_project_not_found():
    response = client.delete("/projects/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Project not found"}
