'''
1.) User Registration
    Endpoint: /auth/register
    Method: POST
    Description: Allows new users to create an account.
    Request Body: JSON object containing username, email, and password.
    Response: JSON object with a message indicating success or failure and user details.

2.) User Login
    Endpoint: /auth/login
    Method: POST
    Description: Authenticates users and returns a token.
    Request Body: JSON object with username and password.
    Response: JSON object with an authentication token (JWT).

3.) Token Refresh (Optional)
    Endpoint: /auth/refresh
    Method: POST
    Description: Refreshes an expired authentication token.
    Request Body: JSON object with refresh_token.
    Response: JSON object with a new authentication token.
'''

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from pydantic import BaseModel

#define the router
router = APIRouter(prefix="/auth")

#simulating a user database with a dictionary
fake_users_db = {}

#password context for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#JWT secret and algorithm
SECRET_KEY = "YOUR_SECRET_KEY"  #use a secure secret key (removed for public git)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  #token expiration time

class User(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(User):
    hashed_password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register")
async def register_user(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = {"username": user.username, "email": user.email, "hashed_password": hashed_password}
    return {"message": "User successfully registered.", "username": user.username, "email": user.email}

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Assuming you have a mechanism to refresh tokens
@router.post("/refresh")
async def refresh_token():
    # Placeholder for token refresh logic
    return {"access_token": "new_access_token", "token_type": "bearer"}