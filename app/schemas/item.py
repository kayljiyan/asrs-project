from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StoreItem(BaseModel):
    trayId: str
    itemName: Optional[str]


class Item(StoreItem):
    cameraIPs: str
    latestPhotoPath: str
    updatedAt: datetime
