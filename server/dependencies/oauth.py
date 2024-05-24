from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from server.authentication.tokens import get_user_by_access_token
from server.core.database import get_db
from server.user.models import User

oauth2_scheme = OAuth2PasswordBearer(
    # This is the path to the login from authentication
    tokenUrl="/token",
)


async def get_current_user(access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user, err = get_user_by_access_token(access_token, db)
    if err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
        )
    return user
