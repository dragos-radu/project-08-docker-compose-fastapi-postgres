# Project 08 – Docker Compose Multi-Container FastAPI App

## Overview

This project extends the FastAPI CRUD API created in Project 06 into a local multi-container application using Docker Compose.

The existing FastAPI application is reused as the API service, while a PostgreSQL database service is added as the first step toward replacing in-memory storage with persistent database storage.

This project demonstrates how to:

- Reuse an existing FastAPI application in a Docker Compose setup
- Define multiple services using Docker Compose
- Prepare a local API + database architecture using internal Docker networking
- Manage sensitive configuration through environment variables
- Prepare the project for future database persistence, monitoring, CI/CD, and Kubernetes

## Architecture

```text
Client / Browser / curl
        |
        v
[ FastAPI API Container ]
        |
        v
[ Docker Internal Network ]
        |
        v
[ PostgreSQL Database Container ]
        |
        v
[ Persistent Docker Volume ]
```

## Jira

### Epic

- **DEVOPS-34** – Build Multi-Container FastAPI App with Docker Compose

### Tasks

- **DEVOPS-35** – Prepare existing FastAPI project for Docker Compose
- **DEVOPS-36** – Add PostgreSQL service with Docker Compose
- **DEVOPS-37** – Replace in-memory storage with PostgreSQL persistence
- **DEVOPS-38** – Connect FastAPI service to PostgreSQL container
- **DEVOPS-39** – Update tests for database-backed API
- **DEVOPS-40** – Validate Docker Compose networking and persistence
- **DEVOPS-41** – Prepare structure for monitoring and future deployment
- **DEVOPS-42** – Update README.md and setup.md

## Goal

The goal of this project is to transform the existing FastAPI CRUD API from Project 06 into a multi-container local application.

At this stage, the project focuses only on the initial Docker Compose foundation. The API code from Project 06 is kept as the starting point, while the repository is prepared for a PostgreSQL database service, persistent volumes, internal networking, and environment-based configuration.

The project does not include AWS, Terraform, or Kubernetes in this phase.

## Tech Stack

- **Python** – Programming language
- **FastAPI** – Modern web framework for building APIs
- **PostgreSQL** – Relational database for persistent storage
- **Docker** – Containerization platform
- **Docker Compose** – Multi-container orchestration
- **SQLAlchemy** – ORM for database operations
- **Pytest** – Testing framework

## Project Status

In progress

## Implementation Details

### Prepare Existing FastAPI Project for Docker Compose

The existing FastAPI CRUD API from Project 06 was reused as the base application for this project.

Instead of recreating the Python code, the project was copied into a new repository dedicated to the Docker Compose multi-container setup. This keeps Project 06 focused on the standalone FastAPI API, while Project 08 focuses on container orchestration.

The initial Docker Compose foundation was added with two services:

- `api` for the FastAPI application
- `db` for the PostgreSQL database

The setup also introduced a persistent Docker volume for database data, an internal Docker network for service communication, and environment variable support using a local `.env` file.

Sensitive values are not stored directly in `docker-compose.yml`. Instead, they are defined in the `.env` file, which is included in `.gitignore` to prevent accidental commits of sensitive information.

### Add PostgreSQL Service with Docker Compose

A PostgreSQL database service was added as a separate Docker Compose service.

The database runs in its own container, uses environment variables from the local `.env` file, and stores data in a persistent Docker volume.

A healthcheck was configured using `pg_isready` so Docker Compose can detect when the database is ready to accept connections.

The service is connected to the internal Docker network, allowing the API service to communicate with it using the service name `db`.

### Replace In-Memory Storage with PostgreSQL Persistence

The previous in-memory dictionary from `store.py` was replaced with PostgreSQL-backed persistence.

A SQLAlchemy database connection was added, together with a dedicated database model for portfolio projects. The existing FastAPI endpoints and Pydantic models were kept, while the storage layer now reads and writes project data from the PostgreSQL container.

The API automatically creates the required database table when the application starts.