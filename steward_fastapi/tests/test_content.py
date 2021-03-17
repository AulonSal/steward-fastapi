import asyncio
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from steward_fastapi.core.models.database import ContentType
from steward_fastapi.main import app


@pytest.fixture(scope="module")
def client() -> Generator:
    initializer(["steward_fastapi.core.models.database"])
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


def test_create_type(client: TestClient, event_loop: asyncio.AbstractEventLoop):  # nosec
    response = client.post("/types", json={"name": "tech"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "tech"
    assert "id" in data
    type_id = data["id"]

    async def get_type_by_db():
        type_ = await ContentType.get(id=type_id)
        return type_

    type_obj = event_loop.run_until_complete(get_type_by_db())
    assert type_obj.id == type_id

