from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StoreItem(BaseModel):
    trayId: int
    itemName: Optional[str]


class Item(StoreItem):
    latestPhotoPath: str
    updatedAt: datetime
