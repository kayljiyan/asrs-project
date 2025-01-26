from sqlalchemy.orm import Session

from app import models


def store(session: Session, trayId: str):
	ip = retrieve_ips(session, trayId)
	photo1path = take_photo(ip[0])
	photo2path = take_photo(ip[1])
	return stitch_photo(photo1path, photo2path, trayId)

def retrieve_ips(session: Session, trayId: str):
    ips = session.query(models.Item.cameraIPs).filter(models.Item.trayId == trayId).first()
    return ips

def take_photo(ip: str):
	# take photo via ip
	# return photo taken path || error
    pass

def stitch_photo(photo1path: str, photo2path: str, trayId: str):
	# stitch photos
	# return store_photo(trayId, photoPath) || error
    pass

def archive_photo(session: Session, trayId: str, photoPath: str):
    db_photo = models.ItemArchive(
        photoPath=photoPath,
        trayId=trayId
    )
    session.add(db_photo)
    session.commit()
    return True

def retrieve_photo(session: Session, trayId: str):
    latestPhotoPath = session.query(models.Item.latestPhotoPath).filter(models.Item.trayId == trayId).first()
    return latestPhotoPath

def store_photo(session: Session, trayId: str, photoPath: str, itemName: str || None = None, cameraIPs: str || None = None):
	latestPhotoPath = retrieve_photo(session, trayId)
    if latestPhotoPath:
	    archive_photo(session, trayId, latestPhotoPath)
        db_photo = session.query(models.Item).filter(models.Item.trayId == trayId)
        if db_photo.first():
            db_photo.update({"latestPhotoPath": photoPath})
            return True
    else:
        db_photo = models.Item(
            itemName=itemName,
            cameraIPs=cameraIPs,
            latestPhotoPath=photoPath,
        )
        session.add(db_photo)
        session.commit()
        return True
        
