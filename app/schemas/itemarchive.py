from datetime import datetime

from pydantic import UUID4, BaseModel


class ItemArchive(BaseModel):
    archiveId: UUID4
    photoPath: str
    createdAt: datetime
    trayId: UUID4
