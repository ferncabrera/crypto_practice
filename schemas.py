from pydantic import BaseModel
from typing import List, Optional


class CoinBase(BaseModel):
    coin_name: str
    amount: int
    purchase_price: float


class Coin(CoinBase):
    id: str
    user_id: str

    class Config:
        orm_mode = True


class CoinCreate(CoinBase):
    pass


class UserBase(BaseModel):
    username: str
    email: str
    name: str
    hashed_password: str
    total_earnings: float


class User(UserBase):
    id: str
    coins: List[Coin] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass
