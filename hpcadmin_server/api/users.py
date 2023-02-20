from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas
from ..database import crud
from ..database.db import get_db


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.User])
async def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db=db)
    return users


@router.post("/", response_model=schemas.User)
async def post_user(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user_create.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db=db, user=user_create)


@router.get("/{id}", response_model=schemas.User)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, id=id)
    return user


@router.get("/{username}", response_model=schemas.User)
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=username)
    return user
