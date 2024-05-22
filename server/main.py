from fastapi import Depends, FastAPI

from .core.database import migrate
from .dependencies import debug
from .routers import user

# Create the database tables
migrate()


app = FastAPI(dependencies=[Depends(debug)])
app.include_router(user.router)
