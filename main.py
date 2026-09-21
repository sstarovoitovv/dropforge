from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime, timedelta, timezone

from database import get_connection


# Описываем JSON, который клиент присылает для создания drop
class DropCreate(BaseModel):
    content: str
    ttl_seconds: int | None = None
    max_views: int | None = None


# Храним drop с ID, текстом и возможным временем истечения
class Drop(BaseModel):
    id: str
    content: str
    expires_at: datetime | None = None
    views_remaining: int | None = None


app = FastAPI()
drops: dict[str, Drop] = {}

# Проверяем, что API запущен и отвечает на GET-запросы
@app.get("/")
def read_root():
    return {"message": "DropForge is running"}

# Возвращаем один сохранённый drop по его ID из URL
@app.get("/drops/{drop_id}")
def get_drop(drop_id: str):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, content, expires_at, views_remaining
                FROM drops
                WHERE id = %s
                FOR UPDATE
                """,
                (drop_id,),
            )
            row = cursor.fetchone()
            
            if row is None:
                raise HTTPException(404, detail="Drop not found")

            drop = Drop(
                id=str(row[0]),
                content=row[1],
                expires_at=row[2],
                views_remaining=row[3],
            )

            if drop.expires_at is not None and drop.expires_at <= datetime.now(timezone.utc):
                raise HTTPException(status_code=410, detail="drop lifetime expired")

            if drop.views_remaining is not None and drop.views_remaining <= 0:
                raise HTTPException(status_code=410, detail="View limit reached")
            
            if drop.views_remaining is not None:
                cursor.execute(
                    """
                    UPDATE drops
                    SET views_remaining = views_remaining - 1
                    WHERE id = %s
                    RETURNING views_remaining
                    """,
                    (drop_id,),
                )
                drop.views_remaining = cursor.fetchone()[0]
                
            return drop

# Создаём drop из JSON, присланного клиентом, и сохраняем его в PostgreSQL
@app.post("/drops", status_code=201)
def create_drop(payload: DropCreate):
    if payload.ttl_seconds is not None and payload.ttl_seconds <= 0:
        raise HTTPException(status_code=400, detail="ttl must be positive")

    if payload.max_views is not None and payload.max_views <= 0:
        raise HTTPException(status_code=400, detail="max_views must be positive")

    expires_at = None
    if payload.ttl_seconds is not None:
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=payload.ttl_seconds)

    drop_id = str(uuid4())
    
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO drops (
                    id, 
                    content, 
                    expires_at, 
                    views_remaining
                    )
                VALUES (
                    %s, 
                    %s, 
                    %s,
                    %s
                )
                RETURNING id, content, expires_at, views_remaining
                """,
                (drop_id, 
                 payload.content,
                 expires_at,
                 payload.max_views,
                 )
            )

            row = cursor.fetchone()
    
    created_drop = Drop(
        id=str(row[0]), 
        content=row[1],
        expires_at=row[2],
        views_remaining=row[3])
    
    return created_drop

# Удаляем сохранённый drop по ID; успешное удаление возвращает 204 без тела
@app.delete("/drops/{drop_id}", status_code=204)
def delete_drop(drop_id: str):
    
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                 DELETE FROM drops
                WHERE id = %s
                RETURNING id
                """, 
                (drop_id,)
                
            )
            row = cursor.fetchone()

    if row is None:
        raise HTTPException(404, detail="Drop not found")

    return None
