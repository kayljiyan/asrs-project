from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Session

Base: DeclarativeMeta = declarative_base()

from .models import item, itemarchive


def init_trays(db: Session):
    for i in range(1, 8, 2):
        db_tray = item.Item(
            trayId=f"TRAY0{i}", cameraIPs=f"192.168.0.{i+1},192.168.0.{(i+1)*2}"
        )
        db.add(db_tray)
    db.commit()
