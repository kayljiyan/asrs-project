from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Session

Base: DeclarativeMeta = declarative_base()

from .models import item, itemarchive


def init_trays(db: Session):
    db_tray = item.Item(
        trayId=f"TRAY01",
    )
    db.add(db_tray)
    db.commit()
