from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel
import hashlib
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://EugIva:EugIva@postgres:5432/arch_db"

Base = declarative_base()


class Recipient(Base):
    __tablename__ = 'recipients'

    recipient_id = Column(Integer, primary_key=True)
    recipient_login = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), nullable=False)
    second_name = Column(String(255))
    address = Column(String(255))
    password = Column(String(255), nullable=False)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()


class RecipientCreate(BaseModel):
    recipient_login: str
    first_name: str
    second_name: str = None
    address: str = None
    password: str


class RecipientUpdate(BaseModel):
    recipient_login: str = None
    first_name: str = None
    second_name: str = None
    address: str = None
    password: str = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_recipient/")
def create_recipient(recipient: RecipientCreate, db=Depends(get_db)):
    recipient_data = recipient.model_dump()
    recipient_data['password'] = hashlib.sha256(
        recipient_data['password'].encode()).hexdigest()

    db_recipient = Recipient(**recipient_data)
    db.add(db_recipient)
    db.commit()
    db.refresh(db_recipient)
    return {"recipient_id": db_recipient.recipient_id}


@app.put("/update_recipient/{recipient_id}")
def update_recipient(recipient_id: int, recipient: RecipientUpdate, db=Depends(get_db)):
    db_recipient = db.query(Recipient).filter(
        Recipient.recipient_id == recipient_id).first()
    if db_recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    recipient_data = recipient.model_dump(exclude_unset=True)
    if recipient_data.get('password'):
        recipient_data['password'] = hashlib.sha256(
            recipient_data['password'].encode()).hexdigest()
    for key, value in recipient_data.items():
        setattr(db_recipient, key, value)
    db.commit()
    return {"message": "Recipient updated successfully"}


@app.get("/get_recipient_details/{recipient_id}")
def get_recipient_details(recipient_id: int, db=Depends(get_db)):
    db_recipient = db.query(Recipient).filter(
        Recipient.recipient_id == recipient_id).first()
    if db_recipient is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    return db_recipient


@app.delete("/remove_recipient/{recipient_id}")
async def remove_user(recipient_id: int, db=Depends(get_db)):
    try:
        recipient = db.query(Recipient).filter(
            Recipient.recipient_id == recipient_id).first()
        db.delete(recipient)
        db.commit()
    except HTTPException as http_error:
        print("HTTP Exception occurred:",
              http_error.status_code, http_error.detail)
        return {"error": http_error.detail}, http_error.status_code
    except Exception as e:
        print(e)
        db.rollback()
        return {"error": "Failed to remove user"}, 500
    finally:
        db.close()

    return {"message": "successfully removed"}, 200


@app.get("/search_by_name/")
def search_by_name(first_name: str = Query(None, min_length=1), second_name: str = Query(None, min_length=1), db=Depends(get_db)):
    if not first_name or not second_name:
        raise HTTPException(
            status_code=400, detail="Missing required parameters: first_name and second_name")
    results = db.query(Recipient).filter(Recipient.first_name.ilike(
        f'{first_name}%'), Recipient.second_name.ilike(f'{second_name}%')).all()
    return results


@app.get("/search_by_recipient_login/")
def search_by_username(recipient_login: str = Query(None, min_length=1), db=Depends(get_db)):
    if not recipient_login:
        raise HTTPException(
            status_code=400, detail="Missing required parameter: recipient_login")
    results = db.query(Recipient).filter(
        Recipient.recipient_login.ilike(f'{recipient_login}%')).all()
    return results
