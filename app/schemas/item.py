from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel


class StoreItem(BaseModel):
    trayId: UUID4
    itemName: Optional[str]


class Item(StoreItem):
    cameraIPs: str
    latestPhotoPath: str
    updatedAt: datetime
