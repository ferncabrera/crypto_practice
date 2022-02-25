from sqlalchemy.orm import Session
import models
import schemas
import uuid
import requests


def get_user(db: Session, id: str):
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    id = uuid.uuid4()
    while get_user(db=db, id=str(id)):
        id = uuid.uuid4()
    db_user = models.User(id=str(id), username=user.username, name=user.name,
                          email=user.email, hashed_password=user.hashed_password, total_earnings=user.total_earnings)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_earnings(db: Session, id: str, update_amount: float = 0):
    db_user = db.query(models.User).filter(models.User.id == id).one_or_none()
    if db_user is None:
        print("no user found")
        return None
        
    current_amount = db_user.total_earnings
    setattr(db_user, "total_earnings", current_amount + update_amount)

    db.commit()
    db.refresh(db_user)
    return db_user

def get_coins_by_user_id(db: Session, id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Coin).filter(models.Coin.user_id == id).offset(skip).limit(limit).all()


def get_coin_by_id(db: Session, id: str):
    return db.query(models.Coin).filter(models.Coin.id == id).first()


def add_coin(db: Session, coin: schemas.CoinCreate, id: str):
    if not get_user(db=db, id=str(id)):
        return None
    coin_id = uuid.uuid4()
    while get_coin_by_id(db=db, id=str(coin_id)):
        coin_id = uuid.uuid4()

    db_coin = models.Coin(id=str(coin_id), purchase_price=coin.purchase_price, coin_name=coin.coin_name, amount=coin.amount, user_id=id)
    db.add(db_coin)
    db.commit()
    db.refresh(db_coin)
    return db_coin


def delete_coin(db: Session, id: str):
    db.query(models.Coin).filter(models.Coin.id == id).delete()
    db.commit()
