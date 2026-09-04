from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import current_active_user
from app.core.database import get_async_session
from app.models.ops_log import OpsLog
from app.models.user import User
from app.schemas.ops_log import OpsLogList, OpsLogRead

router = APIRouter(prefix="/api/ops-logs", tags=["ops-logs"])


@router.get("", response_model=OpsLogList)
async def list_ops_logs(
    _: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
    limit: int = Query(default=5, ge=1, le=20),
):
    result = await session.execute(
        select(OpsLog).order_by(OpsLog.created_at.desc()).limit(limit)
    )
    logs = list(result.scalars().all())
    items = [OpsLogRead.model_validate(log) for log in logs]
    return OpsLogList(items=items, has_failure=any(not item.success for item in items))
