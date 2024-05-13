from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import subprocess
import random

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def call_model(user: schemas.UserCreate, db: Session = Depends(get_db)):
    ctx = crud.create_user(db=db, user=user)
    subprocess.run(["python", "trigger.py"])

    result = random.uniform(0,1)
    # result = datamodel.evaluate(ctx)
    return crud.pretext_handling(result)

@app.post("/")
def root(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not user.content and not user.url:
        raise HTTPException(status_code=400, detail="Need input either URL or text content")
    
    if user.content:
        if crud.text_is_English(user.content): 
            if crud.text_is_Gibberish(user.content):
                raise HTTPException(status_code=400, detail="Input text is gibberish.")
            else: return call_model(db=db,user=user)
        else: 
            raise HTTPException(status_code=400, detail="For now we process content in the English language only")
    else:
        if crud.url_is_valid(user.url):
            return call_model(db=db,user=user)
        else:
            raise HTTPException(status_code=400, detail="Invalid URL request")


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, customer_name=user.customer_name)
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user