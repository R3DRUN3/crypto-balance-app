import re
import json
import uvicorn
import requests
from fastapi import FastAPI
from requests import Request, Session
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse

PRICE_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC,ETH'
BTC_BALANCE_URL = "https://www.blockchain.com/btc/address/"
ETH_BALANCE_URL = "https://www.blockchain.com/eth/address/"
PARAMETERS = {
  'convert':'EUR'
}
HEADERS = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'COINMARKETCAP_API_KEY_HERE',
}
BTC_ADDRESS_LIST=["BTC_ADDRESS_1_HERE", 
                  "BTC_ADDRESS_2_HERE", 
                  "BTC_ADDRESS_3_HERE"
                ]
ETH_ADDRESS_LIST=["ETH_ADDRESS_1_HERE",
                  "ETH_ADDRESS_2_HERE",
                  "ETH_ADDRESS_3_HERE"
                ]
FAVICON_PATH = 'favicon.ico'

app = FastAPI()

@app.get('/favicon.ico')
async def favicon():
    return FileResponse(FAVICON_PATH)

@app.get("/wallet", response_class=HTMLResponse)
async def read_news():
    eth_amount=get_eth_balance(ETH_ADDRESS_LIST)
    btc_amount =get_btc_balance(BTC_ADDRESS_LIST)
    total_price = get_total_price(btc_amount, eth_amount)
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
            <title>CRYPTO WALLET</title>
            <style>
                    html {
                        height: 100%;
                    }
                    body {
                        height: 100%;
                        margin: 0;
                        background-repeat: no-repeat;
                        background-attachment: fixed;
                        background: linear-gradient(70deg, #ffcc00, #665200);
                    }
                    /* Header/Logo Title */
                    .header {
                        padding: 60px;
                        text-align: center;
                        background: #1abc9c;
                        color: white;
                        font-size: 30px;
                        background: linear-gradient(70deg, #33ff33, #001a00);
                    }
                    h1 {
                        color: black;
                        animation-duration: 3s;
                        animation-name: slidein;
                    }

                    @keyframes slidein {
                    from {
                        margin-left: 100%;
                        width: 300%;
                    }

                    to {
                        margin-left: 0%;
                        width: 100%;
                    }
                    }
                    p {
                        color: black;
                    animation-duration: 3s;
                    animation-name: slideout;
                    }

                    @keyframes slideout {
                    from {
                        margin-right: 100%;
                        width: 300%;
                    }

                    to {
                        margin-left: 0%;
                        width: 100%;
                    }
                    }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>BTC """+str(btc_amount)+""" ₿</h1>
                </br>
                <h1>ETH """+str(eth_amount)+""" ⧫</h1>
                </br>
                </br>
                <h1>TOTAL WEALTH: """+str(total_price)+""" 💶</h1>
                </br>
            </div>
            </br>
            </br>
            <h3><center>💰 YOUR WELCOME! 💰</center></h3>
            </br>
            <ul>  
        """
    
    return HTMLResponse(content=html_content, status_code=200)

def get_total_price(btc_total, eth_total):
    session = Session()
    session.headers.update(HEADERS)
    response = session.get(PRICE_URL, params=PARAMETERS)
    data = json.loads(response.text)
    btcPrice = data['data']['BTC']['quote']['USD']['price']
    ethPrice = data['data']['ETH']['quote']['USD']['price']
    totalValue = ((btcPrice*btc_total) +(ethPrice* eth_total))
    totalValue = round(totalValue, 2)
    return totalValue

def get_eth_balance(eth_address_list):
    total_eth_balance = 0.0
    for a in eth_address_list:
        r=requests.get(ETH_BALANCE_URL+a).content
        r = re.search(r'The current value of this address is(.*?)ETH', str(r)).group(1)
        total_eth_balance += float(r)
    return total_eth_balance

def get_btc_balance(btc_address_list):
    total_btc_balance = 0.0
    for a in btc_address_list:
        r=requests.get(BTC_BALANCE_URL+a).content
        r = re.search(r'The current value of this address is(.*?)BTC', str(r)).group(1)
        total_btc_balance += float(r)
    return total_btc_balance

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4321)
