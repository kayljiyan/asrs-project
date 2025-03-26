import asyncio
import os
import threading
from datetime import date, datetime
from pathlib import Path
from time import sleep, time

import cv2
import numpy as np
from PIL import Image
from sqlalchemy.orm import Session

from app.db import models
from app.schemas import item_schema


async def store(session: Session, item: item_schema.StoreItem):
    task1 = asyncio.create_task(take_photo(0, 1))
    task2 = asyncio.create_task(take_photo(1, 2))
    results = await asyncio.gather(task1, task2)
    save_folder = "images"
    os.makedirs(save_folder, exist_ok=True)
    filename = f"{item.trayId}-{date.today()}-{int(time())}.jpg"
    filename: str = str(filename).replace(" ", "-")
    filename = os.path.normpath(os.path.join(save_folder, filename))
    filename = str(filename).strip().encode("utf-8").decode("utf-8")
    filename = Path(filename)
    return stitch_photo(
        session, results[0], results[1], item.trayId, str(filename), item.itemName
    )


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
    filename = f"photo{num}.jpg"
    cap = cv2.VideoCapture(ip)

    if not cap.isOpened():
        print("Error: Unable to connect to the IP camera.")
    else:
        ret, frame = cap.read()
        #frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_LINEAR)
        if ret:
            cv2.imwrite(filename, frame)
        else:
            print("Error: Unable to capture a frame.")

    cap.release()
    return filename


def stitch_photo(
    session: Session,
    photo1path: str,
    photo2path: str,
    trayId: str,
    filename: str,
    itemName: str = "",
):
    image1 = Image.open(photo1path)
    image2 = Image.open(photo2path)

    height1 = image1.height
    height2 = image2.height
    max_height = max(height1, height2)
    crop_size = min(image1.width, image2.width) // 4

    image1 = image1.resize((image1.width, max_height))
    image2 = image2.resize((image2.width, max_height))

    #img1_cropped = image1.crop((0, 0, image1.width-crop_size, height1))
    #img2_cropped = image2.crop((crop_size, 0, image2.width, height2))

    stitched_image = Image.new("RGB", (image1.width + image2.width, max_height))

    stitched_image.paste(image1, (0, 0))
    stitched_image.paste(image2, (image1.width, 0))
    stitched_image = stitched_image.rotate(180)
    stitched_image.save(fp=filename)
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
        return photoPath, trayId
    return False

async def close_specific_window(window_name, delay):
    await asyncio.sleep(delay)
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) >= 1:
        cv2.destroyWindow(window_name)


def show_image(filename: str, trayId: str):
    image = Image.open(filename)
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    cv2.namedWindow(trayId, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(trayId, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(trayId, img_cv)
    cv2.waitKey(100)
    return True
