"""Seed sample collections, environments, history."""
import json
from database import SessionLocal, engine, Base
import models


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(models.Collection).count() > 0:
            return

        # Collections + requests
        jp = models.Collection(name="JSONPlaceholder")
        jp.requests = [
            models.Request(
                name="List Posts",
                method="GET",
                url="https://jsonplaceholder.typicode.com/posts",
            ),
            models.Request(
                name="Get Post #1",
                method="GET",
                url="https://jsonplaceholder.typicode.com/posts/1",
            ),
            models.Request(
                name="Create Post",
                method="POST",
                url="https://jsonplaceholder.typicode.com/posts",
                body_mode="raw",
                raw_type="json",
                body=json.dumps(
                    {"title": "hello", "body": "world", "userId": 1}, indent=2
                ),
                headers=json.dumps(
                    [{"key": "Content-Type", "value": "application/json", "enabled": True}]
                ),
            ),
        ]

        hb = models.Collection(name="HTTPBin")
        hb.requests = [
            models.Request(name="GET", method="GET", url="https://httpbin.org/get"),
            models.Request(
                name="POST echo",
                method="POST",
                url="https://httpbin.org/post",
                body_mode="raw",
                raw_type="json",
                body='{"hello":"world"}',
            ),
            models.Request(
                name="Bearer Auth",
                method="GET",
                url="https://httpbin.org/bearer",
                auth_type="bearer",
                auth_data=json.dumps({"token": "{{token}}"}),
            ),
        ]

        # Environments
        dev = models.Environment(name="Development", is_active=True)
        dev.variables = [
            models.EnvVariable(key="base_url", value="https://jsonplaceholder.typicode.com"),
            models.EnvVariable(key="token", value="dev-secret-token"),
        ]
        prod = models.Environment(name="Production")
        prod.variables = [
            models.EnvVariable(key="base_url", value="https://api.example.com"),
            models.EnvVariable(key="token", value="prod-token"),
        ]

        db.add_all([jp, hb, dev, prod])
        db.commit()
        print("Seeded sample data.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
