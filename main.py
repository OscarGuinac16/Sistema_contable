from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from database import close_pool, get_connection


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    close_pool()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/db/ping")
def ping_oracle():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM dual")
                row = cursor.fetchone()
        return {"ok": True, "result": row[0] if row else None}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"No se pudo conectar a Oracle: {exc}") from exc
