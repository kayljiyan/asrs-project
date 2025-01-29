from datetime import datetime

import cv2
from sqlalchemy.orm import Session

from app.db import models
from app.schemas import item_schema


def store(session: Session, item: item_schema.StoreItem):
    ips = retrieve_ips(session, item.trayId)
    photo1path = take_photo(ips[0], 1)
    photo2path = take_photo(ips[1], 2)
    return stitch_photo(session, photo1path, photo2path, item.trayId, item.itemName)


def retrieve_ips(session: Session, trayId: str):
    ips = (
        session.query(models.Item.cameraIPs)
        .filter(models.Item.trayId == trayId)
        .first()
    )
    ips = ips.split(",")
    return ips


def take_photo(ip: str, num: int):
    ip_camera_url = f"http://{ip}:<PORT>/video"

    filename = f"photo{num}.jpg"
    cap = cv2.VideoCapture(ip_camera_url)

    if not cap.isOpened():
        print("Error: Unable to connect to the IP camera.")
    else:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(filename, frame)
        else:
            print("Error: Unable to capture a frame.")

    cap.release()
    return filename


def stitch_photo(
    session: Session, photo1path: str, photo2path: str, trayId: str, itemName: str = ""
):
    image1 = cv2.imread(photo1path)
    image2 = cv2.imread(photo2path)

    stitcher = cv2.Stitcher_create()
    status, stitched_image = stitcher.stitch([image1, image2])

    filename = f"{trayId}{datetime.now()}.jpg"

    if status == cv2.Stitcher_OK:
        cv2.imwrite(filename, stitched_image)
    else:
        print("Stitching failed. Error code:", status)

    return store_photo(session, trayId, filename, itemName)


def archive_photo(session: Session, trayId: str, photoPath: str):
    db_photo = models.ItemArchive(photoPath=photoPath, trayId=trayId)
    session.add(db_photo)
    session.commit()
    return True


def retrieve_photo(session: Session, trayId: str):
    latestPhotoPath = (
        session.query(models.Item.latestPhotoPath)
        .filter(models.Item.trayId == trayId)
        .first()
    )
    return latestPhotoPath


def store_photo(
    session: Session,
    trayId: str,
    photoPath: str,
    itemName: str = "",
):
    latestPhotoPath = retrieve_photo(session, trayId)
    if latestPhotoPath:
        archive_photo(session, trayId, latestPhotoPath)
    db_photo = session.query(models.Item).filter(models.Item.trayId == trayId)
    if db_photo.first():
        db_photo.update({"latestPhotoPath": photoPath})
        db_photo.update({"itemName": itemName})
        return True
    return False
