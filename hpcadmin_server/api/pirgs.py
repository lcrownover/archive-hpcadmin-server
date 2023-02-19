from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from . import schemas
from ..database import crud
from ..database.db import get_db


router = APIRouter(
    prefix="/pirgs",
    tags=["pirgs"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Pirg])
async def get_pirgs(db: Session = Depends(get_db)):
    pirgs = crud.get_pirgs(db)
    return pirgs


@router.post("/", response_model=schemas.Pirg)
async def post_pirg(pirg_create: schemas.PirgCreate, db: Session = Depends(get_db)):
    db_pirg = crud.get_pirg_by_name(db=db, name=pirg_create.name)
    if db_pirg:
        raise HTTPException(status_code=400, detail="Pirg already exists")
    if not crud.get_user(db=db, user_id=pirg_create.owner_id):
        raise HTTPException(status_code=404, detail="Owner does not exist")
    return crud.create_pirg(db=db, pirg=pirg_create)


@router.post("/{pirg_name}/users", response_model=schemas.Pirg)
async def post_pirg_users(
    pirg_name: str, user: schemas.PirgAddUser, db: Session = Depends(get_db)
):
    db_pirg = crud.get_pirg_by_name(db=db, name=pirg_name)
    if not db_pirg:
        raise HTTPException(status_code=404, detail="Pirg not found")
    db_user = crud.get_user(db=db, user_id=user.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.add_user_to_pirg(db=db, pirg=db_pirg, user=db_user)
