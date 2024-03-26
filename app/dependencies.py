from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models import User

# TODO: actual logic for verifying and decoding authentication tokens to retrieve user information.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#fake database of users
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}

def fake_hash_password(password: str):
    return "fakehashed" + password

#dependency
async def get_current_active_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # TODO: verify the token and return the user information
    user = fake_users_db.get("johndoe")
    if user is None:
        raise credentials_exception
    user_obj = User(
        username=user["username"],
        email=user["email"],
        hashed_password=user["hashed_password"],
        disabled=user.get("disabled", False)
    )
    return user_obj
