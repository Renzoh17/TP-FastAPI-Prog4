from fastapi import FastAPI, Depends
from sqlmodel import Session
from database import get_session, create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.get("/")
def read_root(session: Session = Depends(get_session)):
    return {"status": "OK"}