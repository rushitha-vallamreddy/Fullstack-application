import json
import time
from typing import List
import httpx
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models, schemas, crud
from seed import seed

Base.metadata.create_all(bind=engine)
seed()

app = FastAPI(title="Postman Clone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Postman Clone API"}


# ---------------------------------------------------------------------------
# SEND (proxy runner)
# ---------------------------------------------------------------------------
@app.post("/send", response_model=schemas.SendResponse)
async def send_request(payload: schemas.SendPayload, db: Session = Depends(get_db)):
    method = payload.method.upper()

    # build body
    content = None
    data = None
    files = None
    json_body = None
    headers = {k: v for k, v in payload.headers.items() if k}

    if payload.body_mode == "raw" and payload.body is not None and payload.body != "":
        if payload.raw_type == "json":
            try:
                json_body = json.loads(payload.body) if isinstance(payload.body, str) else payload.body
                headers.setdefault("Content-Type", "application/json")
            except Exception:
                content = payload.body
                headers.setdefault("Content-Type", "application/json")
        else:
            content = payload.body if isinstance(payload.body, str) else str(payload.body)
            headers.setdefault("Content-Type", "text/plain")
    elif payload.body_mode == "x-www-form-urlencoded" and isinstance(payload.body, dict):
        data = payload.body
    elif payload.body_mode == "form-data" and isinstance(payload.body, dict):
        # send as multipart text fields
        files = [(k, (None, str(v))) for k, v in payload.body.items()]

    params = {k: v for k, v in payload.params.items() if k}

    start = time.perf_counter()
    try:
        async with httpx.AsyncClient(
            timeout=payload.timeout_ms / 1000.0, follow_redirects=True
        ) as client:
            resp = await client.request(
                method=method,
                url=payload.url,
                headers=headers,
                params=params,
                content=content,
                data=data,
                files=files,
                json=json_body,
            )
        elapsed = (time.perf_counter() - start) * 1000.0
        body_text = resp.text
        size_bytes = len(resp.content)
        out_headers = {k: v for k, v in resp.headers.items()}

        crud.add_history(
            db,
            method=method,
            url=str(resp.request.url),
            status_code=resp.status_code,
            time_ms=elapsed,
            size_bytes=size_bytes,
            snapshot=payload.request_snapshot or payload.model_dump(),
        )

        return schemas.SendResponse(
            status_code=resp.status_code,
            status_text=resp.reason_phrase or "",
            time_ms=elapsed,
            size_bytes=size_bytes,
            headers=out_headers,
            body=body_text,
            content_type=out_headers.get("content-type", ""),
        )
    except httpx.TimeoutException:
        elapsed = (time.perf_counter() - start) * 1000.0
        crud.add_history(db, method, payload.url, 0, elapsed, 0, payload.request_snapshot or payload.model_dump())
        raise HTTPException(status_code=408, detail="Request timed out")
    except httpx.RequestError as e:
        elapsed = (time.perf_counter() - start) * 1000.0
        crud.add_history(db, method, payload.url, 0, elapsed, 0, payload.request_snapshot or payload.model_dump())
        raise HTTPException(status_code=502, detail=f"Network error: {e}")


# ---------------------------------------------------------------------------
# COLLECTIONS
# ---------------------------------------------------------------------------
@app.get("/collections", response_model=List[schemas.CollectionOut])
def get_collections(db: Session = Depends(get_db)):
    return crud.list_collections(db)


@app.post("/collections", response_model=schemas.CollectionOut)
def post_collection(data: schemas.CollectionCreate, db: Session = Depends(get_db)):
    return crud.create_collection(db, data)


@app.patch("/collections/{cid}", response_model=schemas.CollectionOut)
def patch_collection(cid: int, data: schemas.CollectionCreate, db: Session = Depends(get_db)):
    c = crud.rename_collection(db, cid, data.name)
    if not c:
        raise HTTPException(404, "Not found")
    return c


@app.delete("/collections/{cid}")
def del_collection(cid: int, db: Session = Depends(get_db)):
    if not crud.delete_collection(db, cid):
        raise HTTPException(404, "Not found")
    return {"ok": True}


# ---------------------------------------------------------------------------
# REQUESTS
# ---------------------------------------------------------------------------
@app.post("/requests", response_model=schemas.RequestOut)
def post_request(data: schemas.RequestCreate, db: Session = Depends(get_db)):
    return crud.create_request(db, data)


@app.put("/requests/{rid}", response_model=schemas.RequestOut)
def put_request(rid: int, data: schemas.RequestCreate, db: Session = Depends(get_db)):
    r = crud.update_request(db, rid, data)
    if not r:
        raise HTTPException(404, "Not found")
    return r


@app.delete("/requests/{rid}")
def del_request(rid: int, db: Session = Depends(get_db)):
    if not crud.delete_request(db, rid):
        raise HTTPException(404, "Not found")
    return {"ok": True}


# ---------------------------------------------------------------------------
# ENVIRONMENTS
# ---------------------------------------------------------------------------
@app.get("/environments", response_model=List[schemas.EnvironmentOut])
def get_envs(db: Session = Depends(get_db)):
    return crud.list_environments(db)


@app.post("/environments", response_model=schemas.EnvironmentOut)
def post_env(data: schemas.EnvironmentCreate, db: Session = Depends(get_db)):
    return crud.create_environment(db, data)


@app.patch("/environments/{eid}", response_model=schemas.EnvironmentOut)
def patch_env(eid: int, data: schemas.EnvironmentUpdate, db: Session = Depends(get_db)):
    env = crud.update_environment(db, eid, data)
    if not env:
        raise HTTPException(404, "Not found")
    return env


@app.delete("/environments/{eid}")
def del_env(eid: int, db: Session = Depends(get_db)):
    if not crud.delete_environment(db, eid):
        raise HTTPException(404, "Not found")
    return {"ok": True}


# ---------------------------------------------------------------------------
# HISTORY
# ---------------------------------------------------------------------------
@app.get("/history", response_model=List[schemas.HistoryOut])
def get_history(db: Session = Depends(get_db)):
    return crud.list_history(db)


@app.delete("/history")
def del_history(db: Session = Depends(get_db)):
    crud.clear_history(db)
    return {"ok": True}
