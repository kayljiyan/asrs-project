from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.sqlite import TEXT, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ItemArchive(Base):
    __tablename__ = "item_archives"

    archiveId: Mapped[str] = mapped_column(
        TEXT(50), primary_key=True, default=str(uuid4)
    )
    photoPath: Mapped[str] = mapped_column(TEXT(200), nullable=True, unique=True)
    createdAt: Mapped[DateTime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.now()
    )
    trayId: Mapped[str] = mapped_column(
        TEXT(50), ForeignKey("items.trayId"), nullable=False
    )
