from fastapi import Depends, FastAPI

from .database import Base, engine
from .dependencies import debug
from .routers import user

Base.metadata.create_all(bind=engine)


app = FastAPI(dependencies=[Depends(debug)])
app.include_router(user.router)
