# Setup – Project 06 FastAPI CRUD API

## 1. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Install dependencies

```bash
pip install -r requirements-dev.txt
```

## 3. Run the API locally

```bash
uvicorn app.main:app --reload
```

API health check:

```bash
curl http://127.0.0.1:8000/health
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

OpenAPI schema:

```text
http://127.0.0.1:8000/openapi.json
```

## 4. Run tests

```bash
pytest -v
```

## 5. Run pre-commit checks

```bash
pre-commit install
pre-commit run --all-files
```

## 6. Build Docker image

```bash
docker build -t project-06-fastapi-crud-api .
```

## 7. Run Docker container

```bash
docker run --rm -p 8000:8000 project-06-fastapi-crud-api
```

Test container:

```bash
curl http://127.0.0.1:8000/health
```

## 8. Test optional Lambda wrapper import

```bash
python -c "from aws.lambda_wrapper.handler import handler; print(handler)"
```

## Notes

The main application runs locally and in Docker using Uvicorn.

The AWS Lambda wrapper is optional and only prepares the project for a future serverless deployment. No AWS deployment is required in this project.
