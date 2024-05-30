from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from server.asset import views as asset
from server.authentication import views as auth
from server.authentication.controllers import authenticate_user
from server.authentication.schemas import Credential
from server.authentication.tokens import create_token_by_user
from server.core.database import get_db, migrate
from server.tag import views as tag
from server.user import views as user

# Create the database tables
migrate()


app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(tag.router)
app.include_router(asset.router)


@app.post(
    "/token",
    summary="Swagger authorize only",
    description="""
    !! To exclude this path from the OpenAPI schema. !! \n
    OAuth2PasswordBearer provides an authorization form that uses form data rather than JSON.\n
    https://github.com/tiangolo/fastapi/discussions/7616
    """,
    tags=["Hidden"],
    include_in_schema=False,
)
def swagger_authorize(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    # This should be the same as the login path from authentication
    credential = Credential(email=form_data.username, password=form_data.password)
    user, err = authenticate_user(db, credential)
    if err is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
        )
    user_token = create_token_by_user(user)
    return user_token
