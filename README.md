# DropForge

A small API for sharing text that should not live forever.

DropForge creates a text drop and gives it a unique ID. A drop may expire after a set number of seconds or become unavailable after a set number of views.

The current version supports creating, reading and deleting drops. Drops are stored in PostgreSQL, so they survive server restarts.

## Run locally

The project uses Python 3.14 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive documentation is at `http://127.0.0.1:8000/docs`.

## Database

DropForge uses PostgreSQL. Configure `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` and `PGPASSWORD` in your environment, then create the schema:

```bash
uv run alembic upgrade head
```

The local `.env` file is ignored by Git and must never be committed.

## Create a drop

```bash
curl -X POST http://127.0.0.1:8000/drops \
  -H "Content-Type: application/json" \
  -d '{"content":"hello","ttl_seconds":60,"max_views":2}'
```
