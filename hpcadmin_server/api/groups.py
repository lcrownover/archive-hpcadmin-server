from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import schemas
from ..database import crud
from ..database.db import get_db


router = APIRouter(
    prefix="/groups",
    tags=["groups"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Group])
async def get_groups(db: Session = Depends(get_db)):
    groups = crud.get_pirg_groups(db)
    return groups
