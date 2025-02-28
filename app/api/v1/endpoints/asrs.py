import os
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.schemas import item_archive_schema, item_schema
from app.services import asrs_service

from . import get_db

router = APIRouter()


@router.post("/store")
async def store_item(
    item: item_schema.StoreItem,
    response: Response,
    session: Session = Depends(get_db),
):
    #try:
    storeResult = await asrs_service.store(session, item)
    if storeResult:
        response.status_code = status.HTTP_200_OK
        return {"detail": f"{item.itemName} stored successfully"}
    return {"detail": f"{item.itemName} storage failure"}
    #except Exception as e:
    #    response.status_code = status.HTTP_400_BAD_REQUEST
    #    return {"detail": f"Error: {str(e)}"}


@router.get("/view/{trayId}")
async def view_item(
    trayId: str,
    response: Response,
    session: Session = Depends(get_db),
):
    try:
        viewResult = asrs_service.retrieve_photo(session, trayId)
        print("Viewresult: ", viewResult)
        if not viewResult:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"detail": "image not found"}
        if not os.path.exists(viewResult):
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"detail": "image not found"}
        return FileResponse(viewResult, media_type="image/jpeg")
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": f"Error: {str(e)}"}
