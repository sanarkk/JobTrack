from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from backend.auth.auth import get_password_hash, verify_password, create_access_token
from backend.dependencies.user_dependencies import get_user_by_email, create_user, get_email_from_token
from backend.database.session import get_db
from sqlalchemy.orm import Session
from backend.schemas.user_schemas import UserCreate, UserOut

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")


@router.post("/register/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_password = get_password_hash(user.password)
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": hashed_password,
    }

    new_user = create_user(db, user_data)
    return new_user


@router.post("/token/")
def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = get_user_by_email(db, form_data.username)


    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/me/")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    data = get_email_from_token(token=token)
    user = get_user_by_email(db, data)

    return user