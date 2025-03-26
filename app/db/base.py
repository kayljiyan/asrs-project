from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Session

Base: DeclarativeMeta = declarative_base()

from .models import item, itemarchive


def init_trays(db: Session):
    for i in range(1,32):
        db_tray = item.Item(
            trayId=i,
            latestPhotoPath="placeholder.jpg",
        )
        db.add(db_tray)
        db.commit()
