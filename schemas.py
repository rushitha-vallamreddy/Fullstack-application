from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime


# ---------- Requests ----------
class RequestBase(BaseModel):
    name: str = "Untitled Request"
    method: str = "GET"
    url: str = ""
    params: str = "[]"
    headers: str = "[]"
    body_mode: str = "none"
    body: str = ""
    raw_type: str = "json"
    auth_type: str = "none"
    auth_data: str = "{}"
    collection_id: Optional[int] = None


class RequestCreate(RequestBase):
    pass


class RequestOut(RequestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------- Collections ----------
class CollectionBase(BaseModel):
    name: str


class CollectionCreate(CollectionBase):
    pass


class CollectionOut(CollectionBase):
    id: int
    created_at: datetime
    requests: List[RequestOut] = []

    class Config:
        from_attributes = True


# ---------- Environments ----------
class EnvVariableIn(BaseModel):
    key: str
    value: str = ""
    enabled: bool = True


class EnvVariableOut(EnvVariableIn):
    id: int

    class Config:
        from_attributes = True


class EnvironmentBase(BaseModel):
    name: str


class EnvironmentCreate(EnvironmentBase):
    variables: List[EnvVariableIn] = []


class EnvironmentUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    variables: Optional[List[EnvVariableIn]] = None


class EnvironmentOut(EnvironmentBase):
    id: int
    is_active: bool
    variables: List[EnvVariableOut] = []

    class Config:
        from_attributes = True


# ---------- Send / History ----------
class SendPayload(BaseModel):
    method: str
    url: str
    headers: Dict[str, str] = {}
    params: Dict[str, str] = {}
    body_mode: str = "none"  # none | raw | form-data | x-www-form-urlencoded
    body: Any = None
    raw_type: str = "json"
    timeout_ms: int = 30000
    request_snapshot: Optional[Dict[str, Any]] = None


class SendResponse(BaseModel):
    status_code: int
    status_text: str
    time_ms: float
    size_bytes: int
    headers: Dict[str, str]
    body: str
    content_type: str


class HistoryOut(BaseModel):
    id: int
    method: str
    url: str
    status_code: Optional[int]
    time_ms: float
    size_bytes: int
    request_snapshot: str
    created_at: datetime

    class Config:
        from_attributes = True
