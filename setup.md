# Setup – Project 08

## 1. Start from the project folder

```bash
cd ~/devops-roadmap-portfolio/project-08-docker-compose-fastapi-postgres
```

## 2. Create the local environment file

```bash
cp .env.example .env
```

Edit the values if needed:

```bash
nano .env
```

For Docker Compose, the API container must use the database service name:

```
DATABASE_HOST=db
DATABASE_PORT=5432
```

## 3. Validate Docker Compose configuration

```bash
docker compose config
```

## 4. Build and start all services

```bash
docker compose up --build
```

Detached mode:

```bash
docker compose up --build -d
```

## 5. Check running services

```bash
docker compose ps
```

Expected services:

- `api`
- `db`

The database service should become healthy.

## 6. View logs

All services:

```bash
docker compose logs -f
```

API only:

```bash
docker compose logs -f api
```

Database only:

```bash
docker compose logs -f db
```

## 7. Test the API

Health check:

```bash
curl http://localhost:8000/health
```

Create a project:

```bash
curl -X POST http://localhost:8000/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"Project 08","description":"Docker Compose FastAPI app with PostgreSQL persistence.","status":"in-progress"}'
```

List projects:

```bash
curl http://localhost:8000/projects
```

Swagger UI:

```
http://localhost:8000/docs
```

## 8. Access PostgreSQL

```bash
docker compose exec db psql -U appuser -d appdb
```

Useful PostgreSQL commands:

```sql
\dt
SELECT * FROM projects;
\q
```

## 9. Run tests locally

The database container must be running first:

```bash
docker compose up -d db
```

Run tests:

```bash
docker compose exec api python -m pytest -v
```

## 10. Run pre-commit checks

```bash
pre-commit run --all-files
```

If pytest is enabled in pre-commit, make sure the database container is running before executing the hook.

## 11. Validate persistence

Create data through the API, then restart the containers without deleting volumes:

```bash
docker compose down
docker compose up -d
```

Check the data again:

```bash
curl http://localhost:8000/projects
```

If the data is still available, the PostgreSQL Docker volume is working.

## 12. Stop services

```bash
docker compose down
```

## 13. Stop services and remove database data

```bash
docker compose down -v
```

Use this only when you want to delete the PostgreSQL volume and reset the database.

## 14. Useful Docker inspection commands

List volumes:

```bash
docker volume ls
```

Inspect the project network:

```bash
docker network ls
```

Inspect containers:

```bash
docker compose ps
```

## 15. Common issues

### API cannot connect to database

Inside Docker Compose, the API must use:

```
DATABASE_HOST=db
DATABASE_PORT=5432
```

For local pytest from the host machine, use the host-exposed database port configured in your environment.

### PostgreSQL password authentication failed

If the database password was changed after the PostgreSQL volume was created, reset the volume:

```bash
docker compose down -v
```

This removes the persistent volume and allows PostgreSQL to reinitialize with the new credentials from `.env`.

### Test collection errors

If pytest fails to collect tests due to database connection errors, ensure:

1. Docker Compose services are running: `docker compose up -d`
2. Tests are mounted in the container (check `docker-compose.yml` volumes)
3. Dependencies are installed: `docker compose exec api pip install -q pytest httpx`

### Container exits unexpectedly

Check logs:

```bash
docker compose logs db
docker compose logs api
```

Common causes:

- Database port 5432 already in use
- Environment variables not loaded correctly
- Dockerfile syntax errors

---

## Project 08 Workflow Summary

1. **Development:** Edit code locally, containers auto-reload with volume mounts
2. **Testing:** Run `docker compose exec api python -m pytest -v`
3. **Manual Testing:** Use Swagger UI at `http://localhost:8000/docs`
4. **Database Inspection:** Access PostgreSQL with `docker compose exec db psql`
5. **Data Persistence:** Volumes survive `docker compose down` (use `-v` to delete)
6. **Cleanup:** `docker compose down -v` removes everything (containers, volumes, networks)

---

## Next: DEVOPS-36

The next phase will add SQLAlchemy models and database schema initialization to replace in-memory storage with persistent PostgreSQL data.
