import websocket
import json
import pprint
from pip._internal import main as install
import numpy
import config
from binance.client import Client
from binance.enums import *
install(["install","ta-lib"])

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

client = Client(config.API_KEY, config.API_SECRET,tld = 'en')

rsi_period = 14
rsioverbought = 70
rsioversold = 30
trade_symmbol = 'ETHUSDT'
trade_quantity = 0.05

in_postion = False
closes = []
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('close connection')

def on_message(ws,message):
    global closes
    print('recieved message')
    print(message)
    json_message = json.loads(message)
    print(json_message)
    pprint.pprint(json_message)


    candle = json_message['k']

    is_candle_closed = candle['x']

    close = candle['c']

    if is_candle_closed:
        print('candle closed at {}'.format(close))

        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > rsi_period:
            np_closes = numpy.array(closes)
            rsi  = talib.RSI(np_closes,rsi_period)
            print("all rsi calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi {}".format(last_rsi))

            if last_rsi > rsioverbought:
                if in_postion:
                    print("sell!!!")
                    #put binance logic
                else:
                    print(" it is overbought,we don't own any")

            if last_rsi < rsioversold:
                if in_postion:
                    print("it is oversold but, youo already own it")
                else:
                    print("buy")
                    #put binance order logic




ws = websocket.WebSocketApp(SOCKET, on_open= on_open, on_close=on_close,on_message=on_message)
ws.run_forever()