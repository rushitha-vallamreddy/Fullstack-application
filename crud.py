import json
from sqlalchemy.orm import Session
from sqlalchemy import desc
import models, schemas


# ---------- Collections ----------
def list_collections(db: Session):
    return db.query(models.Collection).order_by(models.Collection.created_at).all()


def create_collection(db: Session, data: schemas.CollectionCreate):
    c = models.Collection(name=data.name)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def rename_collection(db: Session, cid: int, name: str):
    c = db.query(models.Collection).get(cid)
    if not c:
        return None
    c.name = name
    db.commit()
    db.refresh(c)
    return c


def delete_collection(db: Session, cid: int):
    c = db.query(models.Collection).get(cid)
    if not c:
        return False
    db.delete(c)
    db.commit()
    return True


# ---------- Requests ----------
def create_request(db: Session, data: schemas.RequestCreate):
    r = models.Request(**data.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def update_request(db: Session, rid: int, data: schemas.RequestCreate):
    r = db.query(models.Request).get(rid)
    if not r:
        return None
    for k, v in data.model_dump().items():
        setattr(r, k, v)
    db.commit()
    db.refresh(r)
    return r


def delete_request(db: Session, rid: int):
    r = db.query(models.Request).get(rid)
    if not r:
        return False
    db.delete(r)
    db.commit()
    return True


# ---------- Environments ----------
def list_environments(db: Session):
    return db.query(models.Environment).order_by(models.Environment.created_at).all()


def create_environment(db: Session, data: schemas.EnvironmentCreate):
    env = models.Environment(name=data.name)
    for v in data.variables:
        env.variables.append(models.EnvVariable(**v.model_dump()))
    db.add(env)
    db.commit()
    db.refresh(env)
    return env


def update_environment(db: Session, eid: int, data: schemas.EnvironmentUpdate):
    env = db.query(models.Environment).get(eid)
    if not env:
        return None
    if data.name is not None:
        env.name = data.name
    if data.is_active is not None:
        if data.is_active:
            # only one active
            for other in db.query(models.Environment).all():
                other.is_active = False
        env.is_active = data.is_active
    if data.variables is not None:
        # replace vars
        env.variables.clear()
        db.flush()
        for v in data.variables:
            env.variables.append(models.EnvVariable(**v.model_dump()))
    db.commit()
    db.refresh(env)
    return env


def delete_environment(db: Session, eid: int):
    env = db.query(models.Environment).get(eid)
    if not env:
        return False
    db.delete(env)
    db.commit()
    return True


# ---------- History ----------
def add_history(db: Session, method, url, status_code, time_ms, size_bytes, snapshot):
    h = models.History(
        method=method,
        url=url,
        status_code=status_code,
        time_ms=time_ms,
        size_bytes=size_bytes,
        request_snapshot=json.dumps(snapshot or {}),
    )
    db.add(h)
    db.commit()
    db.refresh(h)
    return h


def list_history(db: Session, limit: int = 200):
    return (
        db.query(models.History)
        .order_by(desc(models.History.created_at))
        .limit(limit)
        .all()
    )


def clear_history(db: Session):
    db.query(models.History).delete()
    db.commit()
