from datetime import timedelta
from fastapi import FastAPI, Request, Depends, status, Form, Response, Path, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from db import SessionLocal, engine, DBContext
import models
import crud
import schemas
from sqlalchemy.orm import Session
from fastapi_login import LoginManager
from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, List, Dict
import requests
import helpers
app = FastAPI()


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 60

manager = LoginManager(SECRET_KEY, token_url="/login", use_cookie=True)
manager.cookie_name = "auth"

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Depends Functions


def get_db():
    with DBContext() as db:
        yield db


def get_hashed_password(plain_password):
    return pwd_ctx.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password, hashed_password)


@manager.user_loader()
def get_user(username: str, db: Session = None):
    if db is None:
        with DBContext() as db:
            return crud.get_user_by_username(db=db, username=username)
    return crud.get_user_by_username(db=db, username=username)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db=db, username=username)
    if not user:
        return None
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return None
    return user


class NotAuthenticatedException(Exception):
    pass


def not_authenticated_exception_handler(request, exception):
    return RedirectResponse("/login")


manager.not_authenticated_exception = NotAuthenticatedException
app.add_exception_handler(NotAuthenticatedException,
                          not_authenticated_exception_handler)


@app.get("/")
def root(request: Request, all_coins: List[Dict] = Depends(helpers.get_all_ticker_data)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home", "coins": all_coins})

@app.post("/")
def root(request: Request, all_coins: List[Dict] = Depends(helpers.get_all_ticker_data), search_coin: Optional[str] = Form(None)):
    return_coins = []
    if search_coin == None:
        return_coins = all_coins
    else:
        for coin in all_coins:
            if search_coin.lower() in coin["id"]:
                return_coins.append(coin)
        if(not return_coins):
            return templates.TemplateResponse("index.html", {"request": request, "title": "Home", "coins": return_coins, "invalid_search": True})
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home", "coins": return_coins})

@app.get("/wallet")
def get_coins(request: Request, clicked_coin: Optional[str] = Query(None),all_coins: List[Dict] = Depends(helpers.get_all_ticker_data), db: Session = Depends(get_db), user: schemas.User = Depends(manager)):
    user_coins = crud.get_coins_by_user_id(db=db, id=user.id)
    coin_dict = helpers.create_coin_dict(user_coins)
    return templates.TemplateResponse("wallet.html", {"request": request,
                                                      "title": "Wallet",
                                                      "user": user,
                                                      "user_coins": user_coins,
                                                      "coin_dict": coin_dict,
                                                      "all_coins": all_coins,
                                                      "clicked_coin": clicked_coin
                                                      })


@app.post("/wallet")
def add_coin(request: Request, search_coin: str = Form(None), all_coins: List[Dict] = Depends(helpers.get_all_ticker_data), amount: int = Form(None), coin_name: str = Form(None), db: Session = Depends(get_db), user: schemas.User = Depends(manager)):
    user_coins = crud.get_coins_by_user_id(db=db, id=user.id)
    coin_dict = helpers.create_coin_dict(user_coins)
    return_coins = []
    template_dict = {"request": request,
                    "title": "Wallet",
                    "user": user,
                    "user_coins": user_coins,
                    "coin_dict":coin_dict,
                    "all_coins": return_coins,
                    "invalid_search": False,
                    "invalid_coin": False,
                    "invalid_db": False
                    }

    if search_coin == None:
        return_coins = all_coins
    else:
        for coin in all_coins:
            if search_coin.lower() in coin["id"]:
                return_coins.append(coin)
        if(not return_coins):
            template_dict["invalid_search"] = True
        return templates.TemplateResponse("wallet.html", template_dict, status_code=status.HTTP_400_BAD_REQUEST)
   
   
    coin_price = helpers.get_ticker_price(coin_name)
    if not coin_price:
        template_dict["all_coins"] = return_coins
        template_dict["invalid_coin"] = True
        return templates.TemplateResponse("wallet.html", template_dict, status_code=status.HTTP_400_BAD_REQUEST)
    purchase_price = round(coin_price[coin_name]["usd"],3)
    added = crud.add_coin(
        db=db, coin=schemas.CoinCreate(coin_name=coin_name.lower(), amount=amount, purchase_price=purchase_price), id=user.id)
    if not added:
        template_dict["all_coins"] = return_coins
        template_dict["invalid_db"] = True
        return templates.TemplateResponse("wallet.html", template_dict, status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return RedirectResponse("/wallet", status_code=status.HTTP_302_FOUND)


@app.get("/wallet/delete/{id}", response_class=RedirectResponse)
def delete_coin(id: str = Path(...), db: Session = Depends(get_db), gain_loss: float = Query(.01) ,user: schemas.User = Depends(manager)):
    print(gain_loss)
    crud.update_user_earnings(db=db, id=user.id, update_amount=float(gain_loss))
    crud.delete_coin(db=db, id=id)
    return RedirectResponse("/wallet")


@app.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Login"})


@app.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(username=form_data.username,
                             password=form_data.password, db=db)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request,
                                                         "title": "Login",
                                                         "invalid": True}, status_code=status.HTTP_401_UNAUTHORIZED)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = manager.create_access_token(
        data={"sub": user.username},
        expires=access_token_expires
    )
    resp = RedirectResponse("/wallet", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)
    return resp


@app.get("/register")
def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "title": "Register"})


@app.post("/register")
def register(request: Request,
             username: str = Form(...),
             email: str = Form(...),
             name: str = Form(...),
             password: str = Form(...),
             db: Session = Depends(get_db)):
    hashed_password = get_hashed_password(password)
    invalid = False
    if crud.get_user_by_username(db=db, username=username):
        invalid = True
    if crud.get_user_by_email(db=db, email=email):
        invalid = True

    if not invalid:
        crud.create_user(db=db, user=schemas.UserCreate(
            username=username, email=email, name=name, hashed_password=hashed_password, total_earnings=float(0)))
        response = RedirectResponse(
            "/login", status_code=status.HTTP_302_FOUND)
        return response
    else:
        return templates.TemplateResponse("register.html", {"request": request, "title": "Register", "invalid": True},
                                          status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/logout")
def logout(response: Response):
    response = RedirectResponse("/")
    manager.set_cookie(response, None)
    return response


@app.get("/binance/{ticker}")
def get_ticker_price(ticker: str):
    api_endpoint = f"https://api.binance.com/api/v3/ticker/price?symbol={ticker}"
    data = requests.get(api_endpoint)
    parsed = data.json()
    # Note parsed is of dict type
    return parsed
