from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

app = FastAPI(title="24/7 Ishlaydigan API")

# Baza jadvallarini yaratish
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def home():
    return {"status": "API muvaffaqiyatli ishlamoqda", "uptime": "24/7"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email allaqachon ro'yxatdan o'tgan")
    
    new_user = models.User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()