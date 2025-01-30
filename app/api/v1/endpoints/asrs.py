from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
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
    try:
        storeResult = asrs_service.store(session, item)
        if storeResult:
            response.status_code = status.HTTP_200_OK
            return {"detail": f"{item.itemName} stored successfully"}
        return {"detail": f"{item.itemName} storage failure"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": f"Error: {str(e)}"}


@router.get("/view/{trayId}")
async def view_item(
    trayId: str,
    response: Response,
    session: Session = Depends(get_db),
):
    try:
        viewResult = asrs_service.retrieve_photo(session, trayId)
        print("Viewresult: ", viewResult)
        if viewResult:
            response.status_code = status.HTTP_200_OK
            return {"data": viewResult}
        return {"detail": f"Retrieval failure"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": f"Error: {str(e)}"}
