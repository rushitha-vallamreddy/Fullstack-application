from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base


class Collection(Base):
    __tablename__ = "collections"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    requests = relationship(
        "Request", back_populates="collection", cascade="all, delete-orphan"
    )


class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(
        Integer, ForeignKey("collections.id", ondelete="CASCADE"), nullable=True
    )
    name = Column(String, nullable=False, default="Untitled Request")
    method = Column(String, nullable=False, default="GET")
    url = Column(Text, nullable=False, default="")
    # JSON-encoded strings
    params = Column(Text, default="[]")   # [{key,value,enabled}]
    headers = Column(Text, default="[]")  # [{key,value,enabled}]
    body_mode = Column(String, default="none")  # none | raw | form-data | x-www-form-urlencoded
    body = Column(Text, default="")
    raw_type = Column(String, default="json")   # json | text
    auth_type = Column(String, default="none")  # none | bearer | basic
    auth_data = Column(Text, default="{}")      # {token} or {username,password}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    collection = relationship("Collection", back_populates="requests")


class Environment(Base):
    __tablename__ = "environments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    variables = relationship(
        "EnvVariable", back_populates="environment", cascade="all, delete-orphan"
    )


class EnvVariable(Base):
    __tablename__ = "env_variables"
    id = Column(Integer, primary_key=True, index=True)
    environment_id = Column(
        Integer, ForeignKey("environments.id", ondelete="CASCADE"), nullable=False
    )
    key = Column(String, nullable=False)
    value = Column(Text, default="")
    enabled = Column(Boolean, default=True)

    environment = relationship("Environment", back_populates="variables")


class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    method = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    status_code = Column(Integer, nullable=True)
    time_ms = Column(Float, default=0)
    size_bytes = Column(Integer, default=0)
    request_snapshot = Column(Text, default="{}")  # full request as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
