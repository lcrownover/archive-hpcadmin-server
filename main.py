import uvicorn

from fastapi import FastAPI

from hpcadmin_server.database import models, db
from hpcadmin_server.api import users, pirgs, groups

models.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(pirgs.router)
app.include_router(groups.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
