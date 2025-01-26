from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.sqlite import TEXT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Item(Base):
    __tablename__ = "items"

    trayId: Mapped[str] = mapped_column(TEXT(50), primary_key=True, default=str(uuid4))
    itemName: Mapped[str] = mapped_column(TEXT(200), nullable=False)
    cameraIPs: Mapped[str] = mapped_column(TEXT(200), nullable=False)
    latestPhotoPath: Mapped[str] = mapped_column(TEXT(200), nullable=True, unique=True)
    updatedAt: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.now()
    )
