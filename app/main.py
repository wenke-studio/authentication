from fastapi import Depends, FastAPI

from .dependencies import debug
from .routers import user

# models.Base.metadata.create_all(bind=engine)


app = FastAPI(dependencies=[Depends(debug)])
app.include_router(user.router)
