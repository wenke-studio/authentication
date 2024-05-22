from fastapi import Depends, FastAPI

from server.core.database import migrate
from server.dependencies import debug
from server.user import views as user

# Create the database tables
migrate()


app = FastAPI(dependencies=[Depends(debug)])
app.include_router(user.router)
