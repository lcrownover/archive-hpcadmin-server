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
    if not crud.get_user(db=db, id=pirg_create.owner_id):
        raise HTTPException(
            status_code=404, detail=f"Owner id {pirg_create.owner_id} does not exist"
        )
    if pirg_create.user_ids:
        for user_id in pirg_create.user_ids:
            if not crud.get_user(db=db, id=user_id):
                raise HTTPException(
                    status_code=404, detail=f"User id {user_id} does not exist"
                )
    return crud.create_pirg(db=db, pirg=pirg_create)


####################
# Pirg Users
####################


@router.post("/{pirg_name}/users", response_model=schemas.Pirg)
async def post_pirg_users(
    pirg_name: str, user: schemas.UserId, db: Session = Depends(get_db)
):
    db_pirg = crud.get_pirg_by_name(db=db, name=pirg_name)
    if not db_pirg:
        raise HTTPException(status_code=404, detail="Pirg not found")
    db_user = crud.get_user(db=db, id=user.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.add_user_to_pirg(db=db, pirg=db_pirg, user=db_user)


@router.delete("/{pirg_name}/users/{user_id}", response_model=schemas.Pirg)
async def delete_pirg_user(pirg_name: str, user_id: int, db: Session = Depends(get_db)):
    db_pirg = crud.get_pirg_by_name(db=db, name=pirg_name)
    if not db_pirg:
        raise HTTPException(status_code=404, detail="Pirg not found")
    db_user = crud.get_user(db=db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.remove_user_from_pirg(db=db, pirg=db_pirg, user=db_user)


####################
# Pirg Groups
####################


@router.get("/{pirg_name}/groups", response_model=list[schemas.Group])
async def get_pirg_groups(pirg_name: str, db: Session = Depends(get_db)):
    pirg = crud.get_pirg_by_name(db=db, name=pirg_name)
    groups = crud.get_pirg_groups(db=db, pirg=pirg)
    return groups


@router.post("/{pirg_name}/groups", response_model=schemas.Group)
async def post_pirg_groups(
    pirg_name: str, group: schemas.GroupCreate, db: Session = Depends(get_db)
):
    # make sure the pirg exists
    db_pirg = crud.get_pirg_by_name(db=db, name=pirg_name)
    if not db_pirg:
        raise HTTPException(status_code=404, detail="Pirg not found")
    # make sure the group doesn't already exist
    db_group = crud.get_pirg_group_by_name(db=db, name=group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="Group already exists")
    # make sure all the users exist
    for user_id in group.user_ids:
        db_user = crud.get_user(db=db, id=user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
    return crud.create_pirg_group(db=db, group=group)


@router.post("/{pirg_name}/groups/{group_id}/users", response_model=schemas.Group)
async def post_pirg_group_users(
    pirg_name: str, group_id: int, user: schemas.UserId, db: Session = Depends(get_db)
):
    db_pirg = crud.get_pirg_by_name(db=db, name=pirg_name)
    if not db_pirg:
        raise HTTPException(status_code=404, detail="Pirg not found")
    db_group = crud.get_pirg_group(db=db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    db_user = crud.get_user(db=db, id=user.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.add_user_to_pirg_group(db=db, group=db_group, user=db_user)


@router.delete(
    "/{pirg_name}/groups/{group_id}/users/{user_id}", response_model=schemas.Group
)
async def delete_pirg_group_users(
    pirg_name: str, group_id: int, user_id: int, db: Session = Depends(get_db)
):
    db_pirg = crud.get_pirg_by_name(db=db, name=pirg_name)
    if not db_pirg:
        raise HTTPException(status_code=404, detail="Pirg not found")
    db_group = crud.get_pirg_group(db=db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    db_user = crud.get_user(db=db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.remove_user_from_pirg_group(db=db, group=db_group, user=db_user)


@router.delete("/{pirg_name}/groups/{group_id}", response_model=schemas.SimpleStatus)
async def delete_pirg_group(
    pirg_name: str, group_id: int, db: Session = Depends(get_db)
):
    db_pirg = crud.get_pirg_by_name(db=db, name=pirg_name)
    if not db_pirg:
        raise HTTPException(status_code=404, detail="Pirg not found")
    db_group = crud.get_pirg_group(db=db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    crud.delete_pirg_group(db=db, group=db_group)
    return schemas.SimpleStatus(status=schemas.Status.SUCCESS)
