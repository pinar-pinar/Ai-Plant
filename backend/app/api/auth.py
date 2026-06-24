from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext
from jose import jwt
import os

router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/db.sqlite")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "devsecret")
ALGORITHM = "HS256"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

class SignupIn(BaseModel):
    username: str
    password: str

class LoginIn(BaseModel):
    username: str
    password: str

@router.post("/signup")
def signup(payload: SignupIn):
    db = SessionLocal()
    user = db.query(User).filter(User.username == payload.username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = pwd_context.hash(payload.password)
    u = User(username=payload.username, hashed_password=hashed)
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"id": u.id, "username": u.username}

@router.post("/login")
def login(payload: LoginIn):
    db = SessionLocal()
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not pwd_context.verify(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
