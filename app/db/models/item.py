from datetime import datetime

from sqlalchemy.dialects.sqlite import TEXT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Item(Base):
    __tablename__ = "items"

    trayId: Mapped[str] = mapped_column(TEXT(50), primary_key=True)
    itemName: Mapped[str] = mapped_column(TEXT(200), nullable=True)
    latestPhotoPath: Mapped[str] = mapped_column(TEXT(200), nullable=True)
    updatedAt: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.now()
    )
