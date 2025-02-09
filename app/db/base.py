from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import Session

Base: DeclarativeMeta = declarative_base()

from .models import item, itemarchive


def init_trays(db: Session):
    db_tray = item.Item(
        trayId=f"TRAY01",
        cameraIPs=f"rtsp://192.168.0.104:554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp?real_stream,rtsp://192.168.0.104:554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp?real_stream",
    )
    db.add(db_tray)
    db.commit()
