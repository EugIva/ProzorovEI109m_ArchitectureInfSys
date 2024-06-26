from fastapi import FastAPI, HTTPException, Query, Depends, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import hashlib
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://EUGIVA:EUGIVA@postgres:5432/arch_db"

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    for error in details:
        if error["msg"] == "Field required" or error["msg"] == "missing":
            modified_details.append(
                {
                    "message": f"The field {error["loc"][1]} absent in your request",
                }
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )


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
    try:
        recipient_data = recipient.model_dump()
        recipient_data['password'] = hashlib.sha256(
            recipient_data['password'].encode()).hexdigest()

        db_recipient = Recipient(**recipient_data)
        db.add(db_recipient)
        db.commit()
        db.refresh(db_recipient)
        return {"recipient_id": db_recipient.recipient_id}
    except:
        raise HTTPException(
            status_code=400, detail="Recipient creating failed")


@app.put("/update_recipient")
def update_recipient(recipient_id: int, recipient: RecipientUpdate, db=Depends(get_db)):
    try:
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
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Recipient updating failed")


@app.get("/get_recipient_details")
def get_recipient_details(recipient_id: int, db=Depends(get_db)):
    try:
        db_recipient = db.query(Recipient).filter(
            Recipient.recipient_id == recipient_id).first()
        if db_recipient is None:
            raise HTTPException(status_code=404, detail="Recipient not found")
        return db_recipient
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Recipient getting failed, please check id and try again")


@app.delete("/remove_recipient")
async def remove_user(recipient_id: int, db=Depends(get_db)):
    try:
        recipient = db.query(Recipient).filter(
            Recipient.recipient_id == recipient_id).first()
        db.delete(recipient)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Failed to remove user")
    finally:
        db.close()
    return {"message": "User successfully removed"}, 200


@app.get("/search_by_name")
def search_by_name(first_name: str = Query(None, min_length=1), second_name: str = Query(None, min_length=1), db=Depends(get_db)):
    try:
        results = db.query(Recipient).filter(Recipient.first_name.ilike(
            f'{first_name}%'), Recipient.second_name.ilike(f'{second_name}%')).all()
    except:
        raise HTTPException(
            status_code=400, detail="Bad first name or second name. Check it and try again")
    return results


@app.get("/search_by_recipient_login/")
def search_by_username(recipient_login: str = Query(None, min_length=1), db=Depends(get_db)):
    try:
        results = db.query(Recipient).filter(
            Recipient.recipient_login.ilike(f'{recipient_login}%')).all()
    except:
        raise HTTPException(
            status_code=400, detail="Bad first name or second name. Check it and try again")
    return results
