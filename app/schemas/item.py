from datetime import datetime

from pydantic import UUID4, BaseModel


class Item(BaseModel):
    trayId: UUID4
    itemName: str
    cameraIPs: list[str]
    latestPhotoPath: str
    updatedAt: datetime
