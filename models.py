from sqlalchemy import String, Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from db import Base


class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    total_earnings = Column(Float, index=True, nullable=True)

    items = relationship("Coin", back_populates="user")


class Coin(Base):
    __tablename__ = "coin"

    id = Column(String, primary_key=True, index=True, nullable=False)
    coin_name = Column(String, index=True, nullable=False)
    amount = Column(Integer, index=True, nullable=True)
    purchase_price = Column(Float, index=True, nullable=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="items")
