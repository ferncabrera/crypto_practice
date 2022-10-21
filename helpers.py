import requests

coin_list = [
    "DOTUSDT",
    "ADAUSDT",
    "BTCUSDT",
    "VETUSDT",
    "CHZUSDT",
    "ETHUSDT",
]


def get_all_ticker_data():
    api_endpoint = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=25&page=1&sparkline=false"
    data = requests.get(api_endpoint)
    parsed = data.json()
    return parsed

def get_ticker_price(ticker: str):
    api_endpoint = f"https://api.coingecko.com/api/v3/simple/price?ids={ticker.lower()}&vs_currencies=usd"
    data = requests.get(api_endpoint)
    parsed = data.json()
    return parsed

def get_curr_prices(coins):
    query_string =  "%2C".join(coins)
    api_endpoint = f"https://api.coingecko.com/api/v3/simple/price?ids={query_string}&vs_currencies=usd"
    data = requests.get(api_endpoint)
    parsed = data.json()
    return parsed

def create_coin_dict(coins):
    coin_dict = {}
    for coin in coins:
        if coin.coin_name not in coin_dict:
               coin_dict[coin.coin_name] = 0
    curr_prices = get_curr_prices(coin_dict)
    for key in coin_dict:
        coin_dict[key] = round(curr_prices[key]["usd"],3)
    return coin_dict
