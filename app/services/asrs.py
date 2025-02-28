import asyncio
import os
from datetime import datetime
from time import sleep

import cv2
from PIL import Image
from sqlalchemy.orm import Session

from app.db import models
from app.schemas import item_schema


async def store(session: Session, item: item_schema.StoreItem):
    # ips = retrieve_ips(session, item.trayId)
    # ips = "rtsp://192.168.0.104:554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp?real_stream"
    task1 = asyncio.create_task(take_photo(2, 1))
    task2 = asyncio.create_task(take_photo(4, 2))
    results = await asyncio.gather(task1, task2)
    # photo1path = take_photo(ips[0], 1)
    # photo2path = take_photo(ips[1], 2)
    return stitch_photo(session, results[0], results[1], item.trayId, item.itemName)


def retrieve_ips(session: Session, trayId: str):
    ips = (
        session.query(models.Item.cameraIPs)
        .filter(models.Item.trayId == trayId)
        .first()
    )
    print("IPS: ", ips)
    ips = ips[0].split(",")
    return ips


async def take_photo(ip: int, num: int):
    ip_camera_url = "rtsp://192.168.0.104:554/user=admin_password=tlJwpbo6_channel=0_stream=0&onvif=0.sdp?real_stream"

    filename = f"photo{num}.jpg"
    cap = cv2.VideoCapture(ip)

    if not cap.isOpened():
        print("Error: Unable to connect to the IP camera.")
    else:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_LINEAR)
        if ret:
            cv2.imwrite(filename, frame)
        else:
            print("Error: Unable to capture a frame.")

    cap.release()
    return filename


def stitch_photo(
    session: Session, photo1path: str, photo2path: str, trayId: str, itemName: str = ""
):
    save_folder = "images"
    os.makedirs(save_folder, exist_ok=True)
    filename = f"{trayId}-{datetime.now()}.jpg"

    image1 = Image.open(photo1path)
    image2 = Image.open(photo2path)

    height1 = image1.height
    height2 = image2.height
    max_height = max(height1, height2)

    image1 = image1.resize((image1.width, max_height))
    image2 = image2.resize((image2.width, max_height))

    stitched_image = Image.new("RGB", (image1.width + image2.width, max_height))

    stitched_image.paste(image1, (0, 0))
    stitched_image.paste(image2, (image1.width, 0))

    filename = os.path.join(save_folder, filename)
    stitched_image.save(filename)
    os.remove(photo1path)
    os.remove(photo2path)
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
    return latestPhotoPath[0]


def store_photo(
    session: Session,
    trayId: str,
    photoPath: str,
    itemName: str = "",
):
    latestPhotoPath = retrieve_photo(session, trayId)
    if latestPhotoPath:
        archive_photo(session, trayId, latestPhotoPath)
    db_photo = session.query(models.Item).filter(models.Item.trayId == trayId).first()
    if db_photo:
        db_photo.latestPhotoPath = photoPath
        db_photo.itemName = itemName
        session.commit()
        session.refresh(db_photo)
        return True
    return False
