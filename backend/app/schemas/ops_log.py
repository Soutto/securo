import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OpsLogRead(BaseModel):
    id: uuid.UUID
    kind: str
    success: bool
    message: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OpsLogList(BaseModel):
    items: list[OpsLogRead] = Field(default_factory=list)
    has_failure: bool = False
