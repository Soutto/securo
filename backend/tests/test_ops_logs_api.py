import uuid
from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ops_log import OpsLog


@pytest.mark.asyncio
async def test_ops_logs_unauthenticated(client: AsyncClient):
    response = await client.get("/api/ops-logs")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_ops_logs_empty(client: AsyncClient, auth_headers):
    response = await client.get("/api/ops-logs", headers=auth_headers)
    assert response.status_code == 200
    payload = response.json()
    assert payload["items"] == []
    assert payload["has_failure"] is False


@pytest.mark.asyncio
async def test_ops_logs_returns_latest_five_and_failure_flag(
    client: AsyncClient, auth_headers, session: AsyncSession
):
    now = datetime.now(timezone.utc)
    for index in range(6):
        session.add(
            OpsLog(
                id=uuid.uuid4(),
                kind="backup" if index % 2 == 0 else "update",
                success=index != 5,
                message=f"run-{index}",
                created_at=now + timedelta(seconds=index),
            )
        )
    await session.commit()

    response = await client.get("/api/ops-logs", headers=auth_headers)
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["items"]) == 5
    assert payload["items"][0]["message"] == "run-5"
    assert payload["has_failure"] is True
    kinds = {item["kind"] for item in payload["items"]}
    assert kinds <= {"backup", "update"}
